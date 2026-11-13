import pytest
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.master_data.models import AcademicYear, SchoolClass


@pytest.fixture
def auth_tokens(db):
    admin_role = Role.objects.create(name="Administrator")
    tu_role = Role.objects.create(name="Tata Usaha")
    guru_role = Role.objects.create(name="Guru")

    admin = User.objects.create_user(username="admin_user", password="Password123!")
    UserRole.objects.create(user=admin, role=admin_role)

    tu = User.objects.create_user(username="tu_user", password="Password123!")
    UserRole.objects.create(user=tu, role=tu_role)

    guru = User.objects.create_user(username="guru_user", password="Password123!")
    UserRole.objects.create(user=guru, role=guru_role)

    return {
        "admin": issue_token_pair(admin)["access_token"],
        "tu": issue_token_pair(tu)["access_token"],
        "guru": issue_token_pair(guru)["access_token"],
    }


@pytest.mark.django_db
def test_academic_year_lifecycle_and_validation(client: Client, auth_tokens):
    headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_tokens['admin']}"}

    # 1. Invalid date range
    bad_res = client.post(
        "/api/master/academic-years",
        data={
            "name": "2026/2027 Ganjil",
            "start_date": "2026-12-01",
            "end_date": "2026-07-01",
            "is_active": True,
        },
        content_type="application/json",
        **headers,
    )
    assert bad_res.status_code == 422

    # 2. Valid creation
    create_res = client.post(
        "/api/master/academic-years",
        data={
            "name": "2026/2027 Ganjil",
            "start_date": "2026-07-15",
            "end_date": "2026-12-20",
            "is_active": True,
        },
        content_type="application/json",
        **headers,
    )
    assert create_res.status_code == 201
    ay1_id = create_res.json()["id"]

    # 3. Create second active year -> first year becomes inactive
    create_res2 = client.post(
        "/api/master/academic-years",
        data={
            "name": "2026/2027 Genap",
            "start_date": "2027-01-10",
            "end_date": "2027-06-25",
            "is_active": True,
        },
        content_type="application/json",
        **headers,
    )
    assert create_res2.status_code == 201
    assert AcademicYear.objects.get(id=ay1_id).is_active is False
    assert AcademicYear.objects.get(id=create_res2.json()["id"]).is_active is True


@pytest.mark.django_db
def test_school_class_and_level_validation(client: Client, auth_tokens):
    headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_tokens['admin']}"}
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-15", end_date="2026-12-20", is_active=True
    )

    # Invalid level (must be 10, 11, or 12)
    bad_level_res = client.post(
        "/api/master/classes",
        data={"academic_year_id": ay.id, "name": "X-A", "level": 9},
        content_type="application/json",
        **headers,
    )
    assert bad_level_res.status_code == 422

    # Valid class creation
    res1 = client.post(
        "/api/master/classes",
        data={"academic_year_id": ay.id, "name": "X-A", "level": 10},
        content_type="application/json",
        **headers,
    )
    assert res1.status_code == 201

    # Duplicate class name in same academic year
    dup_res = client.post(
        "/api/master/classes",
        data={"academic_year_id": ay.id, "name": "X-A", "level": 10},
        content_type="application/json",
        **headers,
    )
    assert dup_res.status_code == 422


@pytest.mark.django_db
def test_student_and_enrollment_integrity(client: Client, auth_tokens):
    headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_tokens['tu']}"}
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-15", end_date="2026-12-20", is_active=True
    )
    cls = SchoolClass.objects.create(academic_year=ay, name="X-A", level=10)

    # Create student
    std_res = client.post(
        "/api/master/students",
        data={"student_number": "20261001", "name": "Budi Santoso", "gender": "LAKI_LAKI"},
        content_type="application/json",
        **headers,
    )
    assert std_res.status_code == 201
    student_id = std_res.json()["id"]

    # Duplicate student number rejected
    dup_std = client.post(
        "/api/master/students",
        data={"student_number": "20261001", "name": "Budi Duplikat", "gender": "LAKI_LAKI"},
        content_type="application/json",
        **headers,
    )
    assert dup_std.status_code == 422

    # Create first enrollment
    enr_res1 = client.post(
        "/api/master/enrollments",
        data={"student_id": student_id, "class_id": cls.id, "start_date": "2026-07-15"},
        content_type="application/json",
        **headers,
    )
    assert enr_res1.status_code == 201
    enr1_id = enr_res1.json()["id"]

    # Overlapping active enrollment rejected
    cls2 = SchoolClass.objects.create(academic_year=ay, name="X-B", level=10)
    enr_dup = client.post(
        "/api/master/enrollments",
        data={"student_id": student_id, "class_id": cls2.id, "start_date": "2026-08-01"},
        content_type="application/json",
        **headers,
    )
    assert enr_dup.status_code == 422

    # Close previous enrollment -> new enrollment succeeds
    client.patch(
        f"/api/master/enrollments/{enr1_id}",
        data={"end_date": "2026-07-31"},
        content_type="application/json",
        **headers,
    )
    enr_res2 = client.post(
        "/api/master/enrollments",
        data={"student_id": student_id, "class_id": cls2.id, "start_date": "2026-08-01"},
        content_type="application/json",
        **headers,
    )
    assert enr_res2.status_code == 201


@pytest.mark.django_db
def test_employee_and_assignment_rbac(client: Client, auth_tokens):
    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_tokens['admin']}"}
    guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_tokens['guru']}"}

    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-15", end_date="2026-12-20", is_active=True
    )
    cls = SchoolClass.objects.create(academic_year=ay, name="X-A", level=10)

    # Guru cannot create employee -> 403
    emp_fail = client.post(
        "/api/master/employees",
        data={"nip": "198001012005011001", "name": "Dra. Siti Aminah"},
        content_type="application/json",
        **guru_headers,
    )
    assert emp_fail.status_code == 403

    # Admin creates employee
    emp_res = client.post(
        "/api/master/employees",
        data={"nip": "198001012005011001", "name": "Dra. Siti Aminah"},
        content_type="application/json",
        **admin_headers,
    )
    assert emp_res.status_code == 201
    emp_id = emp_res.json()["id"]

    # Admin assigns teacher to class
    asg_res = client.post(
        "/api/master/assignments",
        data={
            "employee_id": emp_id,
            "class_id": cls.id,
            "role": "WALI_KELAS",
            "start_date": "2026-07-15",
        },
        content_type="application/json",
        **admin_headers,
    )
    assert asg_res.status_code == 201
    asg_id = asg_res.json()["id"]

    # Duplicate active assignment rejected
    asg_dup = client.post(
        "/api/master/assignments",
        data={
            "employee_id": emp_id,
            "class_id": cls.id,
            "role": "WALI_KELAS",
            "start_date": "2026-07-15",
        },
        content_type="application/json",
        **admin_headers,
    )
    assert asg_dup.status_code == 422

    # Cancel assignment
    del_res = client.delete(f"/api/master/assignments/{asg_id}", **admin_headers)
    assert del_res.status_code == 200
