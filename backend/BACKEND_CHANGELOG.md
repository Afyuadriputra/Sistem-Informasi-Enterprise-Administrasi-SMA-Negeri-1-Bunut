# Backend Changelog - Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Seluruh catatan pembaruan teknis pada pengembangan backend dari milestone BE-M1 hingga BE-M8 dicatat secara kronologis dalam dokumen ini.

---

## [BE-M1] - Foundation & Core Configuration
**Tanggal:** 12 November 2026

### Ditambahkan:
- Direktori dasar `backend/` dengan lingkungan virtual Python 3.12.
- Konfigurasi `backend/config/` (`settings.py`, `asgi.py`, `wsgi.py`, `urls.py`, `api.py`).
- Shared module `backend/apps/core/`:
  - `exceptions.py`: Hierarki exception terstandarisasi (`AppException`, `NotFoundError`, `BusinessValidationError`, `PermissionDeniedError`, `AuthenticationFailedError`, `RateLimitExceededError`, `ConcurrencyConflictError`).
  - `schemas.py`: `ErrorEnvelope` dan `ErrorDetailItem` terpadu sesuai standar OpenAPI.
  - `middleware.py`: `RequestIDMiddleware` dan `RequestLoggingMiddleware` untuk penelusuran korelasi request.
  - `security.py`: `JWTAuth` Ninja bearer authentication, fungsi evaluasi `check_roles` multi-peran, dan `require_roles`.
- Konfigurasi pengujian `backend/pytest.ini` dan linting `backend/ruff.toml`.
- Pengujian unit dasar `backend/tests/test_core.py` (5 skenario lulus).

---

## [BE-M2] - Authentication, Custom User & RBAC
**Tanggal:** 12 November 2026

### Ditambahkan:
- Modul `backend/apps/accounts/`:
  - Model `User`, `Role`, `UserRole`, dan `ActivityLog` dengan skema migrasi `0001_initial.py`.
  - Hashing kata sandi berbasis Argon2id (`argon2-cffi`).
  - Layanan penerbitan pasangan JWT (`access_token` 15 menit, `refresh_token` 7 hari) dan mekanisme rotasi token.
  - Penarikan token logout berbasis cache blacklist menggunakan klaim `jti`.
  - Pembatasan laju login (`LoginRateLimiter`) maksimal 5 kesalahan per 15 menit per IP dan username (BE-01).
  - Pengecekan status akun aktif (`is_active`) yang menolak pengguna nonaktif dengan 401 (BE-02).
  - Router API `/auth` (`login`, `refresh`, `logout`, `me`) dan `/accounts` (`listUsers`, `createUser`, `getUserDetail`, `updateUser`, `listRoles`).
- Pengujian unit autentikasi `backend/tests/test_accounts.py` (7 skenario lulus).

---

## [BE-M3] - Master Data & Academic Management
**Tanggal:** 12 November 2026

### Ditambahkan:
- Modul `backend/apps/master_data/`:
  - Model `AcademicYear`, `SchoolClass`, `Employee`, `Student`, `Enrollment`, dan `ClassAssignment` dengan skema migrasi `0001_initial.py`.
  - Logika siklus tahun ajaran dengan toggle otomatis hanya satu tahun ajaran aktif dalam satu waktu.
  - Validasi keunikan rombel kelas dan pencegahan tumpang tindih penempatan kelas siswa.
  - Validasi keunikan nomor induk siswa (NISN/NIS) dan NIP pegawai.
  - Endpoint RESTful lengkap pada router `/master`: tahun ajaran, kelas, pegawai, siswa, penempatan siswa (`/enrollments`), dan penugasan guru (`/assignments`).
- Pengujian unit master data `backend/tests/test_master_data.py` (4 skenario lulus).

---

## [BE-M4] - Attendance Module & Bulk History
**Tanggal:** 12 November 2026

### Ditambahkan:
- Modul `backend/apps/attendance/`:
  - Model `Attendance` dengan pelacakan audit riwayat snapshot otomatis menggunakan `HistoricalRecords` (`historical_attendances`).
  - Skema migrasi `0001_initial.py` pada tabel `attendances` dan `historical_attendances`.
  - Layanan penyimpanan absensi massal atomik (`save_bulk_attendance`) dengan all-or-nothing rollback (BE-04).
  - Validasi batas tanggal absensi tidak boleh melebihi tanggal hari ini.
  - Validasi wewenang penugasan kelas guru pengampu (`ClassAssignment`) dengan penolakan 403 bagi guru di luar kelas (BE-03).
  - Perekaman snapshot riwayat audit menggunakan `bulk_create_with_history` dan `bulk_update_with_history` (BE-05).
  - Endpoint rekapitulasi kehadiran dan roster kelas pada router `/attendance`.
- Pengujian unit absensi `backend/tests/test_attendance.py` (4 skenario lulus).

---

## [BE-M5] - Student Affairs & Case Timeline
**Tanggal:** 12 November 2026

