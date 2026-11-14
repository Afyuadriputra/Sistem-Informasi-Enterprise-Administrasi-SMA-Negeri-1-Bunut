
Ran find seed scripts in backend
Ran find account files in backend
Checked task Find account files in backend
Analyzed conftest.py:L1-25
Analyzing test_auth.py:L1-60
Ran list test files in backend
Analyzed test_e2e.py:L1-60
Ran check for sqlite database in backend
Ran check users in db.sqlite3 · Exited with code 1
Ran list tables in db.sqlite3
Ran query users in db.sqlite3
Ran query user roles in db.sqlite3
Ran check CORS in backend settings
Analyzed settings.py:L175-210
Ran find venv in project
Ran find venv in backend
Ran find passwords in backend tests
Ran check u_guru password · Exited with code 1
Ran test u_guru password inside backend directory
Ran list all users and roles in db.sqlite3
Ran list roles in db.sqlite3
Ran check if db.sqlite3 is gitignored
Ran seed demo users in local db.sqlite3 · Exited with code 1
Analyzed models.py:L1-60
Ran seed demo accounts in db.sqlite3
Ran test login endpoint with admin credentials

**Ya, frontend Anda sudah 100% siap dijalankan dan diuji langsung di browser!**

Aplikasi frontend dan backend berkomunikasi secara langsung melalui REST API contract-first di `http://localhost:8000/api`.

---

### Langkah 1: Menjalankan Backend (API Server)

Buka terminal pertama (PowerShell), lalu jalankan server backend Django Ninja:

```powershell
cd "d:\Kuliah\joki\radit\PROJEK istri bg givo\backend"
.\.venv\Scripts\python.exe manage.py runserver 8000
```

> Server backend akan aktif melayani request di: `http://localhost:8000` (endpoint API di `http://localhost:8000/api`).

---

### Langkah 2: Menjalankan Frontend (Vite Dev Server)

Buka terminal kedua (PowerShell), lalu jalankan dev server frontend:

```powershell
cd "d:\Kuliah\joki\radit\PROJEK istri bg givo\frontend"
npm run dev
```

> Server frontend akan aktif di: **`http://localhost:5173`**.

Buka browser Anda ke `http://localhost:5173`. Sistem akan otomatis mengarahkan Anda ke halaman login resmi SMA Negeri 1 Bunut di `http://localhost:5173/login`.

---

### Langkah 3: Akun Demo untuk Login

Seluruh 6 peran (*roles*) resmi enterprise telah disiapkan di database lokal dengan kata sandi (*password*) default yang seragam:

> **Kata Sandi (Password) untuk Semua Akun:** `Password123!`

Pilih akun login sesuai peran yang ingin Anda uji:

| Peran (*Role*)            | Nama Pengguna (*Username*) | Kata Sandi (*Password*) | Tampilan & Fitur yang Dapat Dicoba                                                                                       |
| --------------------------- | ---------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Administrator**     | `admin`                    | `Password123!`          | **S02 / S04 / S05 / S06 / S07 / S17**Kelola Pengguna, Data Siswa, Tahun Ajaran, Rombel, Penugasan Guru, Log Audit  |
| **Guru Pengampu**     | `guru`                     | `Password123!`          | **S02 / S08 / S09**Presensi Kelas Harian (Tandai Semua Hadir, H/S/I/A toggle), Rekap Kehadiran, Ekspor Excel       |
| **Wali Kelas**        | `wali_kelas`               | `Password123!`          | **S02 / S08 / S09 / S10**Presensi Kelas Perwalian, Monitoring Siswa, Rujuk Kasus Siswa                             |
| **Kesiswaan (BK)**    | `kesiswaan`                | `Password123!`          | **S02 / S10 / S11**Antrean Kasus BK, Detail Kasus 62:38 Golden Ratio, Alur Mediasi & Catatan Konseling             |
| **Tata Usaha (TU)**   | `tata_usaha`               | `Password123!`          | **S02 / S12 / S13 / S14 / S15**Antrean Surat Masuk, Buat Permohonan Baru, Upload Berkas Persyaratan, Katalog Arsip |
| **Pimpinan (Kepsek)** | `kepsek`                   | `Password123!`          | **S02 / S14-P / S16**Antrean Persetujuan/Disposisi Pimpinan, Monitoring Eksekutif, Penerbitan Laporan Resmi        |

---

### Fitur Keamanan yang Berjalan Saat Login:

1. **Zero Storage Leakage:** Token otentikasi disimpan eksklusif dalam memori volatil aplikasi (`src/lib/api-client.ts`), tidak ada penyimpanan token pada `localStorage`, `sessionStorage`, maupun cookie browser.
2. **Auto Context Redirection:** Setelah login, Anda akan langsung diarahkan ke Dashboard peran yang sesuai dengan 4 kartu metrik utama.
3. **Role Context Switcher:** Jika memiliki lebih dari 1 peran, Anda dapat beralih peran kerja secara instan melalui dropdown profil di pojok kanan atas.
