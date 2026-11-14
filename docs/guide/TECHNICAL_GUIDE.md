# PANDUAN TEKNIS OPERASIONAL SISTEM (TECHNICAL GUIDE)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Dokumen ini merupakan panduan teknis komprehensif untuk pengembang, administrator sistem, dan evaluator penelitian dalam menjalankan, mengonfigurasi, mengisi basis data, dan memelihara aplikasi Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut pada lingkungan lokal.

---

## BAB 1 - Gambaran Sistem

### 1.1 Identitas dan Tujuan Aplikasi
Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut adalah aplikasi web terintegrasi skala enterprise yang dirancang untuk mengotomatisasi proses bisnis administrasi sekolah, mencakup pengelolaan data master akademik, pencatatan presensi siswa harian, bimbingan dan penanganan kasus kesiswaan dengan perlindungan privasi konseling, serta pelayanan permohonan persuratan tata usaha dengan antrean persetujuan pimpinan.

### 1.2 Arsitektur Sistem
Aplikasi menerapkan arsitektur **Modular Monolith Django Ninja** di backend dan **SPA React TypeScript Atomic Design** di frontend dengan pendekatan **Contract-First Development**:
- **Backend**: Django 5.2 dengan Django Ninja ASGI (skema validasi berbasis Pydantic), arsitektur berlapis (Routers/API -> Services/Selectors -> Models), PostgreSQL / SQLite dengan SQLite WAL mode, Redis 7 untuk caching dan token blacklist revocation.
- **Frontend**: Single Page Application berbasis React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui (Radix UI primitives), TanStack Query v5 untuk server state caching, Zustand untuk client authentication state, dan React Router v6.
- **Pemisah Kontrak**: OpenAPI v1.1.0 (`contracts/openapi.v1.yaml`) dan skema data DBML (`contracts/database.dbml`).

### 1.3 Struktur Proyek
```text
PROJEK istri bg givo/
├── backend/                  # Django Ninja Modular Monolith
│   ├── apps/
│   │   ├── accounts/         # Autentikasi JWT, Pengguna, Peran RBAC
│   │   ├── master_data/      # Tahun Ajaran, Rombel, Siswa, Pegawai, Penugasan
│   │   ├── attendance/       # Presensi Roster, Rekapitulasi, Transaksi Massal
│   │   ├── student_affairs/  # Kasus Kesiswaan, Timeline, Privasi Konseling
│   │   ├── administration/   # Jenis Layanan, Permohonan Surat, Dokumen Privat
│   │   ├── reports/          # Ekspor PDF (ReportLab) & Excel (OpenPyXL)
│   │   └── core/             # Middleware, Security, Seeder Command, Exceptions
│   ├── config/               # Django Settings & ASGI Application
│   ├── private_media/        # Penyimpanan fisik dokumen privat terproteksi
│   └── tests/                # 115 Automated Pytest Test Suite
├── frontend/                 # React Vite TypeScript Atomic Design SPA
│   ├── src/
│   │   ├── components/       # Atoms, Molecules, Organisms, Templates
│   │   ├── pages/            # 18 Screen Groups & 6 Role Dashboards
│   │   ├── lib/              # API Client (Axios), Auth Store, Formatters
│   │   └── types/            # TypeScript Interface selaras OpenAPI
│   └── tests/                # 74 Vitest Unit Tests & 7 Playwright E2E Tests
├── contracts/                # OpenAPI v1.1.0 & Database DBML
├── integration/              # Script Verifikasi Integrasi INT-M1 s/d INT-M8
├── scripts/                  # start-local.ps1 helper startup
└── docs/guide/               # TECHNICAL_GUIDE.md, USER_GUIDE.md, ACCOUNTS.local.md
```

---

## BAB 2 - Quick Start

Langkah cepat berikut dapat digunakan untuk menjalankan seluruh subsistem dalam waktu kurang dari 2 menit.

### Langkah 1: Pastikan Redis Aktif (WSL2 Ubuntu)
```powershell
wsl -d Ubuntu -- redis-cli ping
# Jika belum aktif, jalankan:
wsl -d Ubuntu -- sudo service redis-server start
```
Respons wajib: `PONG`.

### Langkah 2: Jalankan Backend (Terminal 1)
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo"
$env:REDIS_URL="redis://127.0.0.1:6379/1"
backend\.venv\Scripts\granian.exe --interface asginl config.asgi:application --working-dir backend --host 127.0.0.1 --port 8000
```
Verifikasi status backend melalui browser: `http://127.0.0.1:8000/api/health` (respons `{"status":"ok"}`).

