# Comprehensive Role-Based Access Control (RBAC) Matrix

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | APPROVED BASELINE v1.1.0 (Governed by Deny-by-Default; Unvalidated Policies marked PENDING_APPROVAL) |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Integration Agent / Security Auditor |
| Acuan | PRD §8, BSD §4/§8, DBD §7, UID §2/§8, AFD §1-10 |

---

## 1. Prinsip Utama Otorisasi

1. **Deny-by-Default:** Setiap kombinasi tindakan, peran, dan objek yang tidak tercantum secara eksplisit dengan status `ALLOWED` pada matriks ini akan ditolak dengan status HTTP 403 Forbidden.
2. **Object-Level Scoping:** Hak akses peran tidak bersifat global, melainkan dibatasi oleh cakupan objek (*object scoping*). Contoh: Guru hanya berwenang pada kelas yang ditugaskan kepadanya; Wali Kelas hanya berwenang pada kelas binaannya; Guru BK hanya pada kasus yang ditangani.
3. **Pemisahan Kewenangan (Separation of Duties):** Administrator sistem berwenang mengelola akun dan konfigurasi, namun **dilarang keras** memiliki akses otomatis membaca detail konseling kesiswaan sensitif atau mengunduh dokumen privat siswa tanpa penugasan fungsional.
4. **Izin Efektif Multi-Role (Additive Union without Invalidation):**
   - Hak akses pengguna yang memiliki lebih dari satu peran (misal Guru yang juga Wali Kelas) dievaluasi sebagai gabungan izin sah (*disjunctive / additive evaluation*).
   - Memiliki peran dengan hak lebih rendah (Guru) **tidak membatalkan** hak lebih tinggi yang dimiliki dari peran lain (Wali Kelas).
   - **Pengecualian Batasan Global (Global Security Boundary):** Larangan keamanan yang bersifat mutlak tetap berlaku (contoh: Administrator sistem dilarang membaca catatan konseling privat BK, dan Guru dilarang mengakses dokumen administrasi TU).
5. **Penegakan Runtime untuk Status PENDING_APPROVAL:**
   - Seluruh item yang bertanda `PENDING_APPROVAL` adalah usulan kebijakan yang masih menunggu validasi SOP resmi sekolah.
   - Pada tingkat runtime backend dan antarmuka frontend, item `PENDING_APPROVAL` **wajib diperlakukan sebagai DENIED (Deny-by-Default)** sampai diterbitkan ketetapan tertulis resmi.

---

## 2. Definisi Tindakan (Actions)

| Tindakan | Definisi Semantik |
|---|---|
| `LIST` | Mengambil daftar entitas dengan paginasi, pencarian, dan filter cakupan |
| `READ` | Membaca rincian lengkap satu objek entitas spesifik berdasarkan ID |
| `CREATE` | Menambahkan baris entitas baru ke sistem |
| `UPDATE` | Memperbarui atribut data entitas yang sudah ada |
| `DEACTIVATE`| Menonaktifkan entitas (soft disable / deactivation) |
| `ASSIGN` | Menghubungkan relasi antar-entitas (guru ke kelas, siswa ke rombel) |
| `RECORD` | Mencatat transaksi operasional baru (misal input absensi harian) |
| `CORRECT` | Mengoreksi data transaksi yang telah tersimpan sebelumnya |
| `PROCESS` | Memajukan tahapan alur kerja (misal verifikasi surat di TU) |
| `APPROVE` | Memberikan persetujuan resmi pimpinan pada permohonan |
| `REJECT` | Menolak permohonan dengan alasan penolakan tertulis |
| `CANCEL` | Membatalkan berkas atau kasus yang sedang berjalan |
| `EXPORT` | Mengunduh hasil agregasi laporan dalam format Excel (.xlsx) atau PDF |
| `DOWNLOAD` | Mengunduh berkas fisik privat yang tersimpan di direktori privat terproteksi |
| `AUDIT` | Membaca log audit jejak aktivitas sistem |

---

## 3. Matriks Hak Akses Rinci Lintas Entitas dan Peran

