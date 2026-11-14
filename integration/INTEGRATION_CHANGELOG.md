# Integration Track Changelog

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Dokumen ini mencatat seluruh riwayat pembaruan, verifikasi integrasi sistem, rekonsiliasi kontrak, dan pencapaian gerbang rilis (release gates) secara kronologis pada lintasan integrasi (Integration Track).

---

## [INT-M8.1 Addendum] - 2026-11-14

### Status Kesiapan
`READY — RELEASE_CANDIDATE_VERIFIED_FOR_RESEARCH_DEMONSTRATION`

### Ringkasan Eksekutif
Audit komprehensif, implementasi, dan pengerasan manajemen konfigurasi environment terpusat (Centralized Environment Configuration & Secret Management) sesuai amanat TRD Bab 9. Seluruh konfigurasi koneksi database, Redis, URL API, port, CORS, private storage, dan secrets dikelola secara terpusat melalui environment variables dengan validasi fail-fast saat startup, proteksi kebocoran kredensial ke Git dan client bundle, serta isolasi database pengujian.

### Environment & Secret Management Enhancements
- **Backend Centralized Configuration Loader & Fail-Fast Validator:**
  - Pembuatan modul `backend/config/env.py` dengan fungsi `load_environment()` dan `validate_environment()`.
  - Hierarki pemuatan fleksibel: variabel `ENV_FILE` (prioritas utama), `.env.production`, `.env.integration`, atau `.env` standar.
  - Validasi fail-fast saat inisialisasi Django: menolak `SECRET_KEY` tidak aman atau < 32 karakter pada production, melarang `DEBUG=True` pada production, melarang wildcard host pada production, memvalidasi skema URL database (`sqlite` atau `postgresql`), serta menegakkan kebijakan fail-closed dengan mewajibkan `REDIS_URL` pada mode `integration` dan `production`.
  - Isolasi konfigurasi test runner database melalui `DATABASES["default"]["TEST"]` pada `backend/config/settings.py` untuk mencegah polusi database operasional.
  - Penambahan dukungan `CACHE_KEY_PREFIX` dan pembersihan deklarasi redundan `PRIVATE_MEDIA_ROOT`.
- **Frontend API URL Normalization & Secret Leakage Prevention:**
  - Implementasi fungsi sentral `resolveApiBaseUrl(raw?: string)` pada `frontend/src/lib/api-client.ts`: normalisasi trailing slash, penambahan otomatis path `/api` pada origin root, dan fallback aman ke `/api`.
  - Penambahan Axios request interceptor untuk memangkas prefix duplikat `/api` (mencegah kesalahan HTTP 404 `/api/api/...`).
  - Isolasi variabel dev server `BACKEND_PROXY_TARGET` pada `frontend/vite.config.ts` via `loadEnv(mode, process.cwd(), '')` tanpa bocor ke client-side JavaScript bundle browser.
  - Pengaturan Playwright dinamis melalui `process.env.PLAYWRIGHT_BASE_URL` dengan fallback ke `http://localhost:3000`.
- **Integration Test Runners Centralization:**
  - Pembuatan modul sentral `integration/config.py` yang membaca `BASE_URL`, `PROXY_URL`, `DATABASE_URL`, dan `REDIS_URL` dari environment variables tanpa hardcoded credentials.
- **Git Protection & Environment Templates:**
  - Pembaruan root `.gitignore` dengan aturan pengecualian `!.env.*.example`, menjamin seluruh template contoh terlacak di Git sementara seluruh file rahasia `.env` dan `.env.integration` terabaikan.
  - Penyediaan template environment lengkap dan bersih dari rahasia riil:
    - `backend/.env` (development SQLite WAL + Redis) & `backend/.env.example`
    - `backend/.env.integration` (PostgreSQL WSL2 + Redis) & `backend/.env.integration.example`
    - `frontend/.env` (Vite dev proxy) & `frontend/.env.example` & `frontend/.env.production.example`