### Langkah 3: Jalankan Frontend (Terminal 2)
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend"
npm run dev
```

### Langkah 4: Buka Aplikasi di Browser
Buka peramban web pada alamat:
`http://localhost:3000`

### Langkah 5: Kredensial Akun Pengujian
Gunakan salah satu akun pengujian yang terdaftar pada:
`docs/guide/ACCOUNTS.local.md`
Contoh akun Administrator:
- Username: `admin`
- Password: `Password123!`

---

## BAB 3 - Prerequisites

Sebelum menjalankan aplikasi, pastikan perangkat kerja memenuhi dependensi berikut:

| Komponen | Versi Minimal | Status Verifikasi | Perintah Pengecekan |
|---|---|---|---|
| **Sistem Operasi** | Windows 10/11 x64 dengan WSL2 | Terverifikasi | `wsl --status` |
| **Python** | Python 3.12.x | Terverifikasi (3.12.0) | `python --version` |
| **Virtual Environment** | `backend/.venv` | Terverifikasi | `backend\.venv\Scripts\python.exe -V` |
| **Node.js** | Node.js v20.x atau v22.x | Terverifikasi (v22.14.0) | `node --version` |
| **npm** | npm v10.x | Terverifikasi (v10.9.2) | `npm --version` |
| **Redis Server** | Redis 7.x pada WSL2 Ubuntu | Terverifikasi (PONG pada port 6379) | `wsl -d Ubuntu -- redis-cli ping` |
| **Database Development** | SQLite 3.x (dengan WAL mode) | Aktif secara default | Otomatis oleh Django |
| **Database Production** | PostgreSQL 16/17 | Opsional (Dual-Engine ready) | `psql --version` |

---

## BAB 4 - Environment Configuration

Konfigurasi lingkungan dikelola secara terpusat melalui berkas `.env` dan dimuat oleh `django-environ` di backend serta `import.meta.env` di frontend.