### 3.1. Modul Akun dan Konfigurasi Sesi (`accounts`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Sesi Login | `CREATE` | Publik / Semua Staf | Global | Kredensial valid & percobaan < 5 | ALLOWED | `/api/auth/login` | POST | S01 | BE-01 |
| Sesi Refresh | `CREATE` | Pengguna Terautentikasi | Sesi sendiri | Refresh token valid & aktif | ALLOWED | `/api/auth/refresh` | POST | S01, S03 | BE-02 |
| Sesi Logout | `CREATE` | Pengguna Terautentikasi | Sesi sendiri | Token aktif di-blacklist | ALLOWED | `/api/auth/logout` | POST | S03 | BE-02 |
| Profil Pengguna | `READ` | Pengguna Terautentikasi | Akun sendiri | Sesi aktif | ALLOWED | `/api/auth/me` | GET | S02, S03 | INT-M2 |
| Pengguna & Peran | `LIST`, `READ` | Administrator | Global | Akun aktif | ALLOWED | `/api/accounts/users` | GET | S04 | BE-02 |
| Pengguna & Peran | `CREATE`, `UPDATE` | Administrator | Global | Username & email unik | ALLOWED | `/api/accounts/users` | POST, PATCH | S04 | BE-02 |
| Status Akun | `DEACTIVATE` | Administrator | Akun selain diri sendiri | Mencegah lockout akun sendiri | ALLOWED | `/api/accounts/users/{id}` | PATCH | S04 | BE-02 |
| Daftar Peran | `LIST` | Administrator | Global | Sesi aktif | ALLOWED | `/api/accounts/roles` | GET | S04 | BE-02 |
| Pengguna & Peran | Semua aksi | Guru, Wali, Kesiswaan, TU, Pimpinan | None | Bukan wewenang peran | DENIED | `/api/accounts/*` | ANY | - | Security-RBAC |

---

### 3.2. Modul Data Master & Penempatan (`master_data`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Tahun Ajaran | `LIST`, `READ` | Seluruh Staf Sekolah | Global | Sesi aktif | ALLOWED | `/api/master/academic-years` | GET | S02, S06, S08 | INT-M3 |
| Tahun Ajaran | `CREATE`, `UPDATE` | Administrator | Global | Tanggal mulai < selesai | ALLOWED | `/api/master/academic-years`, `/api/master/academic-years/{id}` | POST, PATCH | S06 | INT-M3 |
| Kelas Rombel | `LIST`, `READ` | Seluruh Staf Sekolah | Global | Sesi aktif | ALLOWED | `/api/master/classes` | GET | S05, S06, S08 | INT-M3 |
| Kelas Rombel | `CREATE`, `UPDATE` | Administrator | Global | Nama kelas unik per tahun ajaran | ALLOWED | `/api/master/classes`, `/api/master/classes/{id}` | POST, PATCH | S06 | INT-M3 |
| Pegawai & Guru | `LIST`, `READ` | Administrator, TU, Pimpinan | Global | Sesi aktif | ALLOWED | `/api/master/employees` | GET | S06 | INT-M3 |
| Pegawai & Guru | `CREATE`, `UPDATE` | Administrator | Global | NIP/Identitas unik | ALLOWED | `/api/master/employees`, `/api/master/employees/{id}` | POST, PATCH | S06 | INT-M3 |
| Siswa (Demografis) | `LIST`, `READ` | Administrator, TU | Global | Untuk administrasi sekolah & persuratan | ALLOWED | `/api/master/students` | GET | S05, S12, S13 | INT-M3 |
| Siswa (Demografis) | `READ` | Guru, Wali Kelas, Kesiswaan | Kelas tugas / Kasus terkait | Hanya siswa dalam cakupannya | ALLOWED | `/api/master/students/{id}` | GET | S05, S08, S11 | BE-03 |
| Siswa | `CREATE`, `UPDATE` | Administrator | Global | NIS unik | ALLOWED | `/api/master/students`, `/api/master/students/{id}` | POST, PATCH | S05 | INT-M3 |
| Siswa | `CREATE`, `UPDATE` | Tata Usaha | Global | Pendaftaran siswa baru oleh TU | PENDING_APPROVAL | `/api/master/students` | POST, PATCH | S05 | Validasi-SOP |
| Penempatan Siswa | `LIST`, `ASSIGN`, `UPDATE` | Administrator, TU | Global | Siswa belum aktif di kelas lain; UPDATE untuk set end_date | ALLOWED | `/api/master/enrollments`, `/api/master/enrollments/{id}` | GET, POST, PATCH | S07 | INT-M3 |
| Penugasan Guru | `LIST`, `ASSIGN`, `UPDATE` | Administrator | Global | Guru dan kelas aktif; UPDATE untuk set end_date | ALLOWED | `/api/master/assignments`, `/api/master/assignments/{id}` | GET, POST, PATCH | S07 | INT-M3 |
| Penugasan Guru Sendiri | `LIST` | Guru Mata Pelajaran, Wali Kelas | Penugasan sendiri (`employee_id`) | Sesi aktif | ALLOWED | `/api/master/assignments` | GET | S02, S08 | BE-03 |

