# Integration Track Changelog

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Dokumen ini mencatat seluruh riwayat pembaruan, verifikasi integrasi sistem, rekonsiliasi kontrak, dan pencapaian gerbang rilis (release gates) secara kronologis pada lintasan integrasi (Integration Track).

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