### Test Suite Execution Summary
- **Backend Environment Regression Suite:** 11/11 tests PASSED (`backend/tests/test_environment_config.py`).
- **Backend Full Pytest Suite:** 111 tests (110 PASSED, 1 SKIPPED dual-engine conditional).
- **PostgreSQL Live Database Test Suite:** 17 PASSED, 1 SKIPPED dalam 5.70s.
- **Frontend Vitest Suite:** 74 tests PASSED across 15 test files (100%), termasuk verifikasi proteksi kebocoran secret pada client bundle (`frontend/tests/unit/api-client.test.ts`).
- **Frontend Build & Typecheck:** `tsc --noEmit` 0 errors; Vite production build lulus dalam 9.00s.
- **Playwright E2E Browser Suite:** 6/6 tests PASSED (13.9s) across 6 roles.
- **Integration Master Runner:** 8 milestone gates + 20 Cross-Module N2N checks PASSED 100%.

---

## [INT-M8.1] - 2026-11-14

### Status Kesiapan
`READY — RELEASE_CANDIDATE_VERIFIED_FOR_RESEARCH_DEMONSTRATION`

### Ringkasan Eksekutif
Penyelesaian evaluasi independen, penutupan seluruh temuan keamanan kritis P0, penegakan otorisasi least privilege pada PostgreSQL, sinkronisasi kanonikal kontrak OpenAPI v1.1.0 (hash `F1618EB80154D970F639A5617AD645D3A37D139A9CC6B90AFA8E4E054A10B72B`), implementasi pencegahan lost-update presensi massal (CCR-20261114-01) di backend dan frontend, verifikasi runtime produksi Granian ASGI, serta pengujian distributed shared state multi-worker riil via Redis 7.

### Security & Compliance Remediations (P0)
- **Database Credential Exposure Remediation:** String koneksi plaintext pada dokumentasi integrasi disunting menjadi `<REDACTED>`; file `.env.example` terverifikasi bebas dari kredensial riil.
- **PostgreSQL Least Privilege Enforcement:** Atribut `SUPERUSER` pada role basis data `test_be_user` telah dicabut melalui perintah `ALTER USER test_be_user NOSUPERUSER;`. Verifikasi `\du` membuktikan akun hanya memiliki hak `Create DB` untuk test runner, sepenuhnya mematuhi prinsip least privilege.
- **Counseling Privacy & DEC-TECH-18 Enforcement:** Matriks otorisasi negatif pada endpoint `/api/student-affairs/cases/{id}` diverifikasi secara ketat. Peran Pimpinan (`kepsek`) dan Administrator (`admin`) secara tegas ditolak (HTTP 403 Forbidden). Wali Kelas hanya dapat melihat kasus pada rombel binaannya dengan catatan konseling disamarkan (`[Catatan konseling privat - Terproteksi]`). Hanya peran Kesiswaan yang berhak membaca catatan konseling privat asli. Uji canary string membuktikan 0% kebocoran.

### Contract & Concurrency Enhancements
- **OpenAPI v1.1.0 Synchronization:** Kontrak `contracts/openapi.v1.yaml` disinkronkan dengan CCR-20261114-01: penambahan field `roster_version` pada `AttendanceRosterResponse`, field `expected_roster_version` pada `AttendanceBulkRequest`, dan deklarasi respon HTTP 409 Conflict. Hash kanonikal baru: `F1618EB80154D970F639A5617AD645D3A37D139A9CC6B90AFA8E4E054A10B72B`.
- **Backend Concurrency Guard:** Fungsi `save_bulk_attendance` dilengkapi dengan sinkronisasi thread dan transaksi atomik untuk mencegah lost-update pada presensi massal, mengembalikan HTTP 409 CONCURRENCY_CONFLICT ketika versi roster kedaluwarsa tanpa mengalami deadlock penguncian SQLite.
- **Frontend Conflict Recovery:** Antarmuka `RecordAttendancePage.tsx` mengirimkan `expected_roster_version`, menangani respon HTTP 409 secara elegan dengan mempertahankan draft formulir siswa, menampilkan banner peringatan "Konflik Konkurensi Terdeteksi", dan menyediakan tombol "Muat Ulang Roster".
- **Frontend Code Generation:** Tipe data TypeScript `src/types/api.generated.ts` digenerasi ulang secara otomatis dari kontrak kanonikal OpenAPI v1.1.0 (`npm run generate:api`).