---

### 3.3. Modul Kehadiran (`attendance`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Roster Absensi | `READ` | Guru Mata Pelajaran, Wali Kelas | Kelas penugasan aktif | Tanggal valid dalam semester | ALLOWED | `/api/attendance/roster` | GET | S08 | BE-03, E2E-A1 |
| Kehadiran Batch | `RECORD` | Guru Mata Pelajaran, Wali Kelas | Kelas penugasan aktif | Tanggal <= hari ini & siswa aktif | ALLOWED | `/api/attendance/bulk` | POST | S08 | BE-04, BE-05 |
| Kehadiran Batch | `RECORD` | Guru di luar penugasan | Kelas lain | Di luar penugasan | DENIED | `/api/attendance/bulk` | POST | S08 | BE-03, E2E-A3 |
| Kehadiran | `CORRECT` | Guru Pencatat | Kelas penugasan | Waktu koreksi <= 24 jam dengan catatan | ALLOWED | `/api/attendance/bulk` | POST | S08 | BE-05 |
| Kehadiran | `CORRECT` | Guru Pencatat | Kelas penugasan | Waktu koreksi > 24 jam | PENDING_APPROVAL | `/api/attendance/bulk` | POST | S08 | Validasi-SOP |
| Kehadiran | `CORRECT` | Wali Kelas | Kelas binaannya | Koreksi absensi <= 24 jam dengan catatan | ALLOWED | `/api/attendance/bulk` | POST | S08 | BE-05 |
| Kehadiran | `CORRECT` | Wali Kelas | Kelas binaannya | Koreksi absensi > 24 jam tanpa izin pimpinan | PENDING_APPROVAL | `/api/attendance/bulk` | POST | S08 | Validasi-SOP |
| Rekap Kehadiran | `LIST`, `READ` | Guru Mata Pelajaran | Kelas penugasannya | Sesi aktif | ALLOWED | `/api/attendance` | GET | S09 | E2E-A1 |
| Rekap Kehadiran | `LIST`, `READ` | Wali Kelas | Kelas binaannya | Sesi aktif | ALLOWED | `/api/attendance` | GET | S09 | E2E-A1 |
| Rekap Kehadiran | `LIST`, `READ` | Kesiswaan, Pimpinan | Seluruh kelas (Agregat) | Sesi aktif | ALLOWED | `/api/attendance` | GET | S02, S09 | E2E-R1 |
| Rekap Kehadiran | `EXPORT` | Guru, Wali, Kesiswaan, Pimpinan | Sesuai cakupan masing-masing | Format .xlsx | ALLOWED | `/api/reports/attendance.xlsx` | GET | S09, S16 | BE-10 |
| Kehadiran | Semua aksi | Tata Usaha | None | Bukan lingkup operasional TU | DENIED | `/api/attendance/*` | ANY | - | Security-RBAC |

---