### Ditambahkan:
- Modul `backend/apps/student_affairs/`:
  - Model `StudentCase` dengan kolom `version` untuk kontrol konkurensi optimistik dan model `CaseEvent` untuk jejak kronologis penanganan siswa.
  - Skema migrasi `0001_initial.py`.
  - Mesin status kasus (`BARU` -> `DIPROSES` -> `SELESAI` / `DIBATALKAN`) dengan aksi terstruktur.
  - Penegakan kontrol konkurensi optimistik: mendeteksi ketidaksesuaian `expected_version` dan mengembalikan respons HTTP 409 Conflict (BE-06).
  - Pembatasan cakupan objek privasi: Wali Kelas hanya dapat mengakses rekam kasus siswa pada kelas perwaliannya.
  - Endpoint pada router `/student-affairs` (`listStudentCases`, `createStudentCase`, `getStudentCaseDetail`, `transitionStudentCase`).
- Pengujian unit kesiswaan `backend/tests/test_student_affairs.py` (3 skenario lulus).

---

## [BE-M6] - Administration & Private Documents
**Tanggal:** 13 November 2026

### Ditambahkan:
- Modul `backend/apps/administration/`:
  - Model `ServiceType`, `ServiceRequest` (dengan kolom `version`), `ServiceEvent`, dan `Document`.
  - Skema migrasi `0001_initial.py`.
  - Mesin status permohonan persuratan tata usaha (`DIAJUKAN` -> `DIPROSES` -> `MENUNGGU_PERSETUJUAN` -> `DISETUJUI` / `DITOLAK` -> `SELESAI`).
  - Validasi berkas lampiran dengan inspeksi magic bytes header biner (`%PDF-`, `\xff\xd8\xff`, `\x89PNG\r\n\x1a\n`) dan batas ukuran 5 MB; berkas tidak sah ditolak HTTP 422 (BE-07).
  - Penyimpanan berkas privat terisolasi pada `PRIVATE_MEDIA_ROOT` menggunakan random UUID `storage_key`.
  - Endpoint aliran berkas terproteksi `GET /api/administration/documents/{id}/download` dengan pengecekan otorisasi ketat (BE-08).
  - Endpoint permohonan surat dan jenis layanan pada router `/administration`.
- Pengujian unit administrasi `backend/tests/test_administration.py` (5 skenario lulus).

---

## [BE-M7] - Dashboard Aggregations, Reporting & Redis Cache
**Tanggal:** 13 November 2026

### Ditambahkan:
- Modul `backend/apps/reports/`:
  - Skema agregasi metrik peran `DashboardMetricsResponse` dan log audit `AuditLogListResponse`.
  - Selector dashboard `get_dashboard_metrics` teragregasi dinamis berdasarkan peran (Admin, Pimpinan, Tata Usaha, Guru, Kesiswaan) (BE-09).
  - Lapisan caching Redis dengan TTL 5 menit dan helper invalidasi otomatis saat mutasi data.
  - Layanan pembuatan spreadsheet Excel rekap kehadiran siswa menggunakan `openpyxl` dengan tema visual Institusional Navy (`#1E3A8A`) (BE-10).
  - Layanan pembuatan dokumen resmi PDF permohonan surat tata usaha menggunakan `reportlab` (BE-10).
  - Endpoint router `/reports` (`/dashboard`, `/attendance.xlsx`, `/administration.pdf`) dan `/audit-logs`.
- Pengujian unit laporan dan audit `backend/tests/test_reports.py` (4 skenario lulus).

---

## [BE-M8] - Backend Hardening, Security Audit & Final Integration
**Tanggal:** 13 November 2026

### Ditambahkan:
- Rangkaian pengujian integrasi ujung ke ujung (`backend/tests/test_e2e.py`) mencakup lima skenario utama:
  - **Skenario A:** Siklus akademik penuh (Tahun Ajaran -> Kelas -> Siswa -> Penempatan -> Penugasan Guru -> Absensi Massal -> Verifikasi Snapshot Audit).
  - **Skenario B:** Penanganan kasus kesiswaan (Pelaporan Kasus -> Konseling Bimbingan -> Pencatatan Tindakan -> Penyelesaian Kasus).
  - **Skenario C:** Siklus permohonan surat tata usaha (Pengajuan -> Verifikasi TU -> Upload Berkas PDF Magic Bytes -> Persetujuan Kepala Sekolah -> Penyelesaian -> Unduh Aliran Berkas Privat).
  - **Skenario D:** Batas keamanan IDOR dan pembatasan hak lintas peran (Guru ditolak buat surat, TU ditolak isi absensi, Guru ditolak isi absensi kelas lain, Guru ditolak unduh berkas privat, Kesiswaan ditolak lihat log audit).
  - **Skenario E:** Penanganan konflik konkurensi (Optimistic Locking race condition) pada kasus dan permohonan surat (HTTP 409).
- Audit kesesuaian kontrak OpenAPI 100% (seluruh 49 operasi dan 71 skema data terverifikasi identik).
- Audit pencegahan kueri N+1 pada seluruh kueri ORM.
- Sanitasi data rahasia pada seluruh modul logging.
- Dokumentasi master final: `backend/BACKEND_IMPLEMENTATION_REPORT.md` dan `backend/BACKEND_CHANGELOG.md`.
- Pembaruan status koordinasi pada `coordination/BACKEND_STATUS.md`.
