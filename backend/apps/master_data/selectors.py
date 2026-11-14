from typing import Optional

from apps.core.exceptions import NotFoundError
from apps.core.pagination import paginate_queryset
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.master_data.schemas import (
    AcademicYearItem,
    AcademicYearListResponse,
    ClassAssignmentItem,
    ClassAssignmentListResponse,
    ClassItem,
    ClassListResponse,
    EmployeeItem,
    EmployeeListResponse,
    EnrollmentItem,
    EnrollmentListResponse,
    StudentItem,
    StudentListResponse,
)


def list_academic_years(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
) -> AcademicYearListResponse:
    qs = AcademicYear.objects.order_by("-start_date", "-id")
    if search:
        qs = qs.filter(name__icontains=search)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)
    items = [
        AcademicYearItem(
            id=y.id,
            name=y.name,
            start_date=y.start_date,
            end_date=y.end_date,
            is_active=y.is_active,
        )
        for y in paginated["items"]
    ]
    return AcademicYearListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_academic_year(year_id: int) -> AcademicYearItem:
    ay = AcademicYear.objects.filter(id=year_id).first()
    if not ay:
        raise NotFoundError("Tahun ajaran tidak ditemukan.")
    return AcademicYearItem(
        id=ay.id,
        name=ay.name,
        start_date=ay.start_date,
        end_date=ay.end_date,
        is_active=ay.is_active,
    )


def list_classes(
    academic_year_id: Optional[int] = None,
    level: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> ClassListResponse:
    qs = SchoolClass.objects.select_related("academic_year").order_by("-academic_year__is_active", "level", "name")
    if academic_year_id:
        qs = qs.filter(academic_year_id=academic_year_id)
    if level:
        qs = qs.filter(level=level)
    if search:
        qs = qs.filter(name__icontains=search)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)
    items = [
        ClassItem(
            id=c.id,
            academic_year_id=c.academic_year_id,
            academic_year_name=c.academic_year.name,
            name=c.name,
            level=c.level,
        )
        for c in paginated["items"]
    ]
    return ClassListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_class(class_id: int) -> ClassItem:
    cls = SchoolClass.objects.select_related("academic_year").filter(id=class_id).first()
    if not cls:
        raise NotFoundError("Kelas tidak ditemukan.")
    return ClassItem(
        id=cls.id,
        academic_year_id=cls.academic_year_id,
        academic_year_name=cls.academic_year.name,
        name=cls.name,
        level=cls.level,
    )


def list_employees(
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> EmployeeListResponse:
    qs = Employee.objects.order_by("name")
    if status:
        qs = qs.filter(status=status)
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(nip__icontains=search)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)
    items = [
        EmployeeItem(
            id=e.id,
            user_id=e.user_id,
            nip=e.nip,
            name=e.name,
            phone=e.phone,
            status=e.status,
            created_at=e.created_at,
        )
        for e in paginated["items"]
    ]
    return EmployeeListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_employee(employee_id: int) -> EmployeeItem:
    emp = Employee.objects.filter(id=employee_id).first()
    if not emp:
        raise NotFoundError("Pegawai tidak ditemukan.")
    return EmployeeItem(
        id=emp.id,
        user_id=emp.user_id,
        nip=emp.nip,
        name=emp.name,
        phone=emp.phone,
        status=emp.status,
        created_at=emp.created_at,
    )


def list_students(
    status: Optional[str] = None,
    search: Optional[str] = None,
    class_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
) -> StudentListResponse:
    qs = Student.objects.order_by("name")
    if status:
        qs = qs.filter(status=status)
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(student_number__icontains=search)
    if class_id:
        qs = qs.filter(enrollments__school_class_id=class_id, enrollments__end_date__isnull=True)

    paginated = paginate_queryset(qs.distinct(), page=page, page_size=page_size)
    items = [
        StudentItem(
            id=s.id,
            student_number=s.student_number,
            name=s.name,
            gender=s.gender,
            status=s.status,
        )
        for s in paginated["items"]
    ]
    return StudentListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_student(student_id: int) -> StudentItem:
    student = Student.objects.filter(id=student_id).first()
    if not student:
        raise NotFoundError("Data siswa tidak ditemukan.")
    return StudentItem(
        id=student.id,
        student_number=student.student_number,
        name=student.name,
        gender=student.gender,
        status=student.status,
    )


def list_enrollments(
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
) -> EnrollmentListResponse:
    if class_id is not None and page_size == 20:
        page_size = 100
    qs = Enrollment.objects.select_related("student", "school_class").order_by("-start_date")
    if class_id:
        qs = qs.filter(school_class_id=class_id)
    if student_id:
        qs = qs.filter(student_id=student_id)
    if is_active is not None:
        if is_active:
            qs = qs.filter(end_date__isnull=True)
        else:
            qs = qs.filter(end_date__isnull=False)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)
    items = [
        EnrollmentItem(
            id=enr.id,
            student_id=enr.student_id,
            student_name=enr.student.name,
            student_number=enr.student.student_number,
            class_id=enr.school_class_id,
            class_name=enr.school_class.name,
            start_date=enr.start_date,
            end_date=enr.end_date,
        )
        for enr in paginated["items"]
    ]
    return EnrollmentListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def list_assignments(
    class_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
) -> ClassAssignmentListResponse:
    qs = ClassAssignment.objects.select_related("employee", "school_class").order_by("-start_date")
    if class_id:
        qs = qs.filter(school_class_id=class_id)
    if employee_id:
        qs = qs.filter(employee_id=employee_id)
    if role:
        qs = qs.filter(role=role)
    if is_active is not None:
        if is_active:
            qs = qs.filter(end_date__isnull=True)
        else:
            qs = qs.filter(end_date__isnull=False)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)
    items = [
        ClassAssignmentItem(
            id=asg.id,
            employee_id=asg.employee_id,
            employee_name=asg.employee.name,
            employee_nip=asg.employee.nip,
            class_id=asg.school_class_id,
            class_name=asg.school_class.name,
            role=asg.role,
            start_date=asg.start_date,
            end_date=asg.end_date,
        )
        for asg in paginated["items"]
    ]
    return ClassAssignmentListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )
