"""
Deterministic Seeder for Full System Integration Testing
Populates roles, users, employees, academic years, classes, students, enrollments,
assignments, and service types into the target database (SQLite or PostgreSQL).
"""
import os
import sys
from datetime import date
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.accounts.models import Role, User, UserRole
from apps.master_data.models import (
    AcademicYear,
    SchoolClass,
    Employee,
    Student,
    Enrollment,
    ClassAssignment,
)
from apps.administration.models import ServiceType
from django.db import transaction


def seed_database():
    with transaction.atomic():
        print("--- Seeding Roles ---")
        roles = {
            "Administrator": Role.objects.get_or_create(name="Administrator")[0],
            "Guru": Role.objects.get_or_create(name="Guru")[0],
            "Wali Kelas": Role.objects.get_or_create(name="Wali Kelas")[0],
            "Kesiswaan": Role.objects.get_or_create(name="Kesiswaan")[0],
            "Tata Usaha": Role.objects.get_or_create(name="Tata Usaha")[0],
            "Pimpinan": Role.objects.get_or_create(name="Pimpinan")[0],
        }
        for name, role in roles.items():
            print(f"Role: {role.name} (id={role.id})")

        print("--- Seeding Users ---")
        user_specs = [
            ("admin", "Administrator"),
            ("guru", "Guru"),
            ("wali_kelas", "Wali Kelas"),
            ("kesiswaan", "Kesiswaan"),
            ("tata_usaha", "Tata Usaha"),
            ("kepsek", "Pimpinan"),
        ]

        users = {}
        for username, role_name in user_specs:
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    password="Password123!",
                    is_active=True,
                )
            else:
                user.set_password("Password123!")
                user.is_active = True
                user.save()

            UserRole.objects.get_or_create(user=user, role=roles[role_name])
            users[username] = user
            print(f"User: {username} -> {role_name}")

        print("--- Seeding Employees ---")
        emp_specs = [
            ("guru", "198501012010011001", "Ahmad Dahlan, S.Pd."),
            ("wali_kelas", "198602022011012002", "Siti Nurhaliza, M.Pd."),
            ("kesiswaan", "198703032012011003", "Budi Santoso, S.Pd."),
            ("tata_usaha", "198804042013011004", "Dewi Lestari, S.AP."),
            ("kepsek", "197505051999031005", "Dr. H. Sulaiman, M.Pd."),
        ]
        employees = {}
        for username, nip, name in emp_specs:
            u = users[username]
            emp, created = Employee.objects.get_or_create(
                user=u,
                defaults={"nip": nip, "name": name},
            )
            if not created:
                emp.nip = nip
                emp.name = name
                emp.save()
            employees[username] = emp
            print(f"Employee: {emp.name} ({emp.nip})")

        print("--- Seeding Academic Year ---")
        # Ensure only 1 active academic year
        AcademicYear.objects.all().update(is_active=False)
        ay, _ = AcademicYear.objects.get_or_create(
            name="2026/2027 Ganjil",
            defaults={
                "start_date": date(2026, 7, 1),
                "end_date": date(2026, 12, 31),
                "is_active": True,
            },
        )
        ay.is_active = True
        ay.save()
        print(f"Academic Year: {ay.name} (active={ay.is_active})")

        print("--- Seeding Classes ---")
        class_xi, _ = SchoolClass.objects.get_or_create(
            academic_year=ay,
            name="XI-MIPA-1",
            defaults={"level": 11},
        )
        print(f"Class: {class_xi.name} (level={class_xi.level})")

        print("--- Seeding Students ---")
        student_data = [
            ("NISN001", "Aditya Pratama", "LAKI_LAKI"),
            ("NISN002", "Bella Safitri", "PEREMPUAN"),
            ("NISN003", "Cahyo Utomo", "LAKI_LAKI"),
            ("NISN004", "Dinda Maharani", "PEREMPUAN"),
            ("NISN005", "Eko Prasetyo", "LAKI_LAKI"),
        ]
        students = []
        for sn, name, gender in student_data:
            st, _ = Student.objects.get_or_create(
                student_number=sn,
                defaults={"name": name, "gender": gender, "status": "AKTIF"},
            )
            st.name = name
            st.gender = gender
            st.status = "AKTIF"
            st.save()
            students.append(st)
            print(f"Student: {st.name} ({st.student_number})")

        print("--- Seeding Enrollments ---")
        for st in students:
            Enrollment.objects.get_or_create(
                student=st,
                school_class=class_xi,
                defaults={"start_date": date(2026, 7, 1)},
            )
        print(f"Enrolled {len(students)} students in {class_xi.name}")

        print("--- Seeding Class Assignments ---")
        # Guru Mapel
        ClassAssignment.objects.get_or_create(
            employee=employees["guru"],
            school_class=class_xi,
            role="GURU_MAPEL",
            defaults={"start_date": date(2026, 7, 1)},
        )
        # Wali Kelas
        ClassAssignment.objects.get_or_create(
            employee=employees["wali_kelas"],
            school_class=class_xi,
            role="WALI_KELAS",
            defaults={"start_date": date(2026, 7, 1)},
        )
        print("Class assignments created for Guru and Wali Kelas")

        print("--- Seeding Service Types ---")
        st_data = [
            ("SK-AKTIF", "Surat Keterangan Siswa Aktif", True),
            ("SK-LULUS", "Surat Keterangan Lulus (SKL)", True),
            ("LEGALISIR", "Legalisasi Dokumen Ijazah / Rapor", False),
        ]
        for code, name, req_app in st_data:
            stype, _ = ServiceType.objects.get_or_create(
                code=code,
                defaults={"name": name, "requires_approval": req_app, "is_active": True},
            )
            stype.name = name
            stype.requires_approval = req_app
            stype.is_active = True
            stype.save()
            print(f"Service Type: {stype.code} - {stype.name}")

    print("=== SEEDING COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    seed_database()
