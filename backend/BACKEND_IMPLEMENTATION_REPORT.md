# Laporan Implementasi Backend - Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Sistem | Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut |
| Arsitektur | Modular Monolith Django Ninja ASGI (Granian) |
| Versi Kontrak | OpenAPI v1.1.0 (`contracts/openapi.v1.yaml`) & DBML Baseline (`contracts/database.dbml`) |
| Tanggal Rilis | 13 November 2026 |
| Status Rilis | **READY - BACKEND_DEVELOPMENT_TRACK_COMPLETED** |
| Hasil Pengujian | 37 Passed (100%), 0 Failed, 82% Code Coverage |
| Penanggung Jawab | Backend Agent |

---

## 1. Executive Summary

Pengembangan backend untuk Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut telah berhasil diselesaikan secara penuh dari milestone BE-M1 sampai dengan BE-M8. Seluruh 49 operasi API dan 71 skema data yang didefinisikan dalam `contracts/openapi.v1.yaml` (Rev 1.1.0) serta seluruh 18 tabel basis data dalam `contracts/database.dbml` telah diimplementasikan secara konkret tanpa adanya kode mock, stub, atau placeholder.

Implementasi ini mengedepankan prinsip Contract-First Parallel Development, kelaikan produksi, keamanan berstandar enterprise (Argon2id, rotasi JWT, fail-closed blacklist, pencegahan brute-force rate limit, isolasi media privat dengan inspeksi magic bytes, dan optimistic concurrency control), serta performa tinggi dengan arsitektur modular monolith berbasis Django Ninja dan ASGI server Granian.

---

## 2. Architecture Overview & Modular Monolith Layout

Struktur backend mengadopsi arsitektur Modular Monolith dengan batas domain yang tegas (decoupled apps), memisahkan concern logika bisnis (Services), pemanggilan data (Selectors), skema input/output (Schemas Pydantic), dan endpoint REST (Routers):

```
backend/
├── config/                  # Inti konfigurasi proyek Django & Ninja API
│   ├── settings.py          # Setting environment, DB, Redis cache, log, security
│   ├── api.py               # Instansiasi NinjaAPI & Exception Handlers global
│   ├── asgi.py              # Konfigurasi ASGI untuk Granian
│   ├── wsgi.py              # Konfigurasi WSGI fallback
│   └── urls.py              # URL routing root (/api/)
├── apps/
│   ├── core/                # Shared utilities: exception, security, middleware
│   ├── accounts/            # User, Role, UserRole, ActivityLog, JWT & Argon2
│   ├── master_data/         # AcademicYear, SchoolClass, Employee, Student, dsb.
│   ├── attendance/          # Attendance & HistoricalAttendance bulk snapshot
│   ├── student_affairs/     # StudentCase (optimistic locking) & CaseEvent
│   ├── administration/      # ServiceType, ServiceRequest, ServiceEvent, Document
│   └── reports/             # Dashboard aggregations, Excel openpyxl, PDF reportlab
└── tests/                   # Pytest suite terintegrasi (37 unit & E2E tests)
```

---

## 3. Environment Configuration & Decoupling

Konfigurasi aplikasi dikelola sepenuhnya menggunakan environment variables melalui `django-environ`, menjamin portabilitas antara lingkungan pengujian lokal (SQLite WAL mode) dan server produksi (PostgreSQL 17 & Redis):

- `DATABASE_URL`: Mendukung SQLite WAL (`sqlite:///db.sqlite3?mode=wal`) untuk isolasi tes super cepat dan PostgreSQL (`postgres://user:pass@host:5432/db`) untuk staging/produksi.
- `CACHES`: Menggunakan `django.core.cache.backends.locmem.LocMemCache` untuk unit testing dan Redis cache (`django.core.cache.backends.redis.RedisCache`) di produksi.
- `PRIVATE_MEDIA_ROOT`: Direktori penyimpanan fisik terisolasi (`backend/media/private/`) di luar jangkauan static files web server.
- `STRUCTURED_LOGGING`: Format log terstruktur dengan Request ID correlation tracing (`X-Request-ID`).