### 3.4. Modul Kasus Kesiswaan & Bimbingan Konseling (`student_affairs`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Kasus Disiplin Umum | `LIST` | Kesiswaan | Global dalam modul | Sesi aktif | ALLOWED | `/api/student-affairs/cases` | GET | S10 | E2E-A2 |
| Kasus Disiplin Umum | `LIST` | Wali Kelas | Siswa kelas binaannya | Sesi aktif | ALLOWED | `/api/student-affairs/cases` | GET | S10 | E2E-A2 |
| Kasus Disiplin Umum | `READ` | Kesiswaan, Wali Kelas terkait | Siswa dalam cakupan | Sesi aktif | ALLOWED | `/api/student-affairs/cases/{id}` | GET | S11 | E2E-A2 |
| Kasus Disiplin Umum | `CREATE` | Kesiswaan, Wali Kelas | Siswa dalam cakupan | Siswa terdaftar aktif | ALLOWED | `/api/student-affairs/cases` | POST | S10 | E2E-A2 |
| Status Kasus | `PROCESS` | Kesiswaan, Wali Kelas | Kasus terkait | Transisi sah (`BARU -> DIPROSES`) | ALLOWED | `/api/student-affairs/cases/{id}/transitions` | POST | S11 | BE-06 |
| Status Kasus | `PROCESS` (Selesai) | Kesiswaan | Kasus terkait | Status awal DIPROSES & catatan diisi | ALLOWED | `/api/student-affairs/cases/{id}/transitions` | POST | S11 | BE-06 |
| Status Kasus | `CANCEL` | Kesiswaan | Kasus terkait | Alasan pembatalan diisi | ALLOWED | `/api/student-affairs/cases/{id}/transitions` | POST | S11 | State-Machine |
| Catatan Konseling BK | `READ`, `RECORD` | Guru BK / Konselor ditugaskan | Kasus konseling binaannya | Terikat kode etik kerahasiaan konselor | ALLOWED | `/api/student-affairs/cases/{id}` | GET, POST | S11 | Security-Privacy |
| Catatan Konseling BK | `READ` | Wali Kelas siswa terkait | Siswa kelas binaannya | Ringkasan rekomendasi non-privat | ALLOWED | `/api/student-affairs/cases/{id}` | GET | S11 | Security-Privacy |
| Catatan Detail Konseling | `READ` | Administrator, Tata Usaha, Guru Mapel | None | Bukan kewenangan penanganan konseling | DENIED | `/api/student-affairs/cases/{id}` | GET | - | Security-Privacy |
| Catatan Detail Konseling | `READ` | Pimpinan Sekolah | Global | Pimpinan hanya berhak melihat statistik agregat | DENIED | `/api/student-affairs/cases/{id}` | GET | - | Security-Privacy |

---

### 3.5. Modul Persuratan Tata Usaha & Dokumen Privat (`administration`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Jenis Layanan Surat | `LIST`, `READ` | Seluruh Staf Sekolah | Global | Sesi aktif | ALLOWED | `/api/administration/service-types` | GET | S12, S13 | Skenario-B |
| Jenis Layanan Surat | `CREATE`, `UPDATE` | Administrator | Global | Kode dan nama layanan unik | ALLOWED | `/api/administration/service-types`, `/api/administration/service-types/{id}` | POST, PATCH | S06 | Skenario-B |
| Jenis Layanan Surat | `CREATE`, `UPDATE` | Tata Usaha | Global | Penambahan jenis layanan oleh staf TU | PENDING_APPROVAL | `/api/administration/service-types` | POST, PATCH | S06 | Validasi-SOP |
| Permohonan Surat | `LIST` | Tata Usaha | Global antrean permohonan | Sesi aktif | ALLOWED | `/api/administration/requests` | GET | S12, S14 | E2E-B1 |
| Antrean Persetujuan | `LIST` | Pimpinan | Khusus filter `status=MENUNGGU_PERSETUJUAN` | Sesi aktif pimpinan | ALLOWED | `/api/administration/requests` | GET | S14 | E2E-B1 |
| Permohonan Surat | `READ` | Tata Usaha | Global | Sesi aktif | ALLOWED | `/api/administration/requests/{id}` | GET | S14 | E2E-B1 |
| Permohonan Surat | `READ` | Pimpinan | Permohonan butuh persetujuan & arsip disetujui | Sesi aktif pimpinan | ALLOWED | `/api/administration/requests/{id}` | GET | S14, S15 | E2E-B1 |
| Permohonan Surat | `CREATE` | Tata Usaha | Global | Data pemohon lengkap | ALLOWED | `/api/administration/requests` | POST | S13 | E2E-B1 |
| Berkas Lampiran | `CREATE` (Upload) | Tata Usaha | Permohonan terkait | Format .pdf/.jpg/.png & ukuran <= 5MB | ALLOWED | `/api/administration/requests/{id}/documents` | POST | S13 | BE-07 |
| Status Permohonan | `PROCESS` (Verifikasi) | Tata Usaha | Permohonan terkait | DIAJUKAN -> DIPROSES | ALLOWED | `/api/administration/requests/{id}/transitions` | POST | S14 | E2E-B1 |
| Status Permohonan | `PROCESS` (Ajukan) | Tata Usaha | Permohonan terkait | DIPROSES -> MENUNGGU_PERSETUJUAN | ALLOWED | `/api/administration/requests/{id}/transitions` | POST | S14 | E2E-B1 |
| Status Permohonan | `APPROVE` | Pimpinan | Permohonan menunggu persetujuan | Persetujuan resmi kepala sekolah | ALLOWED | `/api/administration/requests/{id}/transitions` | POST | S14 | E2E-B1 |
| Status Permohonan | `REJECT` | Pimpinan | Permohonan menunggu persetujuan | Alasan penolakan tertulis wajib | ALLOWED | `/api/administration/requests/{id}/transitions` | POST | S14 | E2E-B1 |
| Status Permohonan | `PROCESS` (Selesai) | Tata Usaha | Permohonan disetujui / tanpa persetujuan | Surat fisik diserahkan | ALLOWED | `/api/administration/requests/{id}/transitions` | POST | S14 | E2E-B1 |
| Arsip Dokumen | `LIST` | Tata Usaha, Pimpinan | Arsip dokumen yang telah selesai | Sesi aktif | ALLOWED | `/api/administration/documents` | GET | S15 | BE-08 |
| Dokumen Privat | `DOWNLOAD` | Tata Usaha, Pimpinan | Permohonan terkait | Akses terproteksi via token | ALLOWED | `/api/administration/documents/{id}/download` | GET | S14, S15 | BE-08 |
| Dokumen Privat | `DOWNLOAD` | Guru Mapel, Publik, Siswa | None | Tidak memiliki wewenang operasional TU | DENIED | `/api/administration/documents/{id}/download` | GET | - | BE-08, E2E-B2 |
| Laporan Layanan TU | `EXPORT` | Tata Usaha, Pimpinan | Global | Format PDF resmi | ALLOWED | `/api/reports/administration.pdf` | GET | S16 | BE-10 |

