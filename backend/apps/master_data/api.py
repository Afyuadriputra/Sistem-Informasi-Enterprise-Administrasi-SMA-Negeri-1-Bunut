from typing import Optional

from django.http import HttpRequest
from ninja import Query, Router
from ninja.responses import Response

from apps.core.schemas import SuccessMessageResponse
from apps.core.security import jwt_auth, require_roles
from apps.master_data.schemas import (
    AcademicYearCreateRequest,
    AcademicYearItem,
    AcademicYearListResponse,
    AcademicYearUpdateRequest,
    ClassAssignmentCreateRequest,
    ClassAssignmentItem,
    ClassAssignmentListResponse,
    ClassAssignmentUpdateRequest,
    ClassCreateRequest,
    ClassItem,
    ClassListResponse,
    ClassUpdateRequest,
    EmployeeCreateRequest,
    EmployeeItem,
    EmployeeListResponse,
    EmployeeUpdateRequest,
    EnrollmentCreateRequest,
    EnrollmentItem,
    EnrollmentListResponse,
    EnrollmentUpdateRequest,
    StudentCreateRequest,
    StudentItem,
    StudentListResponse,
    StudentUpdateRequest,
)
from apps.master_data.selectors import (
    get_academic_year,
    get_class,
    get_employee,
    get_student,
    list_academic_years,
    list_assignments,
    list_classes,
    list_employees,
    list_enrollments,
    list_students,
)
from apps.master_data.services import (
    cancel_assignment,
    cancel_enrollment,
    create_academic_year,
    create_assignment,
    create_employee,
    create_enrollment,
    create_school_class,
    create_student,
    update_academic_year,
    update_assignment,
    update_employee,
    update_enrollment,
    update_school_class,
    update_student,
)

master_router = Router(tags=["Master Data"], auth=jwt_auth)


