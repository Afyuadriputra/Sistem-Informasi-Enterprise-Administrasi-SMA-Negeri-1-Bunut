from io import StringIO

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.accounts.models import Role
from apps.administration.models import Document, ServiceRequest, ServiceType
from apps.attendance.models import Attendance
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.student_affairs.models import StudentCase

User = get_user_model()


@pytest.mark.django_db
def test_seeder_rejects_production_environment(monkeypatch):
    """Seeder must fail-fast and reject execution in production environment."""
    monkeypatch.setattr(settings, "DJANGO_ENV", "production")
    out = StringIO()
    with pytest.raises(CommandError) as exc_info:
        call_command("seed_school_data", "--profile", "small", stdout=out)
    assert "dilarang keras" in str(exc_info.value).lower()


@pytest.mark.django_db
def test_seeder_dry_run_does_not_mutate_database():
    """Dry run should display simulation plan without creating or mutating database records."""
    initial_user_count = User.objects.count()
    initial_student_count = Student.objects.count()
    out = StringIO()

    call_command("seed_school_data", "--profile", "small", "--dry-run", stdout=out)
    output = out.getvalue()

    assert "DRY RUN MODE" in output
    assert "Dry run selesai" in output
    assert User.objects.count() == initial_user_count
    assert Student.objects.count() == initial_student_count


@pytest.mark.django_db
def test_seeder_small_profile_creates_complete_interconnected_data(tmp_path, monkeypatch):
    """Small profile should populate all required entities, relations, and physical files."""
    monkeypatch.setattr(settings, "PRIVATE_MEDIA_ROOT", tmp_path)
    monkeypatch.setattr(settings, "DJANGO_ENV", "development")

    out = StringIO()
    call_command("seed_school_data", "--profile", "small", "--seed", "123", "--role-passwords", stdout=out)
    output = out.getvalue()

    assert "POPULASI DATABASE SELESAI" in output

    # 1. Roles
    assert Role.objects.count() == 6
    expected_roles = {"Administrator", "Guru", "Wali Kelas", "Kesiswaan", "Tata Usaha", "Pimpinan"}
    assert set(Role.objects.values_list("name", flat=True)) == expected_roles

    # 2. Academic Years - Exactly 1 active
    active_years = AcademicYear.objects.filter(is_active=True)
    assert active_years.count() == 1
    assert active_years.first().name == "2026/2027"

    # 3. School Classes
    assert SchoolClass.objects.filter(academic_year=active_years.first()).count() >= 2

    # 4. Users and Password Hashing
    admin_user = User.objects.filter(username="admin").first()
    assert admin_user is not None
    assert admin_user.check_password("Admin123!")
    assert admin_user.roles.filter(name="Administrator").exists()

    guru_user = User.objects.filter(username="guru").first()
    assert guru_user is not None
    assert guru_user.check_password("Guru123!")
    assert guru_user.roles.filter(name="Guru").exists()

    multi_role_user = User.objects.filter(username="guru_walikelas").first()
    assert multi_role_user is not None
    assert multi_role_user.check_password("GuruWali123!")
    user_roles = set(multi_role_user.roles.values_list("name", flat=True))
    assert "Guru" in user_roles and "Wali Kelas" in user_roles

    # 5. Students & Enrollments
    students = Student.objects.filter(status="AKTIF")
    assert students.count() >= 20
    # Unique student numbers
    student_numbers = list(students.values_list("student_number", flat=True))
    assert len(student_numbers) == len(set(student_numbers))

    enrollments = Enrollment.objects.filter(student__in=students)
    assert enrollments.count() >= 20

    # 6. Class Assignments
    assignments = ClassAssignment.objects.all()
    assert assignments.filter(role="WALI_KELAS").exists()
    assert assignments.filter(role="GURU_MAPEL").exists()

    # 7. Attendance
    attendances = Attendance.objects.all()
    assert attendances.count() > 0
    valid_statuses = {"HADIR", "SAKIT", "IZIN", "ALPA"}
    found_statuses = set(attendances.values_list("status", flat=True))
    assert found_statuses.issubset(valid_statuses)

    # 8. Student Cases and Events
    cases = StudentCase.objects.all()
    assert cases.count() >= 6
    assert cases.filter(events__action="CATAT_TINDAKAN").exists()

    # 9. Administration, Requests, and Physical Documents
    assert ServiceType.objects.count() >= 5
    requests = ServiceRequest.objects.all()
    assert requests.count() >= 12

    docs = Document.objects.all()
    assert docs.count() >= 5
    for doc in docs:
        doc_file = tmp_path / doc.storage_key
        assert doc_file.exists(), f"Physical file missing for document {doc.storage_key}"
        assert doc_file.stat().st_size == doc.file_size
        assert doc.mime_type == "application/pdf"


@pytest.mark.django_db
def test_seeder_idempotent_rerun_does_not_duplicate(tmp_path, monkeypatch):
    """Rerunning seeder multiple times must be idempotent and avoid creating duplicates."""
    monkeypatch.setattr(settings, "PRIVATE_MEDIA_ROOT", tmp_path)
    monkeypatch.setattr(settings, "DJANGO_ENV", "development")

    out1 = StringIO()
    call_command("seed_school_data", "--profile", "small", "--seed", "77", stdout=out1)

    roles_count1 = Role.objects.count()
    users_count1 = User.objects.count()
    classes_count1 = SchoolClass.objects.count()
    students_count1 = Student.objects.count()
    attendances_count1 = Attendance.objects.count()
    cases_count1 = StudentCase.objects.count()
    requests_count1 = ServiceRequest.objects.count()

    out2 = StringIO()
    call_command("seed_school_data", "--profile", "small", "--seed", "77", stdout=out2)

    assert Role.objects.count() == roles_count1
    assert User.objects.count() == users_count1
    assert SchoolClass.objects.count() == classes_count1
    assert Student.objects.count() == students_count1
    assert Attendance.objects.count() == attendances_count1
    assert StudentCase.objects.count() == cases_count1
    assert ServiceRequest.objects.count() == requests_count1
