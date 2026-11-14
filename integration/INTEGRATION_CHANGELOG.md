# Integration Track Changelog

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Dokumen ini mencatat seluruh riwayat pembaruan, verifikasi integrasi sistem, rekonsiliasi kontrak, dan pencapaian gerbang rilis (*release gates*) secara kronologis pada lintasan integrasi (*Integration Track*).

---

## [INT-M0] - 2026-11-14

### Status Kesiapan
`CONDITIONALLY_READY — INTEGRATION_PREFLIGHT_WITH_OPEN_BLOCKERS`

### Ringkasan Eksekutif
Pelaksanaan audit pra-terbang (*system integration preflight*) dan verifikasi baseline lintas backend, frontend, kontrak bersama, serta lingkungan runtime sebelum pelaksanaan gerbang integrasi berjenjang (INT-M1 s/d INT-M8).

### Added (Penambahan)
- Direktori master integrasi `integration/` sebagai wadah resmi artefak pelaporan lintasan integrasi.
- Berkas master `integration/INTEGRATION_IMPLEMENTATION_REPORT.md` yang memuat 11 bab komprehensif analisis kesiapan pra-terbang, audit kontrak, verifikasi infrastruktur runtime, bukti HTTP preflight, matriks rencana pengujian 12 domain bisnis, dan evaluasi 18 quality gates.
- Berkas master `integration/INTEGRATION_CHANGELOG.md` untuk melacak seluruh histori rilis integrasi.
- Matriks pengujian integrasi berjenjang 12 domain bisnis mencakup: Autentikasi, Manajemen Akun, Master Akademik, Master Pegawai & Penugasan, Master Siswa & Enrollment, Presensi Harian, Rekap Presensi, Kasus Kesiswaan, Konseling Rahasia, Permohonan Surat, Persetujuan Pimpinan, serta Unduh Berkas Privat & Laporan.

### Verified (Hasil Verifikasi Baseline)
- **Baseline Backend (Django Ninja):**
  - 93/93 pengujian otomatis lulus 100% via pytest (`backend/tests`) dalam 36.48 detik.
  - Linter Ruff check lulus dengan status `All checks passed!` (exit code 0).
  - Ruff format check mengonfirmasi 79 berkas telah rapi terformat (exit code 0).
- **Baseline Frontend (React Vite TypeScript):**
  - 71/71 pengujian otomatis lulus 100% via Vitest pada 15 berkas uji dalam 24.93 detik.
  - TypeScript typecheck (`tsc --noEmit`) menghasilkan 0 kesalahan diagnostik (exit code 0).
  - Prettier format check mengonfirmasi seluruh berkas `src/**/*.{ts,tsx,css}` telah rapi sesuai standar kode.
  - Production build (`vite build`) berhasil dalam 11.43 detik dengan seluruh bundle terpecah modular di bawah 500 kB.
  - 6/6 skenario Playwright E2E browser testing (Chromium) lulus 100% untuk seluruh 6 peran pengguna (`admin`, `guru`, `wali_kelas`, `kesiswaan`, `tata_usaha`, `kepsek`) dalam 16.3 detik, dengan 8 bukti tangkapan layar di `frontend/evidence/`.
- **Konektivitas Live HTTP Socket:**
  - Endpoint healthcheck `/api/health` merespons HTTP 200 dengan propagasi header `X-Request-ID` secara direct (port 8000) maupun melalui reverse proxy Vite (port 3000).
  - Rute terproteksi `/api/auth/me` mengembalikan HTTP 401 Unauthorized dengan skema ErrorEnvelope saat diakses tanpa token.
  - Alur login riil untuk 6 akun peran pengguna mengembalikan HTTP 200, JWT access/refresh token, dan profil peran yang akurat.
  - Rotasi refresh token atomik diverifikasi sukses menerbitkan pasangan token baru.
  - Uji otorisasi negatif (Guru mengakses `/accounts/users`) menghasilkan HTTP 403 Forbidden dengan kode `PERMISSION_DENIED`.
  - Uji otorisasi positif (Administrator mengakses `/accounts/users`) menghasilkan HTTP 200 dengan data terpaginasi.
  - Pencabutan sesi logout (`POST /api/auth/logout`) berhasil memasukkan token ke blacklist, dan verifikasi susulan ke `/auth/me` mengembalikan HTTP 401 AUTHENTICATION_FAILED.
- **Rekonsiliasi Kontrak OpenAPI v1.1.0:**
  - Checksum kanonikal SHA-256 `D3871BA834C17FC6DC49BB92F63391EB3EC63571E784A6623CE8E2A65CB52B9E` terkonfirmasi presisi memuat 37 paths, 49 operasi bisnis, dan 71 skema komponen.
  - Checksum database DBML SHA-256 `DA7B35DBBFC0DF1080DD40A93E4DB01D97CEB568EDF31EE3A97E1CAF723603B8` terkonfirmasi sinkron 18 tabel fisik.

### Blockers & Open Items (Catatan Terbuka)
- **Host PostgreSQL 17 (Gate G7):** Layanan PostgreSQL 17 aktif di Windows host port 5432 tetapi mewajibkan autentikasi password `scram-sha-256`. Kredensial tidak disediakan dalam repositori. Arsitektur dual-engine SQLite WAL mode dipertahankan untuk lingkungan pengembangan lokal.
- **Host Redis Persisten (Gate G8):** Layanan Redis aktif di WSL2 port 6379, namun host dev server default ke `LocMemCache` dengan kebijakan fail-closed pada keamanan sesi dan fail-open pada cache kueri non-kritis.
- **Attendance Bulk Request Versioning:** Skema `AttendanceBulkRequest` di OpenAPI v1.1.0 belum menyertakan field `expected_version`. Kebutuhan ini diteruskan ke Coordinator untuk evaluasi Contract Change Request jika kebijakan sekolah mewajibkan deteksi benturan presensi baris rombel seketika.