### Runtime & Infrastructure Verification
- **Granian ASGI Production Runtime:** Server backend dijalankan menggunakan Granian 2.8.8 ASGI (`--interface asginl`) pada port 8000 dengan integrasi Redis aktif, mengeliminasi warning lifespan dan memberikan performa tinggi.
- **Real Multi-Worker Shared State Verification:** Skrip `integration/test_live_multi_worker.py` mengeksekusi 9 skenario terdistribusi pada dua worker Granian independen (port 8001 dan port 8002) yang terhubung ke Redis 6379:
  1. Validasi sesi lintas worker (Worker A login -> Worker B verifikasi via `/api/auth/me`).
  2. Propagasi blacklist logout lintas worker (Worker A logout -> Worker B menolak token via HTTP 401).
  3. Single-use refresh token rotation (Worker A memutar token -> Worker B menolak token lama via HTTP 401).
  4. Invalidation token family saat refresh replay terdeteksi.
  5. Pencatatan counter brute-force terdistribusi secara global di Redis.
- **Dual-Engine Compatibility:** Pengujian backend terbukti kompatibel penuh pada dua mesin database: SQLite WAL mode (pengembangan lokal) dan PostgreSQL 16.15 WSL2 / PostgreSQL 17 (integrasi/produksi).

### Test Suite Execution Summary
- **Backend Pytest:** 100 tests (99 PASSED, 1 SKIPPED dual-engine conditional).
- **Frontend Vitest:** 71 tests PASSED across 15 test files (100%).
- **Playwright E2E Browser:** 6/6 tests PASSED (10.4s) across 6 roles (`admin`, `guru`, `wali_kelas`, `kesiswaan`, `tata_usaha`, `kepsek`) dengan 8 bukti visual di `frontend/evidence/`.
- **Integration Master Runner:** 8 milestone gates + 20 Cross-Module N2N checks PASSED 100%.
- **Live Multi-Worker Suite:** 9/9 verification steps PASSED 100%.
- **Frontend Build & Typecheck:** Vite production build lulus dalam 8.15s; `tsc --noEmit` 0 errors.
- **Dependency Audit:** `pip check` mengonfirmasi 0 broken requirements.

---

## [INT-M8] - 2026-11-14

### Status Kesiapan
`READY — FULL_SYSTEM_INTEGRATION_VERIFIED`

### Ringkasan Eksekutif
Penyelesaian evaluasi integrasi sistem menyeluruh (Full System Integration), pengujian lintas modul (20 Cross-Module N2N checks), pengujian peramban Playwright E2E 6 peran, uji pemulihan bencana (disaster recovery), serta penutupan 18 Quality Gates.

### Added (Penambahan)
- Skrip pengujian otomatis 20 hubungan lintas modul: `integration/test_n2n_cross_module.py`.
- Skrip runner master terpadu: `integration/run_all_integration_tests.py`.
- Skrip benchmark latensi performa HTTP: `integration/benchmark_system_performance.py`.

### Verified (Hasil Verifikasi)
- 20/20 hubungan lintas modul (N2N) lulus verifikasi tanpa anomali.
- 6/6 skenario peramban Playwright E2E browser testing lulus dalam 13.8 detik dengan 8 screenshot evidensi visual di `frontend/evidence/`.
- Hasil benchmark performa mencatat latensi kueri rata-rata p50 antara 2.4 ms s/d 35.2 ms, jauh di bawah batas SLA 200 ms.
- Uji pemulihan data (backup/restore) membuktikan integritas byte-for-byte SHA-256 pada berkas privat dan relasi database 100% konsisten.
- Seluruh gerbang rilis G1 sampai G18 terpenuhi dengan status PASSED.

---

## [INT-M7] - 2026-11-14

### Status Kesiapan
`PASSED — REPORTS_DASHBOARD_AND_CACHE_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang laporan: `integration/test_int_m7_reports.py`.

### Verified (Hasil Verifikasi)
- Endpoint `GET /api/reports/dashboard` mengembalikan metrik teragregasi yang cocok dengan kontrak untuk seluruh 6 peran pengguna (`admin`, `guru`, `wali_kelas`, `kesiswaan`, `tata_usaha`, `kepsek`).
- Ekspor laporan administrasi `GET /api/reports/administration.pdf` menghasilkan file biner PDF valid berheader `%PDF-`.
- Ekspor rekapitulasi presensi `GET /api/reports/attendance.xlsx` menghasilkan file spreadsheet valid berheader ZIP PK.
- Otorisasi least privilege terverifikasi: peran Administrator ditolak (HTTP 403) dari mengunduh rekap presensi akademik siswa.
- Endpoint `GET /api/audit-logs` membatasi akses hanya untuk Administrator; Guru yang mencoba mengakses ditolak dengan HTTP 403 PERMISSION_DENIED.

---

## [INT-M6] - 2026-11-14

### Status Kesiapan
`PASSED — ADMINISTRATION_AND_PRIVATE_DOCUMENTS_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang administrasi: `integration/test_int_m6_administration.py`.

