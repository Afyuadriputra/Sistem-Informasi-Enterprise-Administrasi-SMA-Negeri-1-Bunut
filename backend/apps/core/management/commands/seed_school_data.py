import io
import os
import random
import time
import uuid
from datetime import date, timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from simple_history.utils import bulk_create_with_history

from apps.accounts.models import ActivityLog, Role, User, UserRole
from apps.administration.models import (
    Document,
    ServiceActionEnum,
    ServiceEvent,
    ServiceRequest,
    ServiceRequestStatusEnum,
    ServiceType,
)
from apps.attendance.models import Attendance, AttendanceStatusEnum
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    ClassAssignmentRoleEnum,
    Employee,
    EmployeeStatusEnum,
    Enrollment,
    GenderEnum,
    SchoolClass,
    Student,
    StudentStatusEnum,
)
from apps.student_affairs.models import (
    CaseActionEnum,
    CaseEvent,
    CaseStatusEnum,
    StudentCase,
)


class Command(BaseCommand):
    help = "Seed realistic, interconnected operational school data using Faker Indonesia."

    def add_arguments(self, parser):
        parser.add_argument(
            "--profile",
            type=str,
            choices=["small", "full"],
            default="full",
            help="Seeding profile size: 'small' for quick test suites or 'full' for local demonstration (default: full).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=42,
            help="Deterministic random seed value (default: 42).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate and print the planned database seeding without committing mutations.",
        )
        parser.add_argument(
            "--role-passwords",
            action="store_true",
            help="Use distinct role passwords (e.g. Admin123!, Guru123!) instead of uniform Password123!.",
        )
        parser.add_argument("--students", type=int, default=None, help="Explicit active students count override.")
        parser.add_argument("--employees", type=int, default=None, help="Explicit employee count override.")
        parser.add_argument("--classes", type=int, default=None, help="Explicit active classes count override.")
        parser.add_argument("--academic-years", type=int, default=None, help="Explicit academic year count override.")
        parser.add_argument(
            "--attendance-days", type=int, default=None, help="Explicit historical attendance days count override."
        )
        parser.add_argument("--cases", type=int, default=None, help="Explicit student cases count override.")
        parser.add_argument(
            "--requests", type=int, default=None, help="Explicit administration service requests count override."
        )

    def handle(self, *args, **options):
        # 1. Preflight Safety Check: Fail-fast against production environment
        django_env = getattr(settings, "DJANGO_ENV", os.environ.get("DJANGO_ENV", "development")).lower()
        if django_env == "production":
            raise CommandError(
                "ERROR: Seeder dilarang keras dijalankan pada environment 'production'! "
                "Perintah ini hanya diizinkan pada environment development atau integration."
            )

        start_time = time.time()
        profile = options["profile"]
        seed_value = options["seed"]
        dry_run = options["dry_run"]

        # Initialize RNGs
        rng = random.Random(seed_value)
        fake = Faker("id_ID")
        Faker.seed(seed_value)

        # Profile parameters
        if profile == "small":
            active_classes_count = options["classes"] or 2
            students_per_class = 10
            total_active_students = options["students"] or (active_classes_count * students_per_class)
            total_employees = options["employees"] or 10
            academic_years_count = options["academic_years"] or 2
            attendance_days_count = options["attendance_days"] or 5
            total_cases = options["cases"] or 6
            total_requests = options["requests"] or 12
            total_documents = 8
        else:
            active_classes_count = options["classes"] or 12
            students_per_class = 36
            total_active_students = options["students"] or (active_classes_count * students_per_class)  # 432
            total_employees = options["employees"] or 40
            academic_years_count = options["academic_years"] or 3
            attendance_days_count = options["attendance_days"] or 75
            total_cases = options["cases"] or 60
            total_requests = options["requests"] or 150
            total_documents = 120

        self.stdout.write(
            self.style.MIGRATE_HEADING("=== SISTEM INFORMASI ENTERPRISE SMAN 1 BUNUT - DATABASE SEEDER ===")
        )
        self.stdout.write(f"Environment aktif : {django_env}")
        self.stdout.write(f"Database engine   : {settings.DATABASES['default']['ENGINE']}")
        self.stdout.write(f"Database name     : {settings.DATABASES['default'].get('NAME', 'N/A')}")
        self.stdout.write(f"Private media     : {settings.PRIVATE_MEDIA_ROOT}")
        self.stdout.write(f"Seeding profile   : {profile.upper()} (seed={seed_value}, dry_run={dry_run})")
        self.stdout.write("--------------------------------------------------------------------------------")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE: Rencana populasi data tanpa mutasi basis data:"))
            self.stdout.write(" - Peran (Roles)               : 6")
            self.stdout.write(f" - Pegawai (Employees)         : {total_employees}")
            self.stdout.write(f" - Pengguna (Users)            : {total_employees}")
            self.stdout.write(f" - Tahun Ajaran (AcademicYears): {academic_years_count} (1 aktif)")
            self.stdout.write(f" - Rombel (SchoolClasses)      : {active_classes_count * academic_years_count}")
            self.stdout.write(f" - Siswa Aktif (Students)      : {total_active_students}")
            self.stdout.write(f" - Penugasan Guru              : {active_classes_count * 2}")
            self.stdout.write(f" - Hari Presensi Historis      : {attendance_days_count} hari")
            self.stdout.write(
                f" - Estimasi Rekor Presensi     : ~{total_active_students * attendance_days_count} baris"
            )
            self.stdout.write(f" - Kasus Kesiswaan             : {total_cases}")
            self.stdout.write(f" - Permohonan Persuratan       : {total_requests}")
            self.stdout.write(f" - Dokumen Privat Fisik        : {total_documents}")
            self.stdout.write(self.style.SUCCESS("Dry run selesai. Tidak ada data yang diubah."))
            return

        # Execution tracking metrics
        metrics = {
            "roles": 0,
            "users": 0,
            "employees": 0,
            "academic_years": 0,
            "classes": 0,
            "students": 0,
            "enrollments": 0,
            "assignments": 0,
            "attendance": 0,
            "cases": 0,
            "case_events": 0,
            "service_types": 0,
            "service_requests": 0,
            "service_events": 0,
            "documents": 0,
            "activity_logs": 0,
        }

        # [01/12] Memeriksa environment & target basis data
        self.stdout.write("[01/12] Memeriksa environment & target basis data... OK")

        # [02/12] Menyiapkan peran sistem (Roles)
        self.stdout.write("[02/12] Menyiapkan peran sistem (Roles)...")
        role_definitions = [
            ("Administrator", "Administrator sistem dengan wewenang master data dan manajemen pengguna"),
            ("Guru", "Guru pengampu mata pelajaran dengan hak input dan rekap presensi kelas penugasan"),
            ("Wali Kelas", "Wali kelas penanggung jawab rombongan belajar dan pemantauan siswa binaan"),
            ("Kesiswaan", "Staf kesiswaan dan guru BK penanggung jawab pembinaan dan kasus siswa"),
            ("Tata Usaha", "Staf administrasi dan tata usaha penanggung jawab layanan persuratan"),
            ("Pimpinan", "Kepala Sekolah / Pimpinan dengan hak persetujuan disposisi dan pemantauan eksekutif"),
        ]
        roles = {}
        for role_name, role_desc in role_definitions:
            r, created = Role.objects.get_or_create(name=role_name, defaults={"description": role_desc})
            roles[role_name] = r
            if created:
                metrics["roles"] += 1
        self.stdout.write(f"        -> 6 Peran terverifikasi ({metrics['roles']} dibuat baru).")

        # [03/12] Menyiapkan tahun ajaran akademik (Academic Years)
        self.stdout.write("[03/12] Menyiapkan tahun ajaran akademik (Academic Years)...")
        # Ensure exactly one active year: 2026/2027
        ay_specs = [
            ("2024/2025", date(2024, 7, 15), date(2025, 6, 20), False),
            ("2025/2026", date(2025, 7, 14), date(2026, 6, 19), False),
            ("2026/2027", date(2026, 7, 13), date(2027, 6, 18), True),
        ]
        if academic_years_count == 2:
            ay_specs = ay_specs[1:]

        academic_years = {}
        for ay_name, s_date, e_date, is_act in ay_specs:
            ay, created = AcademicYear.objects.get_or_create(
                name=ay_name,
                defaults={"start_date": s_date, "end_date": e_date, "is_active": is_act},
            )
            if not created:
                ay.start_date = s_date
                ay.end_date = e_date
                ay.is_active = is_act
                ay.save()
            academic_years[ay_name] = ay
            if created:
                metrics["academic_years"] += 1
        # Explicit guarantee: exactly 1 active year
        AcademicYear.objects.exclude(name="2026/2027").update(is_active=False)
        active_ay = academic_years["2026/2027"]
        active_ay.is_active = True
        active_ay.save()
        self.stdout.write(f"        -> {len(academic_years)} Tahun ajaran siap (Aktif: {active_ay.name}).")

        # [04/12] Membuat rombongan belajar (School Classes)
        self.stdout.write("[04/12] Membuat rombongan belajar (School Classes)...")
        # Class template: 12 classes per academic year (X-1..4, XI-1..4, XII-1..4)
        active_class_names = [
            ("X-1", 10),
            ("X-2", 10),
            ("X-3", 10),
            ("X-4", 10),
            ("XI-MIPA-1", 11),
            ("XI-2", 11),
            ("XI-3", 11),
            ("XI-4", 11),
            ("XII-1", 12),
            ("XII-2", 12),
            ("XII-3", 12),
            ("XII-4", 12),
        ]
        if profile == "small":
            active_class_names = [("X-1", 10), ("XI-MIPA-1", 11)]

        classes_by_year = {}
        for ay_name, ay_obj in academic_years.items():
            classes_by_year[ay_name] = []
            for c_name, c_level in active_class_names:
                sc, created = SchoolClass.objects.get_or_create(
                    academic_year=ay_obj,
                    name=c_name,
                    defaults={"level": c_level},
                )
                classes_by_year[ay_name].append(sc)
                if created:
                    metrics["classes"] += 1
        self.stdout.write(f"        -> {sum(len(v) for v in classes_by_year.values())} Kelas rombel terdaftar.")

        # [05/12] & [06/12] Membuat pegawai, akun pengguna & penugasan RBAC
        self.stdout.write("[05/12 & 06/12] Membuat profil pegawai, akun pengguna & RBAC...")
        # Core 7 test accounts specifications:
        # Username, Role Name, Simple Local Password, Full Name, NIP, Phone
        core_account_specs = [
            ("admin", "Administrator", "Admin123!", "Rizky Firmansyah, S.Kom.", "199001012015011001", "081234567801"),
            ("guru", "Guru", "Guru123!", "Ahmad Dahlan, S.Pd.", "198501012010011001", "081234567802"),
            ("wali_kelas", "Wali Kelas", "Wali123!", "Siti Nurhaliza, M.Pd.", "198602022011012002", "081234567803"),
            ("kesiswaan", "Kesiswaan", "Kesiswaan123!", "Budi Santoso, S.Pd.", "198703032012011003", "081234567804"),
            ("tata_usaha", "Tata Usaha", "TataUsaha123!", "Dewi Lestari, S.AP.", "198804042013011004", "081234567805"),
            ("kepsek", "Pimpinan", "Kepsek123!", "Dr. H. Sulaiman, M.Pd.", "197505051999031005", "081234567806"),
            ("guru_walikelas", "Guru", "GuruWali123!", "Hendra Pratama, S.Pd.", "198906062014011006", "081234567807"),
        ]

        use_role_pwds = options.get("role_passwords", False)
        users = {}
        employees = {}

        for username, primary_role, role_pwd, full_name, nip, phone in core_account_specs:
            pwd = role_pwd if use_role_pwds else "Password123!"
            u = User.objects.filter(username=username).first()
            if not u:
                u = User.objects.create_user(username=username, password=pwd, is_active=True)
                metrics["users"] += 1
            else:
                u.set_password(pwd)
                u.is_active = True
                u.save()

            UserRole.objects.get_or_create(user=u, role=roles[primary_role])
            if username == "guru_walikelas":
                UserRole.objects.get_or_create(user=u, role=roles["Wali Kelas"])
            users[username] = u

            emp, created = Employee.objects.get_or_create(
                nip=nip,
                defaults={"name": full_name, "user": u, "phone": phone, "status": EmployeeStatusEnum.AKTIF},
            )
            if not created:
                emp.user = u
                emp.name = full_name
                emp.phone = phone
                emp.status = EmployeeStatusEnum.AKTIF
                emp.save()
            employees[username] = emp
            if created:
                metrics["employees"] += 1

        # Additional employees to reach target (40 total in full profile)
        extra_target = total_employees - len(core_account_specs)
        for i in range(1, extra_target + 1):
            extra_username = f"pegawai_{i:02d}"
            # Distribution: TU (3), Kesiswaan (2), Guru (remaining)
            if i <= 3:
                role_assigned = "Tata Usaha"
                title = "S.AP."
            elif i <= 5:
                role_assigned = "Kesiswaan"
                title = "S.Pd. (BK)"
            elif i <= 15:
                role_assigned = "Wali Kelas"
                title = "M.Pd."
            else:
                role_assigned = "Guru"
                title = "S.Pd."

            emp_name = f"{fake.name()}, {title}"
            nip_val = f"19{rng.randint(70, 98):02d}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}20{rng.randint(10, 24):02d}{rng.randint(1, 2):01d}{i:03d}"
            phone_val = f"08{rng.randint(11, 29)}{rng.randint(1000000, 9999999)}"

            u = User.objects.filter(username=extra_username).first()
            if not u:
                u = User.objects.create_user(username=extra_username, password="Password123!", is_active=True)
                metrics["users"] += 1
            else:
                u.set_password("Password123!")
                u.is_active = True
                u.save()

            UserRole.objects.get_or_create(user=u, role=roles[role_assigned])
            if role_assigned == "Wali Kelas":
                UserRole.objects.get_or_create(user=u, role=roles["Guru"])
            users[extra_username] = u

            emp, created = Employee.objects.get_or_create(
                nip=nip_val,
                defaults={"name": emp_name, "user": u, "phone": phone_val, "status": EmployeeStatusEnum.AKTIF},
            )
            employees[extra_username] = emp
            if created:
                metrics["employees"] += 1

        self.stdout.write(f"        -> {len(users)} Akun pengguna & {len(employees)} Pegawai siap.")

        # [07/12] Membuat data siswa & penempatan rombel (Students & Enrollments)
        self.stdout.write("[07/12] Membuat data siswa & penempatan rombel (Students & Enrollments)...")
        active_classes = classes_by_year["2026/2027"]
        all_active_students = []

        # Deterministic generation of active students per class
        for _cls_idx, s_class in enumerate(active_classes):
            for s_num in range(1, students_per_class + 1):
                clean_cls_name = s_class.name.replace("-", "").replace(" ", "")
                nis = f"26{clean_cls_name}{s_num:02d}"
                s_gender = GenderEnum.LAKI_LAKI if s_num % 2 == 1 else GenderEnum.PEREMPUAN
                if s_class.name == "XI-MIPA-1" and s_num == 1:
                    s_name = "Aditya Pratama"
                else:
                    raw_name = fake.name_male() if s_gender == GenderEnum.LAKI_LAKI else fake.name_female()
                    if raw_name <= "Aditya Pratama":
                        s_name = f"Budi {raw_name}"
                    else:
                        s_name = raw_name

                st, created = Student.objects.get_or_create(
                    student_number=nis,
                    defaults={"name": s_name, "gender": s_gender, "status": StudentStatusEnum.AKTIF},
                )
                if not created:
                    st.name = s_name
                    st.gender = s_gender
                    st.status = StudentStatusEnum.AKTIF
                    st.save()
                if created:
                    metrics["students"] += 1
                all_active_students.append(st)

                # Enrollment into this class starting 2026-07-13
                enr, enr_created = Enrollment.objects.get_or_create(
                    student=st,
                    school_class=s_class,
                    defaults={"start_date": active_ay.start_date, "end_date": None},
                )
                if enr_created:
                    metrics["enrollments"] += 1

        # Guarantee Aditya Pratama is strictly the first student alphabetically across all active students
        for early_st in (
            Student.objects.filter(status=StudentStatusEnum.AKTIF, name__lt="Aditya Pratama")
            .exclude(student_number="26XIMIPA101")
        ):
            early_st.name = f"Budi {early_st.name}"
            early_st.save()

        # Additional alumni & inactive students from previous years (full profile)
        if profile == "full" and "2025/2026" in classes_by_year:
            past_ay = classes_by_year["2025/2026"]
            # Alumni (telah lulus)
            for a_idx in range(1, 37):
                nis_alumni = f"23XII1{a_idx:02d}"
                st_alumni, created = Student.objects.get_or_create(
                    student_number=nis_alumni,
                    defaults={
                        "name": fake.name(),
                        "gender": GenderEnum.LAKI_LAKI if a_idx % 2 == 1 else GenderEnum.PEREMPUAN,
                        "status": StudentStatusEnum.LULUS,
                    },
                )
                if created:
                    metrics["students"] += 1
                # Enrolled in past year class with end_date
                Enrollment.objects.get_or_create(
                    student=st_alumni,
                    school_class=past_ay[-1],  # XII
                    defaults={"start_date": date(2025, 7, 14), "end_date": date(2026, 6, 19)},
                )
            # Mutasi keluar & nonaktif
            for m_idx in range(1, 7):
                nis_m = f"25MUT{m_idx:02d}"
                st_m, created = Student.objects.get_or_create(
                    student_number=nis_m,
                    defaults={
                        "name": fake.name(),
                        "gender": GenderEnum.PEREMPUAN,
                        "status": StudentStatusEnum.MUTASI_KELUAR,
                    },
                )
                if created:
                    metrics["students"] += 1
            for n_idx in range(1, 7):
                nis_n = f"25NON{n_idx:02d}"
                st_n, created = Student.objects.get_or_create(
                    student_number=nis_n,
                    defaults={
                        "name": fake.name(),
                        "gender": GenderEnum.LAKI_LAKI,
                        "status": StudentStatusEnum.NONAKTIF,
                    },
                )
                if created:
                    metrics["students"] += 1

        self.stdout.write(
            f"        -> {Student.objects.count()} Total siswa ({len(all_active_students)} siswa aktif di 12 rombel)."
        )

        # [08/12] Membuat penugasan guru & wali kelas (Class Assignments)
        self.stdout.write("[08/12] Membuat penugasan guru & wali kelas (Class Assignments)...")
        # 1. Main accounts assignments:
        # - wali_kelas assigned to X-1 and XI-MIPA-1
        # - guru_walikelas assigned to X-2
        # - guru assigned as GURU_MAPEL to X-1, X-2, XI-MIPA-1, XI-2
        # - XII-4 is specifically unassigned to guru and wali_kelas for negative auth testing
        all_teachers = [
            e for u_name, e in employees.items() if "guru" in u_name or "wali" in u_name or "pegawai" in u_name
        ]

        for idx, s_class in enumerate(active_classes):
            # Assign Wali Kelas
            if s_class.name in ["X-1", "XI-MIPA-1"]:
                wk_emp = employees["wali_kelas"]
            elif s_class.name == "X-2":
                wk_emp = employees["guru_walikelas"]
            else:
                wk_emp = all_teachers[(idx + 2) % len(all_teachers)]

            asg_wk, created = ClassAssignment.objects.get_or_create(
                employee=wk_emp,
                school_class=s_class,
                role=ClassAssignmentRoleEnum.WALI_KELAS,
                defaults={"start_date": active_ay.start_date, "end_date": None},
            )
            if created:
                metrics["assignments"] += 1

            # Assign Guru Mapel
            if s_class.name in ["X-1", "X-2", "XI-MIPA-1", "XI-2"]:
                mapel_emp = employees["guru"]
            elif s_class.name == "XII-4":
                # Specifically unassigned to test accounts!
                mapel_emp = all_teachers[-1]
            else:
                mapel_emp = all_teachers[(idx + 5) % len(all_teachers)]

            asg_gm, created = ClassAssignment.objects.get_or_create(
                employee=mapel_emp,
                school_class=s_class,
                role=ClassAssignmentRoleEnum.GURU_MAPEL,
                defaults={"start_date": active_ay.start_date, "end_date": None},
            )
            if created:
                metrics["assignments"] += 1

        self.stdout.write(
            f"        -> {ClassAssignment.objects.count()} Penugasan guru terpasang (12 Wali Kelas lengkap)."
        )

        # [09/12] Mengisi riwayat presensi harian (Attendance & History)
        self.stdout.write(f"[09/12] Mengisi riwayat presensi harian ({attendance_days_count} hari pembelajaran)...")
        # Generate weekdays from start of active AY
        curr_date = active_ay.start_date
        attendance_dates = []
        end_date_limit = min(date(2026, 11, 13), active_ay.end_date)

        while curr_date <= end_date_limit and len(attendance_dates) < attendance_days_count:
            if curr_date.weekday() < 5:  # Monday to Friday
                attendance_dates.append(curr_date)
            curr_date += timedelta(days=1)

        recorded_by_user = users["guru"]
        sakit_notes = ["Demam tinggi", "Flu dan batuk", "Sakit kepala", "Radang tenggorokan", "Sakit perut"]
        izin_notes = [
            "Acara keluarga mendesak",
            "Mengikuti lomba sains",
            "Urusan keluarga",
            "Surat keterangan orang tua",
        ]

        new_attendance_records = []
        existing_keys = set(
            Attendance.objects.filter(school_class__in=active_classes, date__in=attendance_dates).values_list(
                "student_id", "school_class_id", "date"
            )
        )

        primary_classes = ["XI-MIPA-1", "X-1", "X-2"]
        for s_class in active_classes:
            class_students = [st for st in all_active_students if st.enrollments.filter(school_class=s_class).exists()]
            class_dates = attendance_dates if s_class.name in primary_classes else attendance_dates[-10:]
            for att_date in class_dates:
                for st in class_students:
                    key = (st.id, s_class.id, att_date)
                    if key in existing_keys:
                        continue

                    roll = rng.random()
                    if roll < 0.92:
                        att_status = AttendanceStatusEnum.HADIR
                        note_text = ""
                    elif roll < 0.95:
                        att_status = AttendanceStatusEnum.SAKIT
                        note_text = rng.choice(sakit_notes)
                    elif roll < 0.98:
                        att_status = AttendanceStatusEnum.IZIN
                        note_text = rng.choice(izin_notes)
                    else:
                        att_status = AttendanceStatusEnum.ALPA
                        note_text = "Tanpa keterangan"

                    new_attendance_records.append(
                        Attendance(
                            student=st,
                            school_class=s_class,
                            date=att_date,
                            status=att_status,
                            note=note_text,
                            recorded_by=recorded_by_user,
                        )
                    )

        if new_attendance_records:
            # Batch insertion with history tracking
            batch_size = 1000
            for b_idx in range(0, len(new_attendance_records), batch_size):
                chunk = new_attendance_records[b_idx : b_idx + batch_size]
                bulk_create_with_history(chunk, Attendance, batch_size=batch_size)
            metrics["attendance"] += len(new_attendance_records)

        self.stdout.write(
            f"        -> {Attendance.objects.count()} Rekor presensi tercatat ({metrics['attendance']} baru)."
        )

        # [10/12] Mengisi kasus kesiswaan & timeline (Cases & Events)
        self.stdout.write(f"[10/12] Mengisi kasus kesiswaan & timeline ({total_cases} kasus)...")
        case_templates = [
            (
                "Keterlambatan masuk kelas berulang",
                "Siswa tercatat terlambat lebih dari 3 kali dalam satu bulan.",
                CaseStatusEnum.SELESAI,
            ),
            (
                "Ketidakhadiran tanpa keterangan",
                "Siswa tidak hadir 3 hari berturut-turut tanpa surat izin.",
                CaseStatusEnum.DIPROSES,
            ),
            (
                "Atribut seragam tidak lengkap",
                "Siswa tidak mengenakan dasi dan topi saat upacara bendera.",
                CaseStatusEnum.SELESAI,
            ),
            (
                "Keterlambatan pengumpulan tugas",
                "Siswa belum menyerahkan tugas portofolio mata pelajaran.",
                CaseStatusEnum.BARU,
            ),
            (
                "Pembinaan kedisiplinan belajar",
                "Pendampingan motivasi belajar dan kedisiplinan ruang kelas.",
                CaseStatusEnum.DIPROSES,
            ),
            (
                "Konseling penyesuaian lingkungan",
                "Siswa membutuhkan pendampingan adaptasi dan interaksi sosial.",
                CaseStatusEnum.SELESAI,
            ),
            (
                "Klarifikasi izin sakit",
                "Pemeriksaan dan verifikasi surat keterangan sakit dari puskesmas.",
                CaseStatusEnum.SELESAI,
            ),
            (
                "Klarifikasi kesalahpahaman antarsiswa",
                "Mediasi pembinaan komunikasi positif di lingkungan sekolah.",
                CaseStatusEnum.DIBATALKAN,
            ),
        ]

        kesiswaan_emp = employees["kesiswaan"]
        kesiswaan_user = users["kesiswaan"]

        for c_idx in range(total_cases):
            title_tpl, summary_tpl, target_status = case_templates[c_idx % len(case_templates)]
            st_target = all_active_students[c_idx % len(all_active_students)]
            case_title = f"{title_tpl} #{c_idx + 1}"

            sc, created = StudentCase.objects.get_or_create(
                student=st_target,
                title=case_title,
                defaults={
                    "summary": f"{summary_tpl} (Siswa: {st_target.name})",
                    "status": target_status,
                    "assigned_to": kesiswaan_emp,
                    "version": 1 if target_status == CaseStatusEnum.BARU else 2,
                },
            )
            if created:
                metrics["cases"] += 1
                # Create timeline events
                # Initial event: Creation
                CaseEvent.objects.create(
                    case=sc,
                    action=CaseActionEnum.MULAI_PENANGANAN if target_status != CaseStatusEnum.BARU else "BUAT_KASUS",
                    initial_status=CaseStatusEnum.BARU,
                    final_status=CaseStatusEnum.DIPROSES
                    if target_status != CaseStatusEnum.BARU
                    else CaseStatusEnum.BARU,
                    note="Kasus kesiswaan telah dicatat dan dijadwalkan untuk pendampingan.",
                    actor=kesiswaan_user,
                )
                metrics["case_events"] += 1

                if target_status in [CaseStatusEnum.DIPROSES, CaseStatusEnum.SELESAI]:
                    # Action recorded (contains confidential counseling note for DEC-TECH-18 masking)
                    CaseEvent.objects.create(
                        case=sc,
                        action=CaseActionEnum.CATAT_TINDAKAN,
                        initial_status=CaseStatusEnum.DIPROSES,
                        final_status=CaseStatusEnum.DIPROSES,
                        note="[Catatan konseling privat] Telah dilakukan pembinaan tatap muka dan konseling berkala dengan siswa.",
                        actor=kesiswaan_user,
                    )
                    metrics["case_events"] += 1

                if target_status == CaseStatusEnum.SELESAI:
                    CaseEvent.objects.create(
                        case=sc,
                        action=CaseActionEnum.SELESAIKAN,
                        initial_status=CaseStatusEnum.DIPROSES,
                        final_status=CaseStatusEnum.SELESAI,
                        note="Siswa telah menunjukkan perbaikan perilaku yang signifikan. Kasus resmi ditutup.",
                        actor=kesiswaan_user,
                    )
                    metrics["case_events"] += 1
                elif target_status == CaseStatusEnum.DIBATALKAN:
                    CaseEvent.objects.create(
                        case=sc,
                        action=CaseActionEnum.BATALKAN,
                        initial_status=CaseStatusEnum.BARU,
                        final_status=CaseStatusEnum.DIBATALKAN,
                        note="Setelah klarifikasi dokumen, permasalahan telah selesai secara kekeluargaan.",
                        actor=kesiswaan_user,
                    )
                    metrics["case_events"] += 1

        self.stdout.write(
            f"        -> {StudentCase.objects.count()} Kasus kesiswaan & {CaseEvent.objects.count()} Events siap."
        )

        # [11/12] Mengisi jenis layanan, permohonan surat & dokumen fisik
        self.stdout.write(
            f"[11/12] Mengisi jenis layanan, permohonan surat & dokumen fisik ({total_requests} permohonan)..."
        )
        service_types_data = [
            (
                "SK-AKTIF",
                "Surat Keterangan Siswa Aktif",
                "Surat keterangan resmi status keaktifan belajar siswa.",
                True,
            ),
            (
                "SK-LULUS",
                "Surat Keterangan Lulus (SKL)",
                "Surat keterangan tamat belajar sementara sebelum ijazah terbit.",
                True,
            ),
            (
                "LEGALISIR",
                "Legalisasi Dokumen Ijazah / Rapor",
                "Pengesahan salinan dokumen akademik sesuai aslinya.",
                False,
            ),
            (
                "SK-BEASISWA",
                "Surat Keterangan Pengajuan Beasiswa",
                "Surat rekomendasi untuk melengkapi persyaratan beasiswa.",
                True,
            ),
            ("SK-PINDAH", "Surat Keterangan Pindah Sekolah", "Surat pengantar mutasi keluar ke sekolah lain.", True),
            (
                "SK-KELAKUAN",
                "Surat Keterangan Berkelakuan Baik",
                "Surat keterangan catatan kepatuhan dan tata tertib siswa.",
                True,
            ),
            (
                "SURAT-PENGANTAR",
                "Surat Pengantar Magang / Lomba",
                "Surat izin dan tugas mengikuti kegiatan eksternal.",
                True,
            ),
            (
                "SALINAN-RAPOR",
                "Permohonan Salinan Rapor",
                "Permohonan cetak ulang lembar penilaian rapor siswa.",
                False,
            ),
            (
                "SK-PEGAWAI",
                "Surat Keterangan Aktif Pegawai",
                "Surat keterangan masa kerja dan keaktifan tugas pegawai.",
                True,
            ),
            ("INFO-AKADEMIK", "Permohonan Informasi Data Akademik", "Layanan verifikasi data pokok pendidikan.", False),
        ]
        service_types = []
        for code, st_name, st_desc, req_app in service_types_data:
            st_obj, created = ServiceType.objects.get_or_create(
                code=code,
                defaults={"name": st_name, "description": st_desc, "requires_approval": req_app, "is_active": True},
            )
            service_types.append(st_obj)
            if created:
                metrics["service_types"] += 1

        tu_user = users["tata_usaha"]
        kepsek_user = users["kepsek"]
        private_media_dir = Path(settings.PRIVATE_MEDIA_ROOT)
        private_media_dir.mkdir(parents=True, exist_ok=True)

        # Status distribution pool for realistic queues
        status_pool = (
            [ServiceRequestStatusEnum.DIAJUKAN] * 4
            + [ServiceRequestStatusEnum.DIPROSES] * 3
            + [ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN] * 3
            + [ServiceRequestStatusEnum.DISETUJUI] * 2
            + [ServiceRequestStatusEnum.DITOLAK] * 1
            + [ServiceRequestStatusEnum.SELESAI] * 4
        )

        for req_idx in range(total_requests):
            stype = service_types[req_idx % len(service_types)]
            target_status = status_pool[req_idx % len(status_pool)]
            st_applicant = all_active_students[req_idx % len(all_active_students)]
            req_num = f"SR-202611{req_idx + 1:04d}"

            sreq, created = ServiceRequest.objects.get_or_create(
                request_number=req_num,
                defaults={
                    "service_type": stype,
                    "applicant_name": st_applicant.name,
                    "applicant_phone": f"0812{rng.randint(10000000, 99999999)}",
                    "student": st_applicant,
                    "purpose": f"Melengkapi berkas administrasi keperluan {stype.name.lower()}.",
                    "status": target_status,
                    "created_by": tu_user,
                    "version": 1 if target_status == ServiceRequestStatusEnum.DIAJUKAN else 2,
                },
            )
            if created:
                metrics["service_requests"] += 1
                # Lifecycle events
                ServiceEvent.objects.create(
                    request=sreq,
                    action="PENGAJUAN",
                    initial_status=ServiceRequestStatusEnum.DIAJUKAN,
                    final_status=ServiceRequestStatusEnum.DIAJUKAN,
                    note="Permohonan surat berhasil didaftarkan ke sistem tata usaha.",
                    actor=tu_user,
                )
                metrics["service_events"] += 1

                if target_status != ServiceRequestStatusEnum.DIAJUKAN:
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.PROSES,
                        initial_status=ServiceRequestStatusEnum.DIAJUKAN,
                        final_status=ServiceRequestStatusEnum.DIPROSES,
                        note="Berkas sedang diverifikasi oleh staf tata usaha.",
                        actor=tu_user,
                    )
                    metrics["service_events"] += 1

                if target_status in [
                    ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                    ServiceRequestStatusEnum.DISETUJUI,
                    ServiceRequestStatusEnum.DITOLAK,
                    ServiceRequestStatusEnum.SELESAI,
                ]:
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.AJUKAN_PERSETUJUAN,
                        initial_status=ServiceRequestStatusEnum.DIPROSES,
                        final_status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                        note="Diteruskan ke Kepala Sekolah untuk disposisi persetujuan.",
                        actor=tu_user,
                    )
                    metrics["service_events"] += 1

                if target_status == ServiceRequestStatusEnum.DISETUJUI:
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.SETUJUI,
                        initial_status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                        final_status=ServiceRequestStatusEnum.DISETUJUI,
                        note="Disetujui. Surat siap dicetak dan ditandatangani.",
                        actor=kepsek_user,
                    )
                    metrics["service_events"] += 1
                elif target_status == ServiceRequestStatusEnum.DITOLAK:
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.TOLAK,
                        initial_status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                        final_status=ServiceRequestStatusEnum.DITOLAK,
                        note="Ditolak. Persyaratan berkas pendukung belum lengkap.",
                        actor=kepsek_user,
                    )
                    metrics["service_events"] += 1
                elif target_status == ServiceRequestStatusEnum.SELESAI:
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.SETUJUI,
                        initial_status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                        final_status=ServiceRequestStatusEnum.DISETUJUI,
                        note="Disetujui Kepala Sekolah.",
                        actor=kepsek_user,
                    )
                    ServiceEvent.objects.create(
                        request=sreq,
                        action=ServiceActionEnum.SELESAIKAN,
                        initial_status=ServiceRequestStatusEnum.DISETUJUI,
                        final_status=ServiceRequestStatusEnum.SELESAI,
                        note="Surat telah diserahkan kepada pemohon dan diarsipkan.",
                        actor=tu_user,
                    )
                    metrics["service_events"] += 2

                # Create physical private document for eligible requests
                if req_idx < total_documents and not sreq.documents.exists():
                    storage_uuid = str(uuid.uuid4())
                    doc_path = private_media_dir / storage_uuid

                    # Generate authentic ReportLab PDF with synthetic watermarks
                    pdf_buf = io.BytesIO()
                    p = canvas.Canvas(pdf_buf, pagesize=letter)
                    p.setFont("Helvetica-Bold", 14)
                    p.drawString(50, 750, "PEMERINTAH PROVINSI RIAU - DINAS PENDIDIKAN")
                    p.setFont("Helvetica-Bold", 16)
                    p.drawString(50, 730, "SMA NEGERI 1 BUNUT")
                    p.setFont("Helvetica", 9)
                    p.drawString(50, 715, "Alamat: Jl. Pelajar No. 1, Bunut, Kec. Bunut, Kab. Pelalawan, Riau")
                    p.line(50, 705, 550, 705)

                    p.setFont("Helvetica-Bold", 11)
                    p.setFillColorRGB(0.8, 0.1, 0.1)
                    p.drawString(50, 680, "[DOKUMEN SINTETIS PENGUJIAN SISTEM LOKAL - BUKAN DOKUMEN RESMI]")
                    p.setFillColorRGB(0, 0, 0)

                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(50, 640, f"SURAT KETERANGAN: {stype.name.upper()}")
                    p.setFont("Helvetica", 10)
                    p.drawString(50, 620, f"Nomor Registrasi : {sreq.request_number}")
                    p.drawString(50, 600, f"Nama Pemohon     : {sreq.applicant_name}")
                    p.drawString(50, 580, f"Siswa Terkait    : {st_applicant.name} ({st_applicant.student_number})")
                    p.drawString(50, 560, f"Status Berkas    : {sreq.status}")
                    p.drawString(50, 540, f"Tanggal Terbit   : {date.today().strftime('%d %B %Y')}")

                    p.drawString(
                        50, 500, "Menerangkan bahwa data permohonan di atas telah terdaftar dan diproses secara sah"
                    )
                    p.drawString(50, 485, "dalam Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut.")
                    p.drawString(50, 470, f"Keperluan: {sreq.purpose}")

                    p.setFont("Helvetica-Oblique", 9)
                    p.drawString(
                        50, 400, "Dokumen ini di-generate secara otomatis untuk validasi alur unduh dokumen privat."
                    )
                    p.save()

                    pdf_bytes = pdf_buf.getvalue()
                    with open(doc_path, "wb") as f_out:
                        f_out.write(pdf_bytes)

                    Document.objects.create(
                        request=sreq,
                        storage_key=storage_uuid,
                        original_filename=f"Surat_{stype.code}_{sreq.request_number}.pdf",
                        mime_type="application/pdf",
                        file_size=len(pdf_bytes),
                        uploaded_by=tu_user,
                    )
                    metrics["documents"] += 1

        self.stdout.write(
            f"        -> {ServiceRequest.objects.count()} Permohonan & {Document.objects.count()} Dokumen privat fisik siap."
        )

        # [12/12] Memverifikasi integritas data & audit trail (Verification)
        self.stdout.write("[12/12] Memverifikasi integritas data & audit trail...")
        # Record master seeding activity log
        ActivityLog.objects.create(
            actor=users["admin"],
            action="EXECUTE_DATABASE_SEEDER",
            resource_type="system",
            resource_id="seed_school_data",
            metadata=f"profile={profile}, seed={seed_value}",
        )
        metrics["activity_logs"] += 1

        duration = time.time() - start_time
        self.stdout.write("--------------------------------------------------------------------------------")
        self.stdout.write(self.style.SUCCESS(f"=== POPULASI DATABASE SELESAI ({duration:.2f} detik) ==="))
        self.stdout.write(f"Total Peran (Roles)               : {Role.objects.count()}")
        self.stdout.write(f"Total Pengguna (Users)            : {User.objects.count()}")
        self.stdout.write(f"Total Pegawai (Employees)         : {Employee.objects.count()}")
        self.stdout.write(
            f"Total Tahun Ajaran (AcademicYears): {AcademicYear.objects.count()} (Aktif: {AcademicYear.objects.filter(is_active=True).count()})"
        )
        self.stdout.write(f"Total Kelas (SchoolClasses)       : {SchoolClass.objects.count()}")
        self.stdout.write(
            f"Total Siswa (Students)            : {Student.objects.count()} (Aktif: {Student.objects.filter(status='AKTIF').count()})"
        )
        self.stdout.write(f"Total Penempatan (Enrollments)    : {Enrollment.objects.count()}")
        self.stdout.write(f"Total Penugasan (ClassAssignments): {ClassAssignment.objects.count()}")
        self.stdout.write(f"Total Rekor Presensi (Attendance) : {Attendance.objects.count()}")
        self.stdout.write(f"Total Kasus Kesiswaan (Cases)     : {StudentCase.objects.count()}")
        self.stdout.write(f"Total Riwayat Kasus (CaseEvents)  : {CaseEvent.objects.count()}")
        self.stdout.write(f"Total Jenis Layanan (ServiceTypes): {ServiceType.objects.count()}")
        self.stdout.write(f"Total Permohonan (ServiceRequests): {ServiceRequest.objects.count()}")
        self.stdout.write(f"Total Riwayat Permohonan (Events) : {ServiceEvent.objects.count()}")
        self.stdout.write(f"Total Dokumen Fisik (Documents)   : {Document.objects.count()}")
        self.stdout.write("--------------------------------------------------------------------------------")
        self.stdout.write(
            self.style.NOTICE("Daftar akun dan password lokal tersimpan di: docs/guide/ACCOUNTS.local.md")
        )
