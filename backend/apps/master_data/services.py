from django.db import transaction

from apps.accounts.models import ActivityLog, User
from apps.core.exceptions import BusinessValidationError, NotFoundError
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.master_data.schemas import (
    AcademicYearCreateRequest,
    AcademicYearUpdateRequest,
    ClassAssignmentCreateRequest,
    ClassAssignmentUpdateRequest,
    ClassCreateRequest,
    ClassUpdateRequest,
    EmployeeCreateRequest,
    EmployeeUpdateRequest,
    EnrollmentCreateRequest,
    EnrollmentUpdateRequest,
    StudentCreateRequest,
    StudentUpdateRequest,
)
from apps.reports.services import invalidate_dashboard_cache


# Academic Year Services
@transaction.atomic
def create_academic_year(data: AcademicYearCreateRequest, actor: User) -> AcademicYear:
    if data.start_date >= data.end_date:
        raise BusinessValidationError("Tanggal mulai tahun ajaran harus lebih awal dari tanggal selesai.")

    if AcademicYear.objects.filter(name=data.name).exists():
        raise BusinessValidationError("Nama tahun ajaran sudah terdaftar.")

    if data.is_active:
        AcademicYear.objects.filter(is_active=True).update(is_active=False)

    ay = AcademicYear.objects.create(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        is_active=data.is_active,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_ACADEMIC_YEAR",
        resource_type="master_data",
        resource_id=str(ay.id),
    )
    return ay


@transaction.atomic
def update_academic_year(year_id: int, data: AcademicYearUpdateRequest, actor: User) -> AcademicYear:
    ay = AcademicYear.objects.filter(id=year_id).first()
    if not ay:
        raise NotFoundError("Tahun ajaran tidak ditemukan.")

    start = data.start_date if data.start_date is not None else ay.start_date
    end = data.end_date if data.end_date is not None else ay.end_date
    if start >= end:
        raise BusinessValidationError("Tanggal mulai tahun ajaran harus lebih awal dari tanggal selesai.")

    if data.name is not None:
        if AcademicYear.objects.filter(name=data.name).exclude(id=ay.id).exists():
            raise BusinessValidationError("Nama tahun ajaran sudah terdaftar.")
        ay.name = data.name

    if data.start_date is not None:
        ay.start_date = data.start_date
    if data.end_date is not None:
        ay.end_date = data.end_date

    if data.is_active is not None:
        if data.is_active:
            AcademicYear.objects.filter(is_active=True).exclude(id=ay.id).update(is_active=False)
        ay.is_active = data.is_active

    ay.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_ACADEMIC_YEAR",
        resource_type="master_data",
        resource_id=str(ay.id),
    )
    return ay


# School Class Services
@transaction.atomic
def create_school_class(data: ClassCreateRequest, actor: User) -> SchoolClass:
    ay = AcademicYear.objects.filter(id=data.academic_year_id).first()
    if not ay:
        raise NotFoundError("Tahun ajaran tidak ditemukan.")

    if data.level not in (10, 11, 12):
        raise BusinessValidationError("Tingkat kelas harus bernilai 10, 11, atau 12.")

    if SchoolClass.objects.filter(academic_year=ay, name=data.name).exists():
        raise BusinessValidationError("Nama kelas sudah terdaftar pada tahun ajaran ini.")

    cls = SchoolClass.objects.create(
        academic_year=ay,
        name=data.name,
        level=data.level,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_CLASS",
        resource_type="master_data",
        resource_id=str(cls.id),
    )
    return cls


@transaction.atomic
def update_school_class(class_id: int, data: ClassUpdateRequest, actor: User) -> SchoolClass:
    cls = SchoolClass.objects.select_related("academic_year").filter(id=class_id).first()
    if not cls:
        raise NotFoundError("Kelas tidak ditemukan.")

    if data.level is not None:
        if data.level not in (10, 11, 12):
            raise BusinessValidationError("Tingkat kelas harus bernilai 10, 11, atau 12.")
        cls.level = data.level

    if data.name is not None:
        if SchoolClass.objects.filter(academic_year=cls.academic_year, name=data.name).exclude(id=cls.id).exists():
            raise BusinessValidationError("Nama kelas sudah terdaftar pada tahun ajaran ini.")
        cls.name = data.name

    cls.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_CLASS",
        resource_type="master_data",
        resource_id=str(cls.id),
    )
    return cls


# Employee Services
@transaction.atomic
def create_employee(data: EmployeeCreateRequest, actor: User) -> Employee:
    if data.nip and Employee.objects.filter(nip=data.nip).exists():
        raise BusinessValidationError("NIP pegawai sudah terdaftar.")

    emp = Employee.objects.create(
        nip=data.nip,
        name=data.name,
        phone=data.phone,
        status=data.status,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_EMPLOYEE",
        resource_type="master_data",
        resource_id=str(emp.id),
    )
    return emp


@transaction.atomic
def update_employee(employee_id: int, data: EmployeeUpdateRequest, actor: User) -> Employee:
    emp = Employee.objects.filter(id=employee_id).first()
    if not emp:
        raise NotFoundError("Pegawai tidak ditemukan.")

    if data.nip is not None:
        if data.nip and Employee.objects.filter(nip=data.nip).exclude(id=emp.id).exists():
            raise BusinessValidationError("NIP pegawai sudah terdaftar.")
        emp.nip = data.nip

    if data.name is not None:
        emp.name = data.name
    if data.phone is not None:
        emp.phone = data.phone
    if data.status is not None:
        emp.status = data.status

    emp.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_EMPLOYEE",
        resource_type="master_data",
        resource_id=str(emp.id),
    )
    return emp


