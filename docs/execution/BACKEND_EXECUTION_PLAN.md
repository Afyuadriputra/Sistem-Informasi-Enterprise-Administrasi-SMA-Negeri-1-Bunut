# Backend Execution Plan

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | APPROVED EXECUTION BASELINE |
| Terakhir Diperbarui | 12 November 2026 |
| Target Arsitektur | Django 5.x Modular Monolith, Django Ninja, Granian (ASGI), Redis, SQLite WAL / PostgreSQL |
| Acuan | TRD §1-11, BSD §1-11, DBD §1-10, contracts/openapi.v1.yaml, contracts/database.dbml |

---

## 1. Prinsip Eksekusi Backend

1. **Independensi Mutlak:** Seluruh modul backend dapat dibangun, dijalankan, dan diuji 100% menggunakan test suite terotomasi (`pytest`) tanpa membutuhkan antarmuka frontend.
2. **Kepatuhan Kontrak (Contract-Bound):** Seluruh input, output, kode HTTP, dan format envelope error wajib mematuhi persis `contracts/openapi.v1.yaml`.
3. **Pemisahan Lapisan (Layered Architecture):**
   - `api.py`: Penanganan HTTP, routing Ninja, autentikasi JWT, delegasi otorisasi.
   - `schemas.py`: Kontrak data request/response berbasis Pydantic.
   - `services.py`: Logika bisnis, transaksi atomik, mutasi database, event recording, audit trail, invalidasi cache.
   - `selectors.py`: Pembacaan data terotorisasi (*object scoping*), filter, paginasi, agregasi.
   - `models.py`: Definisi persistensi ORM, constraint integritas, snapshot histori.
4. **Keamanan Bawaan:** Validasi otorisasi per objek pada kueri (*IDOR prevention*), sanitasi log, dan rate limiting.

---

## 2. Rincian Milestone Pengerjaan Backend (BE-M1 s/d BE-M8)

### BE-M1: Project Foundation & Core Configuration
- **Tujuan:** Menyiapkan struktur repositori Django modular monolith, konfigurasi Granian ASGI, manajemen environment, envelope error terstandar, dan test runner.
- **Task ID:** `BE-TASK-01`
- **Dependency:** Inisialisasi M0 selesai.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (ErrorEnvelope).
- **Allowed Paths:** `backend/config/**`, `backend/apps/core/**`, `backend/manage.py`, `backend/pytest.ini`, `backend/requirements.txt`.
- **Forbidden Paths:** `backend/apps/{accounts,master_data,attendance,student_affairs,administration,reports}/**`, `frontend/**`.
- **Referensi Dokumen:** TRD §1/§2/§3/§9/§10.
- **Business Rules:** Seluruh respon error menggunakan envelope terstandar dengan `request_id` unik; format log terstruktur JSON.
- **Database Impact:** Tidak ada model bisnis pada M1; koneksi database SQLite WAL / PostgreSQL tervalidasi.
- **Implementation Steps:**
  1. Setup struktur direktori backend modular monolith.
  2. Konfigurasi `config/settings.py` dengan decouple environment (`DJANGO_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, dll.).
  3. Konfigurasi exception handler global Django Ninja untuk menangani `ValidationError`, `HttpError`, dan uncaught 500.
  4. Setup middleware request ID dan request logging terstruktur.
  5. Konfigurasi pytest runner dan fixture client dasar.
- **Testing:**
  - Unit Test: Serialisasi `ErrorEnvelope`, generator `request_id`.
  - Integration Test: Healthcheck endpoint `/api/health`, penanganan error 404/500 aman.
- **Definition of Done:** `python manage.py check` lulus; pytest lulus; error handler menghasilkan JSON envelope terstandar.

---

### BE-M2: Authentication, Custom User & RBAC
- **Tujuan:** Membangun Custom User model, integrasi Django Groups/Roles, autentikasi JWT, rotasi token, blacklist sesi saat logout, dan rate limiting brute-force.
- **Task ID:** `BE-TASK-02`
- **Dependency:** `BE-M1`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/auth/*`, `/accounts/*`).
- **Allowed Paths:** `backend/apps/accounts/**`, `backend/apps/core/security.py`, `backend/tests/accounts/**`.
- **Forbidden Paths:** `backend/apps/{master_data,attendance,student_affairs,administration,reports}/**`, `frontend/**`.
- **Referensi Dokumen:** TRD §2/§5, BSD §2/§4, docs/RBAC_MATRIX.md.
- **Business Rules:**
  - Hash kata sandi menggunakan Argon2.
  - Access token berumur 15 menit; refresh token berumur 7 hari dengan rotasi otomatis.
  - Percobaan login salah dibatasi maksimal 5 kali per IP/username dalam 15 menit via counter Redis (HTTP 429).
  - Logout memasukkan refresh token ke blacklist.
