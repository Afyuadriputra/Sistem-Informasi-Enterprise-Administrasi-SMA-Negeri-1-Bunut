# Backend Changelog - Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Seluruh catatan pembaruan teknis pada pengembangan backend dari milestone BE-M1 hingga BE-M9 dicatat secara kronologis dalam dokumen ini.

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

---

## [BE-M9] - Independent Backend Verification, Security Hardening & Performance Validation
**Tanggal:** 13 November 2026

### Ditambahkan:
- Rangkaian pengujian otomatis baru (41 pengujian baru, total 78 pengujian lulus 100%):
  - `backend/tests/test_contract.py` (4 tes): Hash SHA-256 kontrak, integritas DBML, verifikasi 49/49 operasi OpenAPI, 19/19 operasi master data termasuk DEC-TECH-16 PATCH endpoints.
  - `backend/tests/test_jwt_security.py` (9 tes): Validasi access token, expired token 401, signature & format malformed 401, pencegahan pencampuran jenis token, rotasi refresh token dengan deteksi reuse token family, pencabutan sesi logout (access JTI & refresh JTI), blokir akun nonaktif, pencegahan lockout admin terakhir & self-deactivation, login brute-force rate limiter (429).
  - `backend/tests/test_rbac_matrix.py` (4 tes): Log audit strictly Administrator, persetujuan surat strictly Pimpinan, simpan absensi massal strictly Guru pengampu aktif, ekspor laporan strictly peran berwenang.
  - `backend/tests/test_privacy_dec_tech_18.py` (5 tes): Server-side masking catatan konseling untuk Wali Kelas, catatan terbuka untuk Kesiswaan, penolakan Wali Kelas luar perwalian (403), penolakan Administrator murni tanpa peran fungsional (403), validasi catatan wajib pada aksi CATAT_TINDAKAN (422).
  - `backend/tests/test_state_machines.py` (4 tes): Siklus hidup kasus siswa lengkap & terminal state, optimistic locking 409 pada kasus siswa, siklus hidup permohonan surat tata usaha lengkap, rejection terminal state.
  - `backend/tests/test_private_files.py` (5 tes): Penolakan berkas 0-byte (422), sanitasi path traversal pada nama file, penolakan spoofing tipe berkas via inspeksi magic bytes biner (422), penolakan berkas >5 MB (422), kontrol otorisasi unduh berkas privat.
  - `backend/tests/test_concurrency.py` (2 tes): Simulasi multi-threaded ThreadPoolExecutor pengujian race condition optimistic concurrency control pada mutasi kasus siswa dan permohonan persuratan (HTTP 409).
  - `backend/tests/test_query_optimization.py` (5 tes): Eliminasi kueri N+1 pada daftar kasus kesiswaan, kueri terikat konstan pada daftar siswa, rekap absensi, dan daftar permohonan persuratan, serta verifikasi 0 kueri basis data domain pada dashboard warm cache.
  - `backend/tests/test_performance.py` (3 tes): Pengukuran latensi login p95 < 2000 ms, cache dashboard p95 < 200 ms, dan simpan absensi massal 30 siswa < 1000 ms.
- Penguatan Keamanan & Arsitektur:
  - Penghapusan universal Administrator bypass di `apps/core/security.py`, `apps/attendance/services.py`, `apps/student_affairs/selectors.py`, `apps/reports/services.py`.
  - Pelacakan `family_id` pada rotasi JWT refresh token dan invalidasi famili otomatis saat deteksi token reuse replay attack.
  - Penambahan tracking `request.token_jti` dan pencabutan access token JTI serta refresh token pada logout.
  - Penambahan `Prefetch("student__enrollments", ...)` pada `apps/student_affairs/selectors.py` untuk mengeliminasi kueri N+1.
  - Sanitasi formula injection spreadsheet (CWE-1236) pada `apps/reports/services.py` dan penyelarasan tema warna Institusional Navy `#173B63`.
  - Penanganan pengecualian global untuk SQLite `OperationalError: database table is locked` yang dipetakan ke HTTP 409 `CONCURRENCY_CONFLICT`.
  - Hooking `transaction.on_commit(invalidate_dashboard_cache)` pada mutasi akun, siswa, enrollment, absensi, dan permohonan surat.
- Dokumentasi:
  - Pembaruan laporan master `backend/BACKEND_IMPLEMENTATION_REPORT.md` dengan Bab 21 dan evaluasi 18 Acceptance Gates (G1 - G18).
  - Pembaruan status pelacakan pada `coordination/BACKEND_STATUS.md`.

---

## [BE-M9.1] - Infrastructure Verification, Concurrency Hardening & Final Backend Closure
**Tanggal:** 13 November 2026

