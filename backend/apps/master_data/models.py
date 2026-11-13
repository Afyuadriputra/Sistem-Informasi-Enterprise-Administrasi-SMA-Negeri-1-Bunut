from django.conf import settings
from django.db import models


class GenderEnum(models.TextChoices):
    LAKI_LAKI = "LAKI_LAKI", "Laki-laki"
    PEREMPUAN = "PEREMPUAN", "Perempuan"


class StudentStatusEnum(models.TextChoices):
    AKTIF = "AKTIF", "Siswa aktif terdaftar"
    MUTASI_KELUAR = "MUTASI_KELUAR", "Siswa pindah sekolah"
    LULUS = "LULUS", "Siswa telah tamat"
    NONAKTIF = "NONAKTIF", "Siswa nonaktif/cuti"


class EmployeeStatusEnum(models.TextChoices):
    AKTIF = "AKTIF", "Pegawai/guru aktif bertugas"
    CUTI = "CUTI", "Sedang cuti resmi"
    NONAKTIF = "NONAKTIF", "Pensiun/pindah tugas"


class ClassAssignmentRoleEnum(models.TextChoices):
    GURU_MAPEL = "GURU_MAPEL", "Guru pengampu mata pelajaran"
    WALI_KELAS = "WALI_KELAS", "Wali kelas penanggung jawab rombel"


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
        db_column="user_id",
    )
    nip = models.CharField(max_length=30, unique=True, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=EmployeeStatusEnum.choices, default=EmployeeStatusEnum.AKTIF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees"

    def __str__(self):
        return f"{self.name} ({self.nip or '-'})"


class AcademicYear(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "academic_years"

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name="classes", db_column="academic_year_id"
    )
    name = models.CharField(max_length=50)
    level = models.IntegerField()  # 10, 11, or 12
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "school_classes"
        unique_together = (("academic_year", "name"),)

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"


class Student(models.Model):
    student_number = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
    gender = models.CharField(max_length=20, choices=GenderEnum.choices)
    status = models.CharField(
        max_length=20,
        choices=StudentStatusEnum.choices,
        default=StudentStatusEnum.AKTIF,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students"

    @property
    def full_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} ({self.student_number})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments", db_column="student_id")
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="enrollments", db_column="class_id"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "enrollments"
        indexes = [
            models.Index(fields=["student", "school_class", "start_date"], name="idx_enr_std_cls"),
            models.Index(fields=["school_class", "start_date", "end_date"], name="idx_enr_cls_per"),
        ]

    def __str__(self):
        return f"{self.student.name} -> {self.school_class.name}"


class ClassAssignment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="assignments", db_column="employee_id"
    )
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="assignments", db_column="class_id"
    )
    role = models.CharField(
        max_length=20,
        choices=ClassAssignmentRoleEnum.choices,
        default=ClassAssignmentRoleEnum.GURU_MAPEL,
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "class_assignments"
        indexes = [
            models.Index(fields=["employee", "school_class", "role"], name="idx_asg_emp_cls"),
            models.Index(fields=["school_class", "role"], name="idx_asg_cls_role"),
        ]

    def __str__(self):
        return f"{self.employee.name} as {self.role} in {self.school_class.name}"