### Verified (Hasil Verifikasi)
- Alur persetujuan surat resmi (Workflow A): TU membuat permohonan (DIAJUKAN), mengunggah berkas PDF, memproses (DIPROSES), mengajukan ke pimpinan (MENUNGGU_PERSETUJUAN), Kepala Sekolah menyetujui (DISETUJUI), dan TU menyelesaikan (SELESAI).
- Alur penolakan surat resmi (Workflow B): Kepala Sekolah menolak permohonan dengan alasan resmi; status DITOLAK terbukti menjadi terminal state (tidak dapat dilanjutkan ke SELESAI).
- Validasi magic bytes: Berkas dengan signature PDF diterima; berkas biner eksekusi/skrip ditolak.
- Isolasi berkas privat: Berkas fisik disimpan di direktori privat (`PRIVATE_MEDIA_ROOT`) dengan UUID storage key; streaming download terproteksi via endpoint `/api/administration/documents/{id}/download`.
- Keamanan IDOR: Pengguna tidak berwenang (Guru) yang mencoba mengunduh dokumen ditolak dengan HTTP 403 PERMISSION_DENIED.

---

## [INT-M5] - 2026-11-14

### Status Kesiapan
`PASSED — STUDENT_AFFAIRS_AND_PRIVACY_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang kesiswaan: `integration/test_int_m5_affairs.py`.

### Verified (Hasil Verifikasi)
- Siklus hidup kasus siswa (Skenario A2): Kesiswaan membuat kasus (BARU), memulai penanganan (DIPROSES), mencatat tindakan bimbingan konseling (CATAT_TINDAKAN), dan menyelesaikan kasus (SELESAI).
- Kontrol konkurensi optimistik: Upaya transisi status dengan versi usang (`expected_version` tidak cocok) ditolak dengan HTTP 409 CONCURRENCY_CONFLICT.
- Penegakan privasi DEC-TECH-18:
  - Catatan konseling rahasia terbaca utuh oleh Kesiswaan dan Pimpinan.
  - Catatan konseling rahasia otomatis disamarkan menjadi `[Catatan konseling privat - Terproteksi]` saat dibaca oleh Wali Kelas atau Guru.
  - Pengujian dengan synthetic canary marker membuktikan 0% kebocoran data sensitif ke peran non-kesiswaan.

---

## [INT-M4] - 2026-11-14

### Status Kesiapan
`PASSED — ATTENDANCE_CONCURRENCY_AND_RECAP_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang presensi: `integration/test_int_m4_attendance.py`.
- Implementasi Contract Change Request `CCR-20261114-01`: penambahan kolom `roster_version` dan `expected_roster_version`.

### Changed (Pembaruan)
- `backend/apps/attendance/services.py`: Mengatur urutan pemeriksaan otorisasi penugasan guru agar dijalankan mendahului pemeriksaan konkurensi roster version untuk mencegah kebocoran informasi ke peran non-guru.

### Verified (Hasil Verifikasi)
- Guru memuat roster presensi kelas penugasannya lengkap dengan nomor versi roster awal (`roster_version`).
- Guru menyimpan presensi massal (bulk attendance) secara atomik; seluruh baris kehadiran tersimpan dan tercatat di tabel audit `HistoricalAttendance`.
- Deteksi benturan konkurensi: Pengiriman presensi massal dengan versi roster usang ditolak dengan HTTP 409 CONCURRENCY_CONFLICT.
- Wali Kelas membaca rekapitulasi kehadiran dengan perhitungan persentase hadir, sakit, izin, dan alpa yang presisi.
- Ekspor Excel presensi menghasilkan file `.xlsx` valid.
- Pengguna tanpa penugasan aktif di kelas ditolak dengan HTTP 403 PERMISSION_DENIED.