---

### 3.6. Modul Laporan dan Audit Sistem (`reports` & `core`)

| Resource | Action | Role Berwenang | Object Scope | Prasyarat | Status Izin | Endpoint Terkait | Method | Screen ID | Test ID |
|---|---|---|---|---|---|---|---|---|---|
| Dashboard Metrik | `READ` | Semua Peran | Terfilter otomatis sesuai cakupan peran | Sesi aktif | ALLOWED | `/api/reports/dashboard` | GET | S02 | BE-09, E2E-R1 |
| Audit Trail Sistem | `LIST`, `READ` | Administrator | Global | Sesi aktif | ALLOWED | `/api/audit-logs` | GET | S17 | BE-05 |
| Audit Trail Sistem | `LIST`, `READ` | Pimpinan | Khusus log persetujuan & disposisi pimpinan | Persetujuan kebijakan audit eksekutif | PENDING_APPROVAL | `/api/audit-logs` | GET | S17 | Validasi-SOP |
| Audit Trail Sistem | Semua aksi | Guru, Wali, Kesiswaan, TU | None | Bukan kewenangan peran | DENIED | `/api/audit-logs` | ANY | - | Security-Privacy |

---

## 4. Resolusi Multi-Peran (Multi-Role Resolution Algorithm)

Bagi staf sekolah yang mengemban lebih dari satu peran (contoh: Guru dengan NIP 19800101 yang sekaligus ditugaskan sebagai Wali Kelas X-A):

1. **Evaluasi Disjungtif (Additive Union):**
   $$\text{Effective Permissions} = \bigcup_{r \in \text{User.roles}} \text{Permissions}(r)$$
   Jika suatu aksi diizinkan oleh peran Guru ATAU peran Wali Kelas untuk objek sasaran, aksi tersebut **diterima** (*ALLOWED*).
2. **Non-Pembatalan Antar-Peran (No Cross-Role Invalidation):**
   Kepemilikan peran Guru yang tidak berwenang pada kasus kesiswaan kelas lain **tidak membatalkan** hak peran Wali Kelas untuk melihat kasus kesiswaan siswa di kelas binaan binaannya (X-A).
3. **Penegakan Batasan Keamanan Global (Global Security Boundaries):**
   Larangan keamanan mutlak tetap ditegakkan terlepas dari kombinasi peran. Contoh: Administrator sistem yang juga memiliki peran Guru dilarang menyalahgunakan akun admin untuk memintas akses ke catatan konseling privat bimbingan konseling tanpa penugasan konselor resmi.
4. **Pemisahan Konteks Tampilan vs Otorisasi Server:**
   Pilihan "Ganti Konteks Peran" pada antarmuka web (Screen S03) semata-mata menyederhanakan navigasi menu dan filter awal bagi pengguna agar tidak bingung. Di tingkat backend Django Ninja, seluruh kueri dan mutasi selalu divalidasi terhadap hak akses gabungan pengguna dan relasi objek riil di basis data.