- **Database Impact:** Tabel `users`, `roles`, `user_roles`, `activity_logs`.
- **Testing:** Test `BE-01` (rate limiting 429), `BE-02` (akun nonaktif ditolak), test rotasi token dan logout blacklist.
- **Definition of Done:** Seluruh endpoint auth lulus uji keamanan; token kedaluwarsa atau dicabut ditolak secara konsisten.

---

### BE-M3: Master Data & Academic Placements
- **Tujuan:** Membangun entitas tahun ajaran, kelas rombel, profil pegawai/guru, data siswa, penempatan enrollment, dan penugasan guru.
- **Task ID:** `BE-TASK-03`
- **Dependency:** `BE-M2`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/master/*`), `contracts/database.dbml`.
- **Allowed Paths:** `backend/apps/master_data/**`, `backend/tests/master_data/**`.
- **Forbidden Paths:** `backend/apps/{attendance,student_affairs,administration,reports}/**`, `frontend/**`.
- **Referensi Dokumen:** DBD §2/§4/§6, BSD §2, PRD §9 (FR-02).
- **Business Rules:**
  - Hanya satu tahun ajaran aktif secara default.
  - Nama kelas unik per tahun ajaran (`SchoolClass.academic_year_id + name`).
  - Nomor induk siswa (`student_number`) wajib unik dan ternormalisasi.
  - Siswa hanya boleh memiliki satu penempatan kelas aktif (`Enrollment.end_date IS NULL`) pada waktu yang sama.
- **Database Impact:** Tabel `academic_years`, `school_classes`, `employees`, `students`, `enrollments`, `class_assignments`.
- **Testing:** Unit test validasi tanggal tahun ajaran; test constraint unik siswa/kelas; test pencegahan overlap penempatan siswa.
- **Definition of Done:** Migrasi bersih; CRUD master data tervalidasi; fixture seed data sintetis berhasil dimuat.

---

### BE-M4: Attendance Module & Bulk Atomic History
- **Tujuan:** Membangun kueri roster absensi per kelas/tanggal, penyimpanan kehadiran batch atomik, pencatatan snapshot riwayat via bulk history, dan rekapitulasi kehadiran.
- **Task ID:** `BE-TASK-04`
- **Dependency:** `BE-M3`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/attendance/*`).
- **Allowed Paths:** `backend/apps/attendance/**`, `backend/tests/attendance/**`.
- **Forbidden Paths:** `backend/apps/{student_affairs,administration,reports}/**`, `frontend/**`.
- **Referensi Dokumen:** DBD §2/§4/§5, BSD §2/§3.1, TRD §6, AFD §3 (Skenario A).
- **Business Rules:**
  - Guru hanya dapat mencatat dan melihat kelas tugasnya (`ClassAssignment`).
  - Seluruh siswa dalam batch wajib terdaftar aktif pada tanggal absensi terkait.
  - Transaksi atomik: satu siswa tidak valid membatalkan seluruh penyimpanan.
  - Wajib mencatat histori snapshot menggunakan `bulk_create_with_history`.
  - Invalidasi cache rekapitulasi kelas terkait via `transaction.on_commit()`.
- **Database Impact:** Tabel `attendances`, `historical_attendances`.
- **Testing:** Test `BE-03` (guru kelas lain ditolak 403), `BE-04` (siswa tidak terdaftar membatalkan batch 422), `BE-05` (batch sah tersimpan dan riwayat audit tercipta).
- **Definition of Done:** Kueri roster cepat; endpoint bulk atomik teruji; snapshot history tercatat lengkap.

---

### BE-M5: Student Affairs & Case Timeline
- **Tujuan:** Membangun modul penanganan kasus kesiswaan, state machine transisi status kasus, pencatatan tindakan kronologis (`CaseEvent`), dan kontrol konkurensi optimistik (`version`).
- **Task ID:** `BE-TASK-05`
- **Dependency:** `BE-M4`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/student-affairs/*`).
- **Allowed Paths:** `backend/apps/student_affairs/**`, `backend/tests/student_affairs/**`.
- **Forbidden Paths:** `backend/apps/{administration,reports}/**`, `frontend/**`.
- **Referensi Dokumen:** DBD §2/§8, BSD §2/§3.2, AFD §3/§6, PRD §9 (FR-04).
- **Business Rules:**
  - Transisi status wajib mematuhi state machine yang sah (`BARU -> DIPROSES -> SELESAI / DIBATALKAN`).
  - Setiap transisi dan tindakan wajib menyertakan `expected_version`; benturan versi menghasilkan HTTP 409 Conflict.
  - Pencatatan perubahan status dan penambahan entri `CaseEvent` dijalankan dalam satu transaksi atomik.
  - Akses detail kasus dibatasi untuk staf Kesiswaan dan Wali Kelas siswa bersangkutan.
- **Database Impact:** Tabel `student_cases`, `case_events`.
- **Testing:** Test `BE-06` (konflik konkurensi 409), test penolakan transisi status ilegal, test pencatatan tindakan tanpa ubah status (`CATAT_TINDAKAN`).
- **Definition of Done:** Alur kesiswaan lulus uji state machine; isolasi privasi data kasus terverifikasi.

---

### BE-M6: Administration, Approval Workflow & Private Documents
- **Tujuan:** Membangun permohonan persuratan tata usaha, alur persetujuan pimpinan, validasi unggahan berkas privat, dan streaming unduhan terproteksi.
- **Task ID:** `BE-TASK-06`
- **Dependency:** `BE-M3`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/administration/*`).
- **Allowed Paths:** `backend/apps/administration/**`, `backend/tests/administration/**`.
- **Forbidden Paths:** `backend/apps/reports/**`, `frontend/**`.
- **Referensi Dokumen:** DBD §2/§6, BSD §2/§3.3, TRD §5, AFD §4/§6 (Skenario B), PRD §9 (FR-05, FR-06).
- **Business Rules:**
  - Status permohonan mengikuti alur: `DIAJUKAN -> DIPROSES -> MENUNGGU_PERSETUJUAN -> DISETUJUI / DITOLAK -> SELESAI`.
  - Berkas lampiran disimpan di `PRIVATE_MEDIA_ROOT` dengan nama acak UUID tanpa nama asli di filesystem.
  - Verifikasi ekstensi (.pdf, .jpg, .png), ukuran (maks 5MB), dan magic bytes.
  - Unduhan berkas privat via `GET /api/administration/documents/{id}/download` memeriksa wewenang akses per objek.
- **Database Impact:** Tabel `service_types`, `service_requests`, `service_events`, `documents`.
- **Testing:** Test `BE-07` (unggah berkas ilegal ditolak 422), `BE-08` (unduhan tanpa izin ditolak 403), test alur persetujuan dan penolakan tersimpan dengan alasan tertulis.
- **Definition of Done:** Dokumen tersimpan aman dan terisolasi dari akses publik; tahapan persetujuan pimpinan tervalidasi.

---

### BE-M7: Dashboard Aggregations, Reporting & Redis Cache
- **Tujuan:** Membangun kueri ringkasan dashboard teragregasi per peran, generator ekspor data ke Excel (`openpyxl`) dan PDF (`ReportLab`), serta caching Redis dengan invalidasi pasca commit.
- **Task ID:** `BE-TASK-07`
- **Dependency:** `BE-M4`, `BE-M5`, `BE-M6`.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (`/reports/*`, `/audit-logs`).
- **Allowed Paths:** `backend/apps/reports/**`, `backend/tests/reports/**`.
- **Forbidden Paths:** `frontend/**`.
- **Referensi Dokumen:** BSD §2/§5, TRD §2/§6, PRD §9 (FR-07, FR-08, FR-09).
- **Business Rules:**
  - Dashboard menghitung metrik agregat sesuai cakupan peran (Pimpinan melihat ringkasan sekolah, Guru melihat status kelas tugas).
  - Caching kueri agregasi di Redis berdurasi 5-15 menit dengan key spesifik cakupan peran.
  - Ekspor Excel dan PDF menerapkan filter dan batasan otorisasi yang persis sama dengan kueri data antarmuka.
  - Setiap aktivitas ekspor dicatat pada tabel `activity_logs`.
- **Database Impact:** Pembacaan lintas tabel dengan indeks teroptimasi.
- **Testing:** Test `BE-09` (dashboard konsisten pasca mutasi dan cache invalidasi), test `BE-10` (ekspor menerapkan batasan cakupan data).
- **Definition of Done:** Ekspor berkas Excel dan PDF terbuat sempurna; kueri agregasi berjalan efisien (<200 ms).

---

### BE-M8: Backend Hardening, Security Audit & Performance Review
- **Tujuan:** Pengujian beban lokal, audit n+1 kueri, verifikasi proteksi IDOR lintas seluruh endpoint, sanitasi log audit, dan finalisasi dokumentasi instalasi backend.
- **Task ID:** `BE-TASK-08`
- **Dependency:** `BE-M7`.
- **Prasyarat Kontrak:** Seluruh kontrak OpenAPI v1.
- **Allowed Paths:** `backend/**`.
- **Forbidden Paths:** `frontend/**`.
- **Referensi Dokumen:** TRD §10/§11, BSD §10/§11, security-audit skill, ponytail-review skill.
- **Business Rules:**
  - Tidak ada kueri N+1 pada endpoint list terpaginasi (wajib menggunakan `select_related` / `prefetch_related`).
  - Tidak ada token, kata sandi, atau NIK siswa yang bocor di log sistem.
  - Kueri lambat (>500 ms) tercatat sebagai warning.
- **Testing:** Audit keamanan komprehensif seluruh endpoint IDOR; stress-test kueri absensi massal; verifikasi fallback saat Redis nonaktif.
- **Definition of Done:** Seluruh test suite (BE-01 s/d BE-10) lulus 100%; ruff check bersih; backend siap diintegrasikan.