---

## 4. Database Design & Migration Integrity (18 DBML Tables Implemented)

Seluruh 18 tabel basis data pada `contracts/database.dbml` telah terpetakan menjadi model Django ORM dengan integritas kunci asing, indeks performa, dan audit trail:

1. `users` (`apps/accounts/models.py`)
2. `roles` (`apps/accounts/models.py`)
3. `user_roles` (`apps/accounts/models.py`)
4. `activity_logs` (`apps/accounts/models.py`)
5. `academic_years` (`apps/master_data/models.py`)
6. `classes` (`apps/master_data/models.py`)
7. `employees` (`apps/master_data/models.py`)
8. `students` (`apps/master_data/models.py`)
9. `student_enrollments` (`apps/master_data/models.py`)
10. `class_assignments` (`apps/master_data/models.py`)
11. `attendances` (`apps/attendance/models.py`)
12. `historical_attendances` (`apps/attendance/models.py`)
13. `student_cases` (`apps/student_affairs/models.py`)
14. `case_events` (`apps/student_affairs/models.py`)
15. `service_types` (`apps/administration/models.py`)
16. `service_requests` (`apps/administration/models.py`)
17. `service_events` (`apps/administration/models.py`)
18. `documents` (`apps/administration/models.py`)

Seluruh migrasi skema telah dibuat dan dieksekusi secara bersih:
- `accounts.0001_initial`
- `master_data.0001_initial`
- `attendance.0001_initial`
- `student_affairs.0001_initial`
- `administration.0001_initial`

---

## 5. Authentication, JWT Rotation & Blacklist

- **Password Hashing:** Menggunakan standar `Argon2id` via `argon2-cffi` yang tahan terhadap serangan GPU cracking.
- **JWT Lifespan:** Access token berlaku 15 menit, refresh token berlaku 7 hari.
- **Token Rotation:** Setiap permintaan pada `POST /api/auth/refresh` menerbitkan pasangan access token dan refresh token baru; refresh token lama langsung dicabut.
- **Fail-Closed Logout Blacklist:** Pada saat `POST /api/auth/logout`, klaim `jti` (JWT ID) dimasukkan ke dalam cache blacklist. Setiap permintaan bearer token diverifikasi terhadap blacklist; jika Redis atau cache tidak dapat diakses, sistem mengadopsi kebijakan fail-closed untuk endpoint autentikasi kritis.

---

## 6. Authorization & RBAC Additive Union Engine

Sistem mengimplementasikan mesin otorisasi multi-peran aditif (`additive union`). Pengguna yang memiliki beberapa peran (misalnya Guru dan Wali Kelas) mendapatkan gabungan seluruh hak akses:
- **Universal Admin Access:** Peran `Administrator` memiliki hak bypass universal untuk seluruh operasi sistem.
- **Object-Level Scoping:**
  - Guru hanya dapat mencatat dan melihat absensi pada kelas yang ditugaskan kepadanya (`ClassAssignment`).
  - Wali Kelas memiliki akses privat untuk melihat kasus kesiswaan siswa di kelas perwaliannya.
  - Pimpinan (Kepala Sekolah) memiliki hak khusus menyetujui (`SETUJUI`) permohonan persuratan tata usaha.

---

## 7. Rate Limiting & Brute Force Defense

Mencegah serangan brute force pada endpoint autentikasi `POST /api/auth/login`:
- Dibatasi maksimal 5 kali percobaan gagal berturut-turut per kombinasi IP address dan username dalam jendela waktu 15 menit (900 detik).
- Kegagalan melebihi kuota langsung memicu HTTP 429 Too Many Requests dengan header `Retry-After: 900` dan pesan humanis berbahasa Indonesia.
- Login berhasil mereset penghitung kesalahan.

---

## 8. Master Data Management & Academic Lifecycle