# --- Academic Years ---
@master_router.get("/academic-years", response={200: AcademicYearListResponse}, operation_id="listAcademicYears")
def get_academic_years(
    request: HttpRequest,
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_academic_years(search=search, is_active=is_active, page=page, page_size=page_size)


@master_router.post("/academic-years", response={201: AcademicYearItem}, operation_id="createAcademicYear")
def post_academic_year(request: HttpRequest, payload: AcademicYearCreateRequest):
    require_roles(request.user, ["Administrator"])
    ay = create_academic_year(payload, actor=request.user)
    return Response(get_academic_year(ay.id).model_dump(), status=201)


@master_router.get("/academic-years/{id}", response={200: AcademicYearItem}, operation_id="getAcademicYearDetail")
def get_academic_year_detail(request: HttpRequest, id: int):
    return get_academic_year(id)


@master_router.patch("/academic-years/{id}", response={200: AcademicYearItem}, operation_id="updateAcademicYear")
def patch_academic_year(request: HttpRequest, id: int, payload: AcademicYearUpdateRequest):
    require_roles(request.user, ["Administrator"])
    update_academic_year(id, payload, actor=request.user)
    return get_academic_year(id)


# --- School Classes ---
@master_router.get("/classes", response={200: ClassListResponse}, operation_id="listClasses")
def get_classes(
    request: HttpRequest,
    academic_year_id: Optional[int] = Query(None),
    level: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_classes(
        academic_year_id=academic_year_id,
        level=level,
        search=search,
        page=page,
        page_size=page_size,
    )


@master_router.post("/classes", response={201: ClassItem}, operation_id="createClass")
def post_class(request: HttpRequest, payload: ClassCreateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    cls = create_school_class(payload, actor=request.user)
    return Response(get_class(cls.id).model_dump(), status=201)


@master_router.get("/classes/{id}", response={200: ClassItem}, operation_id="getClassDetail")
def get_class_detail(request: HttpRequest, id: int):
    return get_class(id)


@master_router.patch("/classes/{id}", response={200: ClassItem}, operation_id="updateClass")
def patch_class(request: HttpRequest, id: int, payload: ClassUpdateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    update_school_class(id, payload, actor=request.user)
    return get_class(id)


# --- Employees ---
@master_router.get("/employees", response={200: EmployeeListResponse}, operation_id="listEmployees")
def get_employees(
    request: HttpRequest,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_employees(status=status, search=search, page=page, page_size=page_size)


@master_router.post("/employees", response={201: EmployeeItem}, operation_id="createEmployee")
def post_employee(request: HttpRequest, payload: EmployeeCreateRequest):
    require_roles(request.user, ["Administrator"])
    emp = create_employee(payload, actor=request.user)
    return Response(get_employee(emp.id).model_dump(), status=201)


@master_router.get("/employees/{id}", response={200: EmployeeItem}, operation_id="getEmployeeDetail")
def get_employee_detail(request: HttpRequest, id: int):
    return get_employee(id)


@master_router.patch("/employees/{id}", response={200: EmployeeItem}, operation_id="updateEmployee")
def patch_employee(request: HttpRequest, id: int, payload: EmployeeUpdateRequest):
    require_roles(request.user, ["Administrator"])
    update_employee(id, payload, actor=request.user)
    return get_employee(id)


# --- Students ---
@master_router.get("/students", response={200: StudentListResponse}, operation_id="listStudents")
def get_students(
    request: HttpRequest,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    class_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_students(status=status, search=search, class_id=class_id, page=page, page_size=page_size)


@master_router.post("/students", response={201: StudentItem}, operation_id="createStudent")
def post_student(request: HttpRequest, payload: StudentCreateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    student = create_student(payload, actor=request.user)
    return Response(get_student(student.id).model_dump(), status=201)


@master_router.get("/students/{id}", response={200: StudentItem}, operation_id="getStudentDetail")
def get_student_detail(request: HttpRequest, id: int):
    return get_student(id)


@master_router.patch("/students/{id}", response={200: StudentItem}, operation_id="updateStudent")
def patch_student(request: HttpRequest, id: int, payload: StudentUpdateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    update_student(id, payload, actor=request.user)
    return get_student(id)


# --- Enrollments ---
@master_router.get("/enrollments", response={200: EnrollmentListResponse}, operation_id="listEnrollments")
def get_enrollments(
    request: HttpRequest,
    class_id: Optional[int] = Query(None),
    student_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_enrollments(
        class_id=class_id,
        student_id=student_id,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@master_router.post("/enrollments", response={201: EnrollmentItem}, operation_id="createEnrollment")
def post_enrollment(request: HttpRequest, payload: EnrollmentCreateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    enr = create_enrollment(payload, actor=request.user)
    return Response(
        EnrollmentItem(
            id=enr.id,
            student_id=enr.student_id,
            student_name=enr.student.name,
            student_number=enr.student.student_number,
            class_id=enr.school_class_id,
            class_name=enr.school_class.name,
            start_date=enr.start_date,
            end_date=enr.end_date,
        ).model_dump(),
        status=201,
    )


@master_router.patch("/enrollments/{id}", response={200: EnrollmentItem}, operation_id="updateEnrollment")
def patch_enrollment(request: HttpRequest, id: int, payload: EnrollmentUpdateRequest):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    enr = update_enrollment(id, payload, actor=request.user)
    return EnrollmentItem(
        id=enr.id,
        student_id=enr.student_id,
        student_name=enr.student.name,
        student_number=enr.student.student_number,
        class_id=enr.school_class_id,
        class_name=enr.school_class.name,
        start_date=enr.start_date,
        end_date=enr.end_date,
    )


@master_router.delete("/enrollments/{id}", response={200: SuccessMessageResponse}, operation_id="cancelEnrollment")
def delete_enrollment(request: HttpRequest, id: int):
    require_roles(request.user, ["Administrator", "Tata Usaha"])
    cancel_enrollment(id, actor=request.user)
    return SuccessMessageResponse(message="Penempatan siswa berhasil dibatalkan.")


# --- Class Assignments ---
@master_router.get("/assignments", response={200: ClassAssignmentListResponse}, operation_id="listClassAssignments")
def get_assignments(
    request: HttpRequest,
    class_id: Optional[int] = Query(None),
    employee_id: Optional[int] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_assignments(
        class_id=class_id,
        employee_id=employee_id,
        role=role,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@master_router.post("/assignments", response={201: ClassAssignmentItem}, operation_id="createClassAssignment")
def post_assignment(request: HttpRequest, payload: ClassAssignmentCreateRequest):
    require_roles(request.user, ["Administrator"])
    asg = create_assignment(payload, actor=request.user)
    return Response(
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
        ).model_dump(),
        status=201,
    )


@master_router.patch("/assignments/{id}", response={200: ClassAssignmentItem}, operation_id="updateClassAssignment")
def patch_assignment(request: HttpRequest, id: int, payload: ClassAssignmentUpdateRequest):
    require_roles(request.user, ["Administrator"])
    asg = update_assignment(id, payload, actor=request.user)
    return ClassAssignmentItem(
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


@master_router.delete("/assignments/{id}", response={200: SuccessMessageResponse}, operation_id="cancelAssignment")
def delete_assignment(request: HttpRequest, id: int):
    require_roles(request.user, ["Administrator"])
    cancel_assignment(id, actor=request.user)
    return SuccessMessageResponse(message="Penugasan guru berhasil dibatalkan.")