### Ditambahkan & Diperbarui:
- **Ekspansi Rangkaian Pengujian Otomatis (15 pengujian baru, total 93 pengujian lulus 100%):**
  - `backend/tests/test_backup_restore.py` (1 tes): Pengujian disaster recovery sintesis untuk pencadangan dan pemulihan data (`dumpdata`/`loaddata`) serta pemulihan berkas privat fisik dengan verifikasi integritas hash SHA-256 byte-for-byte.
  - `backend/tests/test_real_http_granian.py` (1 tes): Pengujian smoke test HTTP soket riil menggunakan server ASGI Granian pada ephemeral port dinamis melalui panggilan `urllib.request` langsung ke `/api/health`, `/api/auth/login`, dan endpoint 404.
  - `backend/tests/test_concurrency.py` (ekspansi dari 2 menjadi 6 tes):
    - Pengujian multi-threaded race condition rotasi token penyegaran JWT atomik via `ThreadPoolExecutor`.
    - Pengujian persaingan konkurensi aktivasi tahun ajaran ganda (menjamin tepat 1 tahun ajaran aktif).
    - Pengujian pencegahan penonaktifan admin terakhir secara konkruen (menjamin tidak ada admin lockout).
    - Audit kesesuaian kontrak absensi massal terhadap pembaruan basi (*stale update audit*).
  - `backend/tests/test_contract.py` (ekspansi dari 4 menjadi 8 tes):
    - Verifikasi operasional endpoint pemantauan `/api/health` dengan penanganan tag sistem.
    - Validasi kepatuhan skema global `ErrorEnvelope` (`code`, `message`, `details`, `request_id`).
    - Validasi kontrak media type biner dan multipart/form-data (`/administration/requests/{id}/documents`, `/reports/attendance.xlsx`, `/reports/administration.pdf`).
    - Validasi runtime envelope kesalahan pada endpoint API riil (HTTP 401, 404, 422).
  - `backend/tests/test_privacy_dec_tech_18.py` (ekspansi dari 5 menjadi 6 tes):
    - Audit kebocoran privasi bimbingan konseling menggunakan synthetic canary marker (`MARKER_SECRET_COUNSELING_TRAUMA_CONFIDENTIAL_9988`), membuktikan zero leakage pada daftar kasus, detail perwalian, dan log aktivitas.
  - `backend/tests/test_private_files.py` (ekspansi dari 5 menjadi 6 tes):
    - Pengujian pembersihan berkas yatim (*orphan file cleanup*) saat kegagalan transaksi database atau pembatalan unggahan berkas privat.
  - `backend/tests/test_performance.py` (ekspansi dari 3 menjadi 5 tes):
    - Pengukuran latensi daftar siswa dan roster absensi (p95 < 250 ms).
    - Pengukuran latensi ekspor laporan biner Excel dan PDF (p95 < 1000 ms).
  - `backend/tests/test_core.py` (ekspansi dari 5 menjadi 6 tes):
    - Pengujian pemetaan pengecualian database lock SQLite `OperationalError` ke HTTP 409 `CONCURRENCY_CONFLICT`.
  - `backend/tests/conftest.py`:
    - Penambahan fixture autouse `test_private_media_root` yang mengisolasi `PRIVATE_MEDIA_ROOT` pengujian ke direktori sementara `tmp_path`, mencegah polusi berkas pada working tree.

- **Penguatan Keamanan & Kontrol Konkurensi:**
  - Penambahan operasi atomik `cache.add(f"blacklist:{jti}", True)` pada `backend/apps/accounts/services.py:rotate_refresh_token` untuk mengeliminasi celah race condition check-then-act pada rotasi token penyegaran JWT.

- **Verifikasi Infrastruktur & Keselarasan Skema Basis Data:**
  - Verifikasi tabel fisik basis data `school_classes` dan `enrollments` terbukti 100% selaras dengan baris 155 dan 185 pada `contracts/database.dbml`, menuntaskan rekonsiliasi deskriptif masa lalu.
  - Verifikasi PostgreSQL 17 pada host Windows (port 5432) dengan `psycopg 3.3.9`; autentikasi menggunakan `scram-sha-256`. Gate G7 dinyatakan BLOCKED untuk koneksi live host tanpa kata sandi pengguna; dual-engine SQLite WAL mode terverifikasi 100%.
  - Verifikasi Redis 7.0.15; ketiadaan daemon host Windows port 6379 mendasari sertifikasi Gate G8 sebagai BLOCKED untuk soket live host. Kebijakan fail-closed (sesi dan rate limiter) serta fail-open (cache) terverifikasi.

- **Rekonsiliasi Dokumentasi Master:**
  - Rekonsiliasi kontradiksi historis pada Bagian 1-20 `backend/BACKEND_IMPLEMENTATION_REPORT.md` agar konsisten dengan evaluasi Bab 21 dan penambahan Bab 22.
  - Status kesiapan backend final disertifikasi sebagai `CONDITIONALLY_READY — BACKEND_IMPLEMENTED_WITH_VERIFICATION_BLOCKERS` (16 PASS, 2 BLOCKED pada lingkungan infrastruktur host eksternal).