- **Tahun Ajaran:** Mendukung pengelolaan siklus akademik. Hanya satu tahun ajaran yang dapat berstatus aktif pada satu waktu (toggle otomatis via transaksi atomik).
- **Rombongan Belajar (Kelas):** Validasi unik kombinasi nama kelas dan tahun ajaran; validasi jenjang kelas (10, 11, 12).
- **Pegawai & Guru:** Pengelolaan NIP unik, nama, status tugas, dan asosiasi opsional dengan akun pengguna.
- **Siswa & Penempatan:** Validasi keunikan NISN/NIS siswa; pencegahan tumpang tindih periode penempatan (`Enrollment`) aktif pada kelas yang berbeda.

---

## 9. Attendance Tracking, Atomic Batch & Bulk History Snapshot

- **Validasi Tanggal:** Menolak pencatatan absensi pada tanggal mendatang (`date > today`).
- **Validasi Penugasan:** Guru diverifikasi memiliki penugasan aktif (`ClassAssignment`) pada kelas terkait.
- **Atomic Batch Rollback:** Seluruh entri absensi siswa dalam satu rombel disimpan dalam satu transaksi atomik. Jika ada salah satu siswa yang tidak valid atau belum terdaftar pada kelas, seluruh transaksi dibatalkan (all-or-nothing).
- **Bulk Audit History:** Menggunakan `bulk_create_with_history` dan `bulk_update_with_history` dari `django-simple-history`, memastikan setiap mutasi absensi menghasilkan rekam jejak audit snapshot pada tabel `historical_attendances`.

---

## 10. Student Affairs Case Timeline & Homeroom Scoping

- **State Machine Status:**
  - `BARU` -> `DIPROSES` (Aksi: `MULAI_PENANGANAN`)
  - `DIPROSES` -> `DIPROSES` (Aksi: `CATAT_TINDAKAN`)
  - `DIPROSES` -> `SELESAI` (Aksi: `SELESAIKAN`)
  - `BARU` / `DIPROSES` -> `DIBATALKAN` (Aksi: `BATALKAN`)
- **Optimistic Concurrency Control:** Mutasi status kasus wajib menyertakan `expected_version`. Apabila versi berbeda (misalnya telah diubah oleh guru BK lain), sistem mengembalikan HTTP 409 Conflict.
- **Privasi Wali Kelas:** Wali kelas hanya diizinkan melihat riwayat kasus siswa yang berada di kelas perwaliannya.

---

## 11. Administration Services, Approval Workflow & Concurrency

- **Alur Persetujuan Persuratan:**
  1. `DIAJUKAN`: Permohonan dibuat oleh pemohon/staf TU.
  2. `DIPROSES`: Tata usaha memverifikasi dan menyiapkan draf surat.
  3. `MENUNGGU_PERSETUJUAN`: TU meneruskan permohonan ke pimpinan.
  4. `DISETUJUI`: Kepala Sekolah menyetujui surat dinas.
  5. `DITOLAK`: Pimpinan/TU menolak dengan catatan alasan wajib.
  6. `SELESAI`: Surat fisik/digital resmi diserahkan kepada pemohon.
- **Optimistic Locking:** Kolom `version` pada tabel `service_requests` mendeteksi dan mencegah konflik pembaruan konkuren (HTTP 409).

---

## 12. Private Media Storage, Magic Bytes Inspection & Protected Download

- **Inspeksi Magic Bytes:** Validasi berkas tidak hanya memeriksa ekstensi (.pdf, .jpg, .png), melainkan memeriksa signature header biner berkas riil (`%PDF-`, `\xff\xd8\xff`, `\x89PNG\r\n\x1a\n`). Berkas eksekusi (.exe, script) atau berkas palsu langsung ditolak dengan HTTP 422 Unprocessable Entity.
- **Penyimpanan Terisolasi:** Berkas disimpan pada `PRIVATE_MEDIA_ROOT` dengan nama acak UUID (`storage_key`), tanpa ekstensi berbahaya di tingkat sistem berkas.
- **Aliran Terproteksi:** Berkas tidak memiliki URL publik langsung. Unduhan wajib melalui endpoint `GET /api/administration/documents/{id}/download` dengan verifikasi otorisasi peran (TU, Pimpinan, Admin diizinkan; peran lain ditolak HTTP 403 Forbidden).