# Student Services
@transaction.atomic
def create_student(data: StudentCreateRequest, actor: User) -> Student:
    if Student.objects.filter(student_number=data.student_number).exists():
        raise BusinessValidationError("Nomor induk siswa sudah terdaftar.")

    student = Student.objects.create(
        student_number=data.student_number,
        name=data.name,
        gender=data.gender,
        status=data.status,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_STUDENT",
        resource_type="master_data",
        resource_id=str(student.id),
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return student


@transaction.atomic
def update_student(student_id: int, data: StudentUpdateRequest, actor: User) -> Student:
    student = Student.objects.filter(id=student_id).first()
    if not student:
        raise NotFoundError("Data siswa tidak ditemukan.")

    if data.name is not None:
        student.name = data.name
    if data.gender is not None:
        student.gender = data.gender
    if data.status is not None:
        student.status = data.status

    student.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_STUDENT",
        resource_type="master_data",
        resource_id=str(student.id),
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return student


# Enrollment Services
@transaction.atomic
def create_enrollment(data: EnrollmentCreateRequest, actor: User) -> Enrollment:
    student = Student.objects.filter(id=data.student_id).first()
    if not student:
        raise NotFoundError("Siswa tidak ditemukan.")

    school_class = SchoolClass.objects.filter(id=data.class_id).first()
    if not school_class:
        raise NotFoundError("Kelas tidak ditemukan.")

    # Prevent overlapping active enrollment
    active_enr = Enrollment.objects.filter(student=student, end_date__isnull=True).first()
    if active_enr:
        raise BusinessValidationError("Siswa sudah memiliki penempatan kelas aktif.")

    enr = Enrollment.objects.create(
        student=student,
        school_class=school_class,
        start_date=data.start_date,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_ENROLLMENT",
        resource_type="master_data",
        resource_id=str(enr.id),
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return enr


@transaction.atomic
def update_enrollment(enrollment_id: int, data: EnrollmentUpdateRequest, actor: User) -> Enrollment:
    enr = Enrollment.objects.select_related("student", "school_class").filter(id=enrollment_id).first()
    if not enr:
        raise NotFoundError("Data penempatan tidak ditemukan.")

    if data.end_date is not None:
        if data.end_date < enr.start_date:
            raise BusinessValidationError("Tanggal selesai penempatan tidak boleh mendahului tanggal mulai.")
        enr.end_date = data.end_date

    enr.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_ENROLLMENT",
        resource_type="master_data",
        resource_id=str(enr.id),
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return enr


@transaction.atomic
def cancel_enrollment(enrollment_id: int, actor: User):
    enr = Enrollment.objects.filter(id=enrollment_id).first()
    if not enr:
        raise NotFoundError("Data penempatan tidak ditemukan.")

    enr_id = enr.id
    enr.delete()
    ActivityLog.objects.create(
        actor=actor,
        action="CANCEL_ENROLLMENT",
        resource_type="master_data",
        resource_id=str(enr_id),
    )
    transaction.on_commit(invalidate_dashboard_cache)


# Class Assignment Services
@transaction.atomic
def create_assignment(data: ClassAssignmentCreateRequest, actor: User) -> ClassAssignment:
    emp = Employee.objects.filter(id=data.employee_id).first()
    if not emp:
        raise NotFoundError("Pegawai tidak ditemukan.")

    school_class = SchoolClass.objects.filter(id=data.class_id).first()
    if not school_class:
        raise NotFoundError("Kelas tidak ditemukan.")

    # Check active duplicate assignment
    dup = ClassAssignment.objects.filter(
        employee=emp,
        school_class=school_class,
        role=data.role,
        end_date__isnull=True,
    ).first()
    if dup:
        raise BusinessValidationError("Penugasan aktif untuk peran dan kelas ini sudah ada.")

    asg = ClassAssignment.objects.create(
        employee=emp,
        school_class=school_class,
        role=data.role,
        start_date=data.start_date,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_ASSIGNMENT",
        resource_type="master_data",
        resource_id=str(asg.id),
    )
    return asg


@transaction.atomic
def update_assignment(assignment_id: int, data: ClassAssignmentUpdateRequest, actor: User) -> ClassAssignment:
    asg = ClassAssignment.objects.select_related("employee", "school_class").filter(id=assignment_id).first()
    if not asg:
        raise NotFoundError("Penugasan tidak ditemukan.")

    if data.end_date is not None:
        if data.end_date < asg.start_date:
            raise BusinessValidationError("Tanggal akhir penugasan tidak boleh mendahului tanggal mulai.")
        asg.end_date = data.end_date

    asg.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_ASSIGNMENT",
        resource_type="master_data",
        resource_id=str(asg.id),
    )
    return asg


@transaction.atomic
def cancel_assignment(assignment_id: int, actor: User):
    asg = ClassAssignment.objects.filter(id=assignment_id).first()
    if not asg:
        raise NotFoundError("Penugasan tidak ditemukan.")

    asg_id = asg.id
    asg.delete()
    ActivityLog.objects.create(
        actor=actor,
        action="CANCEL_ASSIGNMENT",
        resource_type="master_data",
        resource_id=str(asg_id),
    )