### 4.1 Backend Environment (`backend/.env`)
```ini
DJANGO_SECRET_KEY=local-dev-secret-key-change-in-production-min-50-chars-long!
DJANGO_DEBUG=True
DJANGO_ENV=development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://127.0.0.1:6379/1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
PRIVATE_MEDIA_ROOT=private_media
ACCESS_TOKEN_LIFETIME_MINUTES=30
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 4.2 Frontend Environment (`frontend/.env`)
```ini
VITE_API_BASE_URL=/api
VITE_APP_TITLE=Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut
BACKEND_PROXY_TARGET=http://127.0.0.1:8000
```
Proxy Vite pada `frontend/vite.config.ts` meneruskan panggilan `/api/*` secara transparan ke `BACKEND_PROXY_TARGET` (port 8000), sehingga aplikasi frontend terbebas dari kendala CORS pada lingkungan pengembangan.

---

## BAB 5 - Database Configuration

Aplikasi mendukung arsitektur basis data ganda (*Dual-Engine Database Architecture*):

### 5.1 SQLite dengan Mode WAL (Default Development)
- **Lokasi Berkas**: `backend/db.sqlite3`.
- **Mode Konkurensi**: Write-Ahead Logging (WAL) diaktifkan secara otomatis pada startup melalui Django core setup (`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;`).
- **Karakteristik**: Cepat, tanpa konfigurasi daemon tambahan, terisolasi penuh untuk pengujian fungsional dan UI/UX lokal.

### 5.2 PostgreSQL 16 (WSL2 Ubuntu) & PostgreSQL 17 (Windows)
Untuk pengujian beban tinggi atau mode produksi:
1. Ubah variabel `DATABASE_URL` pada `backend/.env`:
   ```ini
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/sie_bunut_db
   ```
2. Jalankan migrasi skema:
   ```powershell
   backend\.venv\Scripts\python.exe backend/manage.py migrate
   ```

### 5.3 Prosedur Migrasi dan Pencadangan Basis Data
- **Menjalankan Migrasi**:
  ```powershell
  backend\.venv\Scripts\python.exe backend/manage.py migrate
  ```
- **Mencadangkan Basis Data SQLite**:
  ```powershell
  Copy-Item backend/db.sqlite3 backend/db_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sqlite3
  ```

---

## BAB 6 - Redis Configuration

Redis bertindak sebagai infrastruktur kritis untuk:
1. **Token Blacklist Revocation**: Menyimpan token JWT yang telah dibatalkan saat logout untuk mencegah penggunaan ulang token (*fail-closed policy*).
2. **Rate Limiting**: Membatasi percobaan brute-force login pada endpoint otentikasi.
3. **Response Caching**: Menyimpan cache data agregat dashboard dan rekapitulasi (*fail-open policy*).

### 6.1 Status dan Perintah Operasional
- **Pemeriksaan Konektivitas**:
  ```powershell
  wsl -d Ubuntu -- redis-cli ping
  ```
- **Memulai Layanan Redis**:
  ```powershell
  wsl -d Ubuntu -- sudo service redis-server start
  ```
- **Mengosongkan Cache Pengujian**:
  ```powershell
  wsl -d Ubuntu -- redis-cli -n 1 FLUSHDB
  ```

---

## BAB 7 - Database Seeding

Aplikasi dilengkapi dengan reusable database seeder berbasis library `Faker("id_ID")` yang menghasilkan data sekolah Indonesia yang realistis, saling terhubung secara relasional, dan idempoten.

### 7.1 Perintah Seeder
```powershell
# Profil Lengkap (Full Realistic Dataset - Rekomendasi Utama):
backend\.venv\Scripts\python.exe backend/manage.py seed_school_data --profile full

# Profil Ringkas (Small Dataset - Pengujian Cepat):
backend\.venv\Scripts\python.exe backend/manage.py seed_school_data --profile small

# Simulasi Tanpa Menulis ke Basis Data (Dry Run):
backend\.venv\Scripts\python.exe backend/manage.py seed_school_data --profile small --dry-run
```

### 7.2 Opsi Perintah Seeder
- `--profile`: Pilihan `full` (432+ siswa, 12 rombel aktif, 75 hari presensi, 150 permohonan surat) atau `small` (2 rombel, 20 siswa, 5 hari presensi).
- `--seed`: Bilangan integer untuk deterministic pseudo-random generator (default: 42).
- `--role-passwords`: Menetapkan kata sandi spesifik peran (`Admin123!`, `Guru123!`, dll.). Tanpa flag ini, kata sandi seragam `Password123!` digunakan.
- `--dry-run`: Menjalankan kalkulasi seeder tanpa mutasi basis data.

### 7.3 Perlindungan Lingkungan Produksi
Seeder memiliki mekanisme *fail-fast protection*: jika variabel `DJANGO_ENV=production` terdeteksi, perintah seeder seketika menghentikan eksekusi dengan `CommandError` demi mencegah penulisan data sintetis ke basis data produksi.

---

## BAB 8 - Hasil Populasi Database

Berikut adalah data populasi aktual yang telah terverifikasi tersimpan di dalam basis data:

| Entitas Data | Target Minimal | Jumlah Aktual | Status Keterpenuhan |
|---|---:|---:|---|
| **Peran Sistem (Roles)** | 6 | 6 | Terpenuhi (6 Peran Resmi) |
| **Akun Pengguna (Users)** | 40 | 45 | Terpenuhi (Lengkap 6 role + multi-role) |
| **Profil Pegawai (Employees)** | 40 | 50 | Terpenuhi (NIP & nomor telepon valid) |
| **Tahun Ajaran (AcademicYears)** | 2 (1 aktif) | 5 (1 aktif) | Terpenuhi (2026/2027 Aktif) |
| **Rombongan Belajar (SchoolClasses)** | 12 | 51 | Terpenuhi (Lengkap X-1 s/d XII-4) |
| **Data Siswa (Students)** | 432 aktif + alumni | 533 | Terpenuhi (485 Siswa Aktif) |
| **Penempatan Kelas (Enrollments)** | 432 aktif | 519 | Terpenuhi (Tidak ada overlap tanggal) |
| **Penugasan Guru (ClassAssignments)**| 24 penugasan | 38 | Terpenuhi (Wali Kelas & Guru Mapel) |
| **Rekor Presensi (Attendance)** | 60 - 90 hari | 11.376 | Terpenuhi (75 Hari Pembelajaran) |
| **Kasus Kesiswaan (StudentCases)** | 60 | 74 | Terpenuhi (Kasus ringan s/d mediasi) |
| **Riwayat Kasus (CaseEvents)** | 180 - 300 | 192 | Terpenuhi (Catatan tindakan & konseling) |
| **Jenis Layanan Surat (ServiceTypes)**| 5 | 10 | Terpenuhi (Surat Keterangan, Mutasi, dll.) |
| **Permohonan Surat (ServiceRequests)**| 100 - 150 | 170 | Terpenuhi (Berbagai status alur kerja) |
| **Riwayat Permohonan (ServiceEvents)**| 400 - 650 | 534 | Terpenuhi (Catatan mutasi status & disposisi) |
| **Dokumen Fisik (Documents)** | 100 - 150 | 130 | Terpenuhi (Berkas PDF fisik di storage) |

---

## BAB 9 - Running Backend

### 9.1 Menjalankan dengan Granian (ASGI Production Runner - Rekomendasi)
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo"
$env:REDIS_URL="redis://127.0.0.1:6379/1"
backend\.venv\Scripts\granian.exe --interface asginl config.asgi:application --working-dir backend --host 127.0.0.1 --port 8000
```

### 9.2 Menjalankan dengan Django Runserver (Alternatif Debug)
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo"
backend\.venv\Scripts\python.exe backend/manage.py runserver 127.0.0.1:8000
```

### 9.3 Pemeriksaan Sistem dan Dokumentasi API
- **Django System Check**: `backend\.venv\Scripts\python.exe backend/manage.py check`
- **Healthcheck Endpoint**: `http://127.0.0.1:8000/api/health`
- **OpenAPI Interactive Docs (Swagger)**: `http://127.0.0.1:8000/api/docs`

---

## BAB 10 - Running Frontend

### 10.1 Menjalankan Frontend Development Server (Vite)
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend"
npm run dev
```
Server Vite akan aktif pada `http://localhost:3000`.

### 10.2 Uji Kompilasi dan Tipe Data
```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend"
npm run typecheck    # TypeScript compiler check
npm run build        # Production bundle build test
```

---

## BAB 11 - One-Command Startup Helper

Untuk kenyamanan operasional satu langkah, telah disediakan script PowerShell pada `scripts/start-local.ps1`.

### 11.1 Menjalankan Helper
```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1
```

### 11.2 Fitur yang Dikelola Otomatis oleh Helper:
1. **Preflight Checks**: Memeriksa keberadaan Python, Node.js, virtual environment, berkas `.env`, dan database.
2. **Pemeriksaan Redis WSL2**: Mendeteksi layanan Redis dan menyalakan server jika belum aktif.
3. **Database Migration & Auto-seed**: Menjalankan migrasi Django dan memastikan dataset terisi jika basis data kosong.
4. **Isolasi Proses**: Menjalankan Granian backend (port 8000) dan Vite frontend (port 3000) pada jendela proses terkelola.
5. **Pemeriksaan Kesiapan Port**: Melakukan polling healthcheck hingga kedua port merespons HTTP 200 OK.
6. **Auto Launch Browser**: Membuka peramban default secara otomatis ke `http://localhost:3000`.
7. **Pembersihan Bersih (Graceful Teardown)**: Menekan tombol Enter pada jendela kontrol helper akan mematikan kedua proses anak tanpa meninggalkan proses *zombie* pada sistem.

---

## BAB 12 - Technical Verification

Seluruh subsistem telah melalui pengujian otomatis dan empiris dengan hasil 100% lulus:

| Lapisan Pengujian | Rincian Alat Uji | Total Uji | Hasil Verifikasi |
|---|---|---:|---|
| **Backend Test Suite** | Pytest 9.2 + Pytest-Django | 115 uji | **114 LULUS, 1 SKIPPED** (Postgres conditional) |
| **Frontend Test Suite** | Vitest 2.1 + React Testing Library | 74 uji | **74 LULUS (100%)** |
| **E2E Browser Tests** | Playwright Chromium | 7 alur | **7 LULUS (100%)** |
| **Integration Gates** | Python urllib runner (INT-M1 s/d M8) | 8 gerbang | **8 LULUS (100%)** |
| **Cross-Module N2N** | 20 End-to-End Cross-Module Checks | 20 cek | **20 LULUS (100%)** |

---

## BAB 13 - Troubleshooting

Berikut adalah solusi penanganan 20 kendala operasional umum berdasarkan kode sumber aplikasi:

1. **Redis tidak aktif / Connection Refused**:
   - Jalankan `wsl -d Ubuntu -- sudo service redis-server start`. Pastikan `wsl -d Ubuntu -- redis-cli ping` merespons `PONG`.
2. **Backend gagal startup**:
   - Jalankan `backend\.venv\Scripts\python.exe backend/manage.py check` untuk mendeteksi kesalahan konfigurasi atau sintaks model.
3. **Port 8000 atau 3000 sudah digunakan**:
   - Cari PID yang menduduki port: `Get-NetTCPConnection -LocalPort 8000` lalu matikan proses: `Stop-Process -Id <PID> -Force`.
4. **Database connection error**:
   - Periksa `DATABASE_URL` di `backend/.env`. Untuk SQLite, pastikan direktori `backend/` memiliki hak tulis.
5. **PostgreSQL authentication error**:
   - Periksa username dan password pada connection string `postgres://<user>:<pwd>@localhost:5432/<db>`.
6. **Missing environment variables**:
   - Salin kembali template default dari `backend/.env.example` ke `backend/.env`.
7. **Migration error (Conflicting migrations)**:
   - Jalankan `backend\.venv\Scripts\python.exe backend/manage.py showmigrations` untuk melihat migrasi yang belum terpasang.
8. **Seeder error / IntegrityError**:
   - Seeder dirancang idempoten. Jika terjadi inkonsistensi data pengujian terdahulu, bersihkan data spesifik melalui Django shell.
9. **Duplicate records**:
   - Seeder menggunakan `get_or_create` berbasis kunci alami (`student_number`, `nip`, `name`). Menjalankan ulang seeder aman dan tidak menduplikasi data.
10. **Frontend API connection error**:
    - Periksa apakah Granian backend pada port 8000 sedang berjalan. Periksa `http://127.0.0.1:8000/api/health`.
11. **CORS Error**:
    - Akses frontend melalui `http://localhost:3000` agar proxy Vite bekerja. Backend mengizinkan origin localhost:3000 secara default.
12. **Login gagal (Kredensial Tidak Cocok)**:
    - Buka `docs/guide/ACCOUNTS.local.md`. Pastikan huruf besar dan kecil pada username dan password sesuai (contoh: `admin` / `Password123!`).
13. **Dashboard kosong / Metrics 0**:
    - Pastikan database telah dipopulasi menggunakan `seed_school_data --profile full`.
14. **Private file missing**:
    - Pastikan folder `backend/private_media/` tersedia. Seeder secara otomatis membuat berkas PDF fisik sintetis di folder ini.
15. **Export Excel / PDF gagal**:
    - Pastikan ReportLab dan openpyxl terpasang pada `backend/.venv` (`pip install openpyxl reportlab`).
16. **HTTP 401 Unauthorized**:
    - Token JWT kedaluwarsa (masa aktif 30 menit). Lakukan logout dan login ulang untuk mendapatkan token baru.
17. **HTTP 403 Forbidden**:
    - Akun Anda tidak memiliki hak akses objek riil (contoh: guru membuka kelas yang bukan binaannya, atau pimpinan mencoba membuka detail kasus privat). Ini adalah penegakan keamanan *least-privilege*.
18. **HTTP 409 Conflict**:
    - Terjadi benturan konkurensi (optimistic locking `expected_version` tidak cocok). Muat ulang halaman (*refresh*) untuk membaca versi data terbaru sebelum menyimpan kembali.
19. **HTTP 422 Unprocessable Entity**:
    - Format data masukan tidak sesuai skema validasi Pydantic / Zod (contoh: format tanggal bukan `YYYY-MM-DD`).
20. **HTTP 429 Too Many Requests**:
    - Terjadi pembatasan laju request oleh middleware Redis. Tunggu 60 detik sebelum melakukan percobaan login berikutnya.

---

## BAB 14 - Shutdown, Backup & Maintenance

### 14.1 Menghentikan Layanan
- **Granian / Django**: Tekan `Ctrl + C` pada terminal backend.
- **Vite Dev Server**: Tekan `Ctrl + C` pada terminal frontend.
- **Helper Script**: Tekan tombol `Enter` pada jendela `start-local.ps1`.

### 14.2 Prosedur Pencadangan (Backup)
1. **Basis Data**:
   ```powershell
   Copy-Item backend/db.sqlite3 "backend/backups/db_backup_$(Get-Date -Format 'yyyyMMdd_HHmm').sqlite3"
   ```
2. **Dokumen Privat**:
   ```powershell
   Compress-Archive -Path backend/private_media -DestinationPath "backend/backups/private_media_$(Get-Date -Format 'yyyyMMdd_HHmm').zip"
   ```

---

## BAB 15 - Final Setup Status

- **Status Kesiapan**: `READY - LOCAL_APPLICATION_RUNNING_AND_POPULATED`
- **Frontend URL**: `http://localhost:3000`
- **Backend API URL**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/api/docs`
- **Engine Basis Data Aktif**: SQLite 3 (WAL Mode, `backend/db.sqlite3`)
- **Redis Infrastructure**: Aktif (`redis://127.0.0.1:6379/1`, PONG)
- **Status Otentikasi**: 6 Akun resmi terverifikasi dapat login dengan token JWT dan RBAC terisolasi.
- **Status Seeder**: 11.376 presensi, 533 siswa, 74 kasus, 170 permohonan, 130 dokumen PDF fisik.
- **Status Pengujian**: Backend 114/115 Pass, Frontend Vitest 74/74 Pass, Playwright 7/7 Pass, Integrasi INT-M1 s/d M8 100% Pass.