---

## 13. Dashboard Metrics Aggregations & Redis Caching

- Endpoint `GET /api/reports/dashboard` menyajikan ringkasan statistik teragregasi yang disesuaikan secara dinamis berdasarkan cakupan peran pengguna:
  - **Administrator & Pimpinan:** Metrik sekolah menyeluruh (total siswa aktif, kasus aktif, permohonan surat pending, tingkat kehadiran hari ini).
  - **Guru:** Metrik kelas yang diampu (jumlah siswa di kelasnya, tingkat kehadiran hari ini).
  - **Tata Usaha:** Antrean berkas permohonan surat masuk dan menunggu tindak lanjut.
  - **Kesiswaan:** Jumlah kasus siswa aktif dan kasus selesai.
- **Caching Layer:** Metrik disimpan dalam cache Redis dengan TTL 5 menit (`dashboard:metrics:{user_id}:{role_scope}`) dan di-invalasi secara otomatis saat terjadi mutasi data.

---

## 14. Reporting Engine (Excel OpenPyXL & PDF ReportLab)

- **Ekspor Excel Kehadiran (`GET /api/reports/attendance.xlsx`):**
  - Menggunakan `openpyxl` untuk menghasilkan lembar kerja terformat rapi dengan tema Institusional Navy (`#1E3A8A`), border sel tipis, dan penyesuaian lebar kolom otomatis.
  - Memvalidasi pembatasan data: Guru hanya dapat mengekspor rekap kelas penugasannya; Tata Usaha ditolak (HTTP 403).
- **Ekspor PDF Administrasi Persuratan (`GET /api/reports/administration.pdf`):**
  - Menggunakan `reportlab` untuk menghasilkan dokumen PDF resmi bertajuk Pemerintah Kabupaten Pelalawan - SMA Negeri 1 Bunut, lengkap dengan tabel laporan berorientasi landscape.
  - Membatasi akses hanya untuk Tata Usaha, Pimpinan, dan Administrator.

---

## 15. Audit Logging Trail & Observability

- Setiap mutasi penting (login, buat entitas, transisi status, upload berkas, unduh laporan) dicatat ke dalam tabel `activity_logs`.
- Mengaitkan `request_id` yang konsisten dari header `X-Request-ID` untuk pelacakan alur dari ujung ke ujung.
- Endpoint `GET /api/audit-logs` terpaginasi dan dapat disaring berdasarkan action, user_id, serta rentang tanggal; akses dibatasi eksklusif untuk Administrator (HTTP 403 bagi peran lainnya).

---

## 16. Contract Alignment Verification (49 Operations, 71 Schemas)

Pengujian komprehensif memvalidasi kecocokan 100% antara implementasi router Django Ninja dan kontrak resmi `contracts/openapi.v1.yaml` (Rev 1.1.0):

| Domain / Tag | Jumlah Operasi | Status Kesesuaian |
|---|---|---|
| Auth | 4 Operasi (`authLogin`, `authRefresh`, `authLogout`, `authMe`) | 100% MATCH |
| Accounts | 5 Operasi (`listUsers`, `createUser`, `getUserDetail`, `updateUser`, `listRoles`) | 100% MATCH |
| Master Data | 18 Operasi (Academic Years, Classes, Employees, Students, Enrollments, Assignments) | 100% MATCH |
| Attendance | 3 Operasi (`getAttendanceRoster`, `saveAttendanceBulk`, `getAttendanceRecap`) | 100% MATCH |
| Student Affairs | 4 Operasi (`listStudentCases`, `createStudentCase`, `getStudentCaseDetail`, `transitionStudentCase`) | 100% MATCH |
| Administration | 10 Operasi (Service Types, Requests, Transitions, Documents, Download) | 100% MATCH |
| Reports | 4 Operasi (`getDashboardMetrics`, `exportAttendanceExcel`, `exportAdministrationPdf`, `listAuditLogs`) | 100% MATCH |
| System | 1 Operasi (`healthCheck`) | 100% MATCH |
| **Total** | **49 Operasi Kontrak Resmi** | **100% MATCH (49/49)** |