---

## [INT-M3] - 2026-11-14

### Status Kesiapan
`PASSED — MASTER_DATA_AND_ACADEMIC_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang master data: `integration/test_int_m3_master_data.py`.

### Verified (Hasil Verifikasi)
- Siklus akun pengguna: Pembuatan akun, pencarian terpaginasi, detail akun, dan penonaktifan/pengaktifan via PATCH `is_active`.
- Siklus tahun ajaran: Validasi integritas memastikan hanya satu tahun ajaran yang boleh berstatus aktif pada satu waktu (single active academic year).
- Siklus rombel kelas: Pembuatan kelas dan pembaruan parsial nama kelas via PATCH `/master/classes/{id}`.
- Siklus pegawai: Pembuatan data pegawai ber-NIP dan pembaruan nama via PATCH `/master/employees/{id}`.
- Siklus siswa: Pembuatan siswa, validasi enum status (AKTIF, LULUS, PINDAH, KELUAR), dan pembaruan status via PATCH `/master/students/{id}`.
- Penempatan dan penugasan: Pendaftaran siswa ke rombel (`/master/enrollments`) dan penugasan guru (`/master/assignments`) dengan tanggal mulai dan tanggal selesai.

---

## [INT-M2] - 2026-11-14

### Status Kesiapan
`PASSED — AUTH_SESSION_AND_RBAC_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang otentikasi: `integration/test_int_m2_auth.py`.

### Verified (Hasil Verifikasi)
- Alur login riil berhasil untuk seluruh 6 peran pengguna (`admin`, `guru`, `wali_kelas`, `kesiswaan`, `tata_usaha`, `kepsek`) menghasilkan JWT access token (15 menit) dan refresh token (7 hari).
- Endpoint `/api/auth/me` mengembalikan profil pengguna, nama, NIP/employee_id, dan daftar peran yang valid.
- Rotasi refresh token atomik: Penggunaan token refresh menerbitkan pasangan baru dan membatalkan token lama.
- Replay protection: Token refresh yang telah diputar ditolak dengan HTTP 401 saat digunakan ulang.
- Pencabutan sesi logout (`POST /api/auth/logout`): Token dimasukkan ke blacklist Redis/DB dan tidak dapat digunakan kembali.
- Pembatasan tingkat percobaan (rate limiting): Brute force login dicegah melalui `LoginRateLimiter` dengan pembatasan percobaan gagal.
- Penegakan least privilege RBAC: Guru ditolak mengakses manajemen akun (HTTP 403 PERMISSION_DENIED), Administrator diizinkan (HTTP 200).

---

## [INT-M1] - 2026-11-14

### Status Kesiapan
`PASSED — FOUNDATION_AND_INFRASTRUCTURE_GATE`

### Added (Penambahan)
- Skrip verifikasi integrasi gerbang fondasi: `integration/test_int_m1_foundation.py`.

### Verified (Hasil Verifikasi)
- Endpoint healthcheck `/api/health` merespons HTTP 200 dengan status `ok`, versi `1.1.0`, dan nama servis `sie-sman1-bunut-backend`.
- Header `X-Request-ID` terpropagasi secara konsisten baik direct (port 8000) maupun melalui reverse proxy Vite (port 3000).
- Permintaan CORS preflight (`OPTIONS /api/auth/login`) mengembalikan header `Access-Control-Allow-Origin: http://localhost:3000` dan izin metode HTTP.
- Format ErrorEnvelope terverifikasi konsisten pada respon 401 Unauthorized, 404 Not Found, dan 422 Unprocessable Entity (memuat `code`, `message`, `details`, `request_id`).

---

## [INT-M0] - 2026-11-14

### Status Kesiapan
`CONDITIONALLY_READY — INTEGRATION_PREFLIGHT_WITH_OPEN_BLOCKERS`

### Ringkasan Eksekutif
Pelaksanaan audit pra-terbang (system integration preflight) dan verifikasi baseline lintas backend, frontend, kontrak bersama, serta lingkungan runtime sebelum pelaksanaan gerbang integrasi berjenjang (INT-M1 s/d INT-M8).
Semua blocker pra-terbang telah diselesaikan pada tahapan INT-M1 s/d INT-M8 berikutnya.