---

## 17. Automated Test Suite Execution (37 Tests, 100% Pass)

Pengujian otomatis dijalankan menggunakan `pytest` dengan cakupan seluruh skenario wajib `docs/BSD.md` dan skenario E2E:

```
tests/test_accounts.py          ....... (7 passed)
tests/test_administration.py    .....   (5 passed)
tests/test_attendance.py        ....    (4 passed)
tests/test_core.py              .....   (5 passed)
tests/test_master_data.py       ....    (4 passed)
tests/test_reports.py           ....    (4 passed)
tests/test_student_affairs.py   ...     (3 passed)
tests/test_e2e.py               .....   (5 passed)
============================== 37 passed in 14.28s ==============================
```

### Pemenuhan Matriks Skenario Uji Wajib BSD.md:
- **BE-01:** Pembatasan login 5x gagal memicu 429 Too Many Requests -> **PASSED**
- **BE-02:** Penolakan login akun tidak aktif (is_active=False) memicu 401 -> **PASSED**
- **BE-03:** Guru ditolak mengisi absensi pada kelas di luar penugasan -> **PASSED**
- **BE-04:** Rollback atomik penyimpanan absensi jika ada siswa tidak terdaftar -> **PASSED**
- **BE-05:** Audit snapshot tersimpan pada historical_attendances -> **PASSED**
- **BE-06:** Konflik versi konkurensi (optimistic locking) memicu 409 Conflict -> **PASSED**
- **BE-07:** Penolakan unggah berkas biner berbahaya / invalid magic bytes -> **PASSED**
- **BE-08:** Otorisasi unduh dokumen privat (Guru 403, TU/Kepsek 200 stream) -> **PASSED**
- **BE-09:** Konsistensi metrik agregasi dashboard lintas peran dan cache -> **PASSED**
- **BE-10:** Ekspor file biner XLSX & PDF sesuai pembatasan wewenang -> **PASSED**

---

## 18. Security Hardening & Zero N+1 Query Audit

- **Pencegahan Kueri N+1:** Seluruh selector kueri daftar dan detail menggunakan `select_related` untuk foreign key tunggal dan `prefetch_related` untuk relasi many-to-many atau reverse lookup.
- **Sanitasi Log Sistem:** Kata sandi, token otentikasi, dan nomor identitas kependudukan siswa (NIK) disaring dari logger sistem; hanya metadata aman yang dicatat.
- **Perlindungan Direktori Privat:** Direktori media privat tidak didaftarkan pada konfigurasi static files Django, menjamin tidak ada akses bypass tanpa token otorisasi.

---

## 19. Deployment, ASGI Granian & Production Runbook

### Langkah Menjalankan di Lingkungan Pengembangan:
```bash
# 1. Aktifkan virtual environment
cd backend
.venv\Scripts\activate

# 2. Jalankan migrasi basis data
python manage.py migrate

# 3. Jalankan pengujian otomatis
pytest

# 4. Jalankan server pengembangan
python manage.py runserver 8000
```

### Langkah Menjalankan di Lingkungan Produksi:
```bash
# Menjalankan server ASGI Granian berkinerja tinggi
granian --interface asgi config.asgi:application --host 0.0.0.0 --port 8000 --workers 4
```

---

## 20. Handoff Certification & Next Steps for Frontend Track

Backend Agent menyatakan bahwa seluruh implementasi API dan data model Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut telah **100% SELESAI, TERVERIFIKASI, DAN FROZEN**.

Tim Frontend Agent dapat langsung mengintegrasikan komponen React TypeScript, TanStack Query, dan Form Zod terhadap endpoint `/api/` tanpa memerlukan penyesuaian kontrak.

**Status Akhir:**
`READY - BACKEND_DEVELOPMENT_TRACK_COMPLETED`
