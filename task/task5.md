
# LOCAL-M1 — APPLICATION RUNNING, REALISTIC DATABASE SEEDING & OPERATIONAL READINESS

## PROJECT: SISTEM INFORMASI ENTERPRISE ADMINISTRASI SMA NEGERI 1 BUNUT

## MODE: AUTONOMOUS IMPLEMENTATION, DATABASE POPULATION & LOCAL VERIFICATION

---

# 1. ROLE & PRIMARY OBJECTIVE

Bertindak sebagai:

- Senior Full-Stack Engineer.
- Database Engineer.
- QA Engineer.
- Application Setup Engineer.
- Technical Documentation Writer.

Proyek Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut telah menyelesaikan pengembangan backend, frontend, desain dan integrasi hingga INT-M8.1.

Status saat ini:

`RELEASE_CANDIDATE — READY_FOR_CONTROLLED_LOCAL_DEMONSTRATION`

Tugas Anda adalah menyiapkan aplikasi agar dapat langsung dijalankan dan digunakan untuk pengujian seluruh fitur oleh enam role pengguna.

Pekerjaan utama:

1. Memeriksa environment aktual.
2. Menyiapkan prosedur menjalankan backend.
3. Menyiapkan prosedur menjalankan frontend.
4. Menghubungkan frontend dengan backend.
5. Memastikan Redis dan database berfungsi.
6. Membuat reusable database seeder menggunakan Faker.
7. Mengisi seluruh entitas database dengan data realistis dan saling terhubung.
8. Membuat akun seluruh role dengan password sederhana khusus pengujian lokal.
9. Menjalankan aplikasi.
10. Menguji seluruh role melalui browser nyata.
11. Membuat dokumentasi teknis dan panduan penggunaan.
12. Memperbaiki bug yang ditemukan selama proses pengujian.

Jangan membangun ulang aplikasi.

Jangan mengganti framework.

Jangan melakukan redesign besar.

Jangan mengubah business rules atau RBAC yang telah disetujui.

Fokus pada operational readiness, database population dan functional verification.

---

# 2. PROJECT WORKSPACE

Project root:

`D:\Kuliah\joki\radit\PROJEK istri bg givo`

Project directories:

- backend/
- frontend/
- integration/
- contracts/
- coordination/
- design/
- docs/

AI Agent Skills:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Documentation output:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\docs\guide`

## Documentation limitation

Buat hanya tiga file berikut pada docs/guide:

1. TECHNICAL_GUIDE.md.
2. USER_GUIDE.md.
3. ACCOUNTS.local.md.

Dua file pertama merupakan dokumen master.

ACCOUNTS.local.md merupakan file kredensial lokal yang wajib diabaikan Git.

Jangan membuat README.md atau dokumen panduan tambahan yang terpisah.

Gabungkan seluruh panduan teknis ke TECHNICAL_GUIDE.md.

Gabungkan seluruh panduan pengguna dan pengujian manual ke USER_GUIDE.md.

Jangan membuat folder screenshot baru dalam docs/guide. Gunakan existing frontend/evidence apabila screenshot diperlukan.

Gunakan actual project structure.

Patuhi AGENTS.md dan file ownership.

---

# 3. MANDATORY CONTEXT REVIEW

Baca langsung:

## Agent instructions

- Root AGENTS.md.
- backend/AGENTS.md.
- frontend/AGENTS.md.
- Agent instructions lain yang relevan.

## Primary project documentation

- docs/PRD.md.
- docs/TRD.md.
- docs/DBD.md.
- docs/BSD.md.
- docs/AFD.md.
- docs/IPD.md.
- docs/UID.md.
- docs/RBAC_MATRIX.md.
- docs/DECISION_LOG.md.

## Contracts

- contracts/openapi.v1.yaml.
- contracts/database.dbml.
- contracts/README.md.

## Coordination

- PROJECT_STATUS.md.
- BACKEND_STATUS.md.
- FRONTEND_STATUS.md.
- INTEGRATION_STATUS.md.
- CONTRACT_CHANGE_REQUESTS.md.

## Implementation reports

- Backend implementation report dan changelog.
- Frontend implementation report dan changelog.
- Integration implementation report dan changelog.

Periksa source code aktual:

- Django models.
- Django migrations.
- Django management commands.
- Environment loader.
- Django settings.
- Authentication services.
- RBAC.
- Domain services.
- Selectors.
- Historical models.
- Audit logging.
- Frontend package.json.
- Frontend API client.
- Vite configuration.
- Existing seed scripts.
- Existing test fixtures.
- Private file storage.

Jangan hanya mengandalkan laporan lama.

---

# 4. AI AGENT SKILLS & CODE INTELLIGENCE

Gunakan skills aktual dari:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Prioritaskan:

- tdd
- antislop-code
- improve-codebase-architecture
- python-performance-optimization
- security-audit
- ponytail
- ponytail-review
- antislop-ui
- antislop-copywriting

Baca SKILL.md sebelum menggunakan skill.

## CodeGraph

Gunakan CodeGraph MCP atau CLI untuk:

- Model discovery.
- Foreign key relationship mapping.
- Service dependency analysis.
- Domain workflow mapping.
- Seed dependency ordering.
- Audit hook mapping.
- Cache invalidation mapping.
- Blast radius analysis.

## Trail-Code

Baca learning yang relevan.

Catat root cause dan pembelajaran penting apabila ditemukan bug baru.

Jangan menyimpan password, token, credentials atau informasi sensitif pada Trail-Code.

Jangan menginstal ulang tools yang sudah tersedia.

Jangan menambah abstraction yang tidak diperlukan.

---

# 5. EXISTING ENVIRONMENT AUDIT

Environment configuration telah diimplementasikan pada BE-M9.2 dan FE-M10.2.

Periksa file aktual:

## Backend

- backend/.env.
- backend/.env.example.
- backend/.env.integration.
- backend/.env.integration.example.
- backend/config/env.py.
- backend/config/settings.py.

## Frontend

- frontend/.env.
- frontend/.env.example.
- frontend/.env.production.example.
- frontend/vite.config.ts.
- frontend/src/lib/api-client.ts.

## Integration

- integration/config.py.

Verifikasi:

- Python virtual environment.
- Python version.
- Django version.
- Django Ninja version.
- Granian version.
- Installed Python dependencies.
- Node.js.
- npm.
- Frontend dependencies.
- SQLite connectivity.
- PostgreSQL connectivity jika tersedia.
- Redis connectivity.
- Database migration status.
- Available ports.
- Backend API URL.
- Frontend API URL.
- Effective environment settings.

Jangan menginstal ulang dependency apabila sudah tersedia dan berfungsi.

Jangan menimpa .env aktual tanpa memeriksa isinya.

Jangan mencetak credentials sensitif.

Pastikan file environment benar-benar dibaca oleh aplikasi.

---

# 6. DEFAULT LOCAL ENVIRONMENT

Gunakan SQLite WAL sebagai default database untuk pengujian lokal.

Gunakan Redis WSL2 yang sudah tersedia.

Target runtime:

| Component             | Configuration         |
| --------------------- | --------------------- |
| Django environment    | development           |
| Database              | SQLite WAL            |
| Cache                 | Real Redis            |
| Backend host          | 127.0.0.1             |
| Backend port          | 8000                  |
| Frontend host         | localhost             |
| Frontend port         | 3000                  |
| Frontend API base URL | /api                  |
| Backend proxy target  | http://127.0.0.1:8000 |
| Redis port            | 6379                  |

Sesuaikan dengan environment aktual.

Jangan hardcode connection URL ke business logic.

Gunakan existing environment loader.

Periksa:

- journal_mode.
- foreign_keys.
- busy_timeout.

Gunakan actual SQLite PRAGMA.

Pastikan aplikasi menggunakan database yang akan diisi.

Prioritaskan dedicated SQLite database untuk dataset pengujian apabila database development yang ada berisi data yang harus dipertahankan.

Database pengujian fitur ini harus terpisah dari database sementara yang dibuat pytest.

Jangan menjalankan seeder pada database production.

Jangan menggunakan data siswa sekolah yang sebenarnya.

---

# 7. POSTGRESQL ENVIRONMENT ALTERNATIVE

Sediakan panduan menjalankan aplikasi menggunakan PostgreSQL.

## PostgreSQL 16 WSL2

Reported configuration:

- Host: 127.0.0.1.
- Port: 15432.
- Database sesuai .env.integration.
- Redis WSL2.

## PostgreSQL 17 Windows

Reported configuration:

- Host: 127.0.0.1.
- Port: 5432.
- Database dan role sesuai konfigurasi aktual.

Periksa actual connection.

PostgreSQL 17 belum boleh diklaim terverifikasi apabila belum berhasil diuji.

Gunakan:

- DATABASE_URL.
- ENV_FILE.
- DJANGO_ENV.

Sesuai implementasi environment loader aktual.

Jangan mengubah database engine melalui source code.

Jangan menggunakan PostgreSQL administrator atau SUPERUSER sebagai application runtime role.

Jangan menampilkan password database pada dokumentasi.

Jelaskan bahwa pergantian DATABASE_URL tidak otomatis memindahkan data.

Jangan menghapus SQLite development database.

Seeder harus kompatibel dengan SQLite dan PostgreSQL sesuai dukungan model aktual.

---

# 8. REDIS STARTUP & CONNECTIVITY

Periksa distribusi WSL2 aktual.

Verifikasi Redis service.

Gunakan perintah sesuai environment, misalnya:

```powershell
wsl --list --verbose
```

Periksa Redis melalui distribusi yang benar.

Verifikasi:

- redis-cli ping.
- Service status.
- Redis port.
- Connectivity dari backend Windows.
- Effective Django cache backend.
- Cache namespace.
- JWT blacklist.
- Rate limiting.
- Shared cache.

Jika Redis tidak aktif, jalankan melalui mekanisme service lokal yang diizinkan.

Jangan menginstal ulang Redis yang sudah tersedia.

Jangan membuka Redis ke jaringan publik.

Jangan menggunakan FLUSHALL atau FLUSHDB pada shared Redis instance.

Jangan mengganti Redis dengan LocMemCache hanya agar login berhasil.

Jangan melemahkan fail-closed security.

---

# 9. REALISTIC DATABASE SEEDING — PRIMARY REQUIREMENT

Isi seluruh database domain dengan data realistis menggunakan Faker.

Gunakan:

`Faker("id_ID")`

Apabila Faker belum tersedia, tambahkan sebagai development/seeding dependency sesuai dependency management proyek.

Faker hanya digunakan untuk menghasilkan data yang akan disimpan ke database.

Seluruh data harus diproses melalui backend nyata.

Gunakan Django ORM dan domain services yang sesuai.

DILARANG:

- Mock API.
- Static JSON sebagai pengganti database.
- Hardcoded dashboard metrics.
- Hardcoded student list.
- Fake success response.
- Faker runtime pada setiap request.
- Data frontend yang tidak berasal dari API aktual.

Data yang dibuat harus:

- Tersimpan permanen pada database lokal yang dipilih.
- Dapat dicari.
- Dapat difilter.
- Dapat diperbarui.
- Dapat diproses sesuai workflow.
- Dapat dihitung melalui dashboard.
- Dapat diekspor.
- Memiliki foreign key valid.
- Memiliki status yang konsisten.
- Memiliki history yang sesuai.
- Memiliki audit trail sesuai mekanisme existing.

---

# 10. OPERATIONAL UI DATA POLICY

Aplikasi harus terlihat seperti sistem administrasi sekolah yang digunakan sehari-hari.

Gunakan nama manusia Indonesia yang natural.

Gunakan nama kelas, data pegawai, permohonan surat, presensi dan kasus kesiswaan yang realistis.

Jangan menambahkan label berikut pada UI operasional hanya karena data dihasilkan menggunakan Faker:

- Demo.
- Dummy.
- Mockup.
- Simulasi.
- Mock data.
- Akun demo.
- Siswa dummy.
- Guru dummy.
- Dashboard demo.

Contoh yang dilarang:

- Siswa Dummy 001.
- Guru Demo.
- Kelas Simulasi.
- Permohonan Mock.
- Catatan Testing.

Tampilkan nama dan informasi sebagaimana aplikasi normal.

Namun:

- Data tetap merupakan data sintetis untuk pengujian lokal.
- Dokumentasi teknis wajib menjelaskan asal data tersebut.
- Jangan mengklaim data sebagai catatan resmi SMA Negeri 1 Bunut.
- Jangan mencampur data Faker dengan data sekolah nyata.
- Jangan menggunakan dataset tersebut sebagai hasil penelitian empiris.
- Jangan mengirim email, SMS, pesan atau notifikasi nyata kepada identitas sintetis.

Tidak perlu memberi watermark atau label demo pada seluruh halaman aplikasi.

---

# 11. DATABASE POPULATION TARGET

Periksa seluruh actual Django models, DBML, migrations dan approved contract.

Baseline proyek memiliki 18 domain tables.

Isi seluruh entitas bisnis yang tersedia sesuai relasi dan constraints.

| Entitas                   |                               Target awal |
| ------------------------- | ----------------------------------------: |
| Roles                     |                                         6 |
| Users                     |                                Sekitar 40 |
| User roles                |                     Sesuai tanggung jawab |
| Employees                 |                                        40 |
| Academic years            |                                         3 |
| School classes            |                    36 lintas tahun ajaran |
| Active students           |                                       432 |
| Alumni dan siswa nonaktif |                   Tambahan sesuai histori |
| Enrollments               |                Seluruh siswa yang relevan |
| Class assignments         |          Seluruh kelas aktif dan historis |
| Attendance                | Sekitar 60–90 hari pembelajaran historis |
| Historical attendance     |                  Sesuai riwayat perubahan |
| Student cases             |                                        60 |
| Case events               |                                  180–300 |
| Service types             |                                     8–12 |
| Service requests          |                                       150 |
| Service events            |                                  400–650 |
| Documents                 |                                  100–150 |
| Activity logs             |    Berdasarkan aktivitas seeding yang sah |

Angka tersebut merupakan target teknis, bukan populasi sekolah sebenarnya.

Sesuaikan dengan kapasitas perangkat dan actual database constraints.

Jangan membuat model atau field baru hanya untuk memenuhi contoh populasi.

Jangan memaksa tabel internal atau tabel khusus memiliki data apabila tidak diperlukan.

Laporkan actual counts setelah seeding.

---

# 12. ACADEMIC YEARS

Buat tiga tahun ajaran dengan histori yang konsisten.

Untuk November 2026, contoh:

- 2024/2025 — Nonaktif.
- 2025/2026 — Nonaktif.
- 2026/2027 — Aktif.

Gunakan tanggal sistem dan timezone Asia/Jakarta.

Pastikan:

- Tepat satu tahun ajaran aktif.
- Start date valid.
- End date valid.
- Tidak ada periode yang bertentangan dengan business rules.
- Enrollment dan assignment sesuai periode tahun ajaran.
- Data tahun sebelumnya tetap dapat digunakan untuk melihat histori.

Jika tanggal sistem berubah, sesuaikan tahun ajaran secara dinamis.

---

# 13. SCHOOL CLASSES

Buat 12 kelas untuk setiap tahun ajaran jika sesuai schema.

Kelas tahun aktif:

- X-1.
- X-2.
- X-3.
- X-4.
- XI-1.
- XI-2.
- XI-3.
- XI-4.
- XII-1.
- XII-2.
- XII-3.
- XII-4.

Setiap kelas aktif memiliki sekitar 36 siswa.

Total target siswa aktif: 432.

Gunakan grade level dan class names sesuai actual models.

Jangan mengarang jurusan atau peminatan yang tidak tersedia.

Pastikan setiap kelas historis memiliki hubungan enrollment dan assignment yang relevan.

---

# 14. STUDENT DATA

Gunakan Faker Indonesia untuk nama siswa.

Isi seluruh field yang didukung actual schema.

Contoh:

- Nomor induk siswa.
- Nama lengkap.
- Jenis kelamin.
- Status.
- Riwayat penempatan kelas.

Jangan menambahkan field NIK, alamat, tanggal lahir, NISN atau data orang tua apabila tidak tersedia.

Gunakan student identifiers sintetis yang unik.

Jangan mengambil identitas siswa nyata dari internet.

Jangan menggunakan nomor telepon atau alamat nyata yang berpotensi mengarah kepada individu tertentu.

Gunakan approved status enum aktual.

Baseline:

- AKTIF.
- MUTASI_KELUAR.
- LULUS.
- NONAKTIF.

Buat:

- Siswa aktif.
- Alumni.
- Siswa mutasi keluar.
- Siswa nonaktif.

Pastikan status siswa konsisten dengan enrollment.

Jangan menempatkan alumni pada kelas aktif apabila tidak diperbolehkan.

---

# 15. EMPLOYEES & SCHOOL STAFF

Buat sekitar 40 pegawai.

Distribusi awal yang disarankan:

| Kelompok             | Jumlah |
| -------------------- | -----: |
| Pimpinan             |      1 |
| Administrator sistem |      1 |
| Tata Usaha           |      4 |
| Kesiswaan/BK         |      3 |
| Guru                 |     31 |
| Total                |     40 |

Sebagian Guru juga memiliki penugasan sebagai Wali Kelas.

Pastikan seluruh 12 kelas aktif memiliki Wali Kelas sesuai ketentuan sistem.

Gunakan nama Indonesia yang natural.

Gunakan employee identifiers sintetis.

Jangan menggunakan identitas pegawai SMA Negeri 1 Bunut yang sebenarnya.

Isi field sesuai actual model.

Jangan membuat role ketujuh apabila tidak tersedia dalam approved RBAC.

---

# 16. USER ACCOUNTS & ROLE ASSIGNMENTS

Buat akun untuk enam role resmi:

1. Administrator.
2. Guru.
3. Wali Kelas.
4. Kesiswaan.
5. Tata Usaha.
6. Pimpinan.

Sediakan akun utama:

| Username       | Role                |
| -------------- | ------------------- |
| admin          | Administrator       |
| guru           | Guru                |
| wali_kelas     | Wali Kelas          |
| kesiswaan      | Kesiswaan           |
| tata_usaha     | Tata Usaha          |
| kepsek         | Pimpinan            |
| guru_walikelas | Guru dan Wali Kelas |

Gunakan actual role identifiers backend.

Reuse akun yang sudah tersedia hanya jika akun tersebut merupakan akun pengujian yang aman.

Jangan mengambil alih akun existing yang digunakan pengguna nyata.

Tambahkan:

- Akun Guru tambahan.
- Akun Wali Kelas tambahan.
- Akun multi-role.
- Akun nonaktif untuk negative login testing apabila diperlukan.

## Password requirements

Pengguna menginginkan password sederhana.

Gunakan password yang:

- Mudah diketik.
- Mudah diingat.
- Memenuhi minimum password validation aplikasi.
- Berbeda antar-akun utama apabila memungkinkan.

Jangan menonaktifkan password validator.

Jangan mengurangi password hashing.

Gunakan Django set_password() atau account creation service yang sah.

Jangan menyimpan plaintext password pada database.

Jangan menggunakan password PostgreSQL sebagai password aplikasi.

Jangan hardcode password aktif dalam repository.

Simpan daftar username dan password pengujian pada:

`docs/guide/ACCOUNTS.local.md`

Pastikan file tersebut diabaikan Git sebelum dibuat.

Password sederhana hanya boleh digunakan pada aplikasi lokal dengan synthetic dataset dan layanan yang tidak dapat diakses publik.

## RBAC requirements

- Administrator tidak memiliki universal bypass.
- Guru hanya memiliki akses sesuai penugasan.
- Wali Kelas memiliki scope kelas binaan.
- Tata Usaha tidak boleh melakukan approval Pimpinan.
- Pimpinan tidak boleh membaca catatan konseling privat.
- Multi-role mengikuti additive union dan privacy boundaries.

---

# 17. ENROLLMENTS & CLASS ASSIGNMENTS

Buat enrollment untuk seluruh siswa yang relevan.

Pastikan:

- Setiap siswa aktif memiliki kelas yang sesuai.
- Tidak terdapat enrollment overlap yang dilarang.
- Start date dan end date valid.
- Riwayat kenaikan kelas konsisten.
- Siswa pindah memiliki histori yang sesuai.
- Alumni tidak memiliki enrollment aktif yang tidak sah.

Buat penugasan Guru untuk kelas.

Gunakan approved assignment roles.

Baseline:

- GURU_MAPEL.
- WALI_KELAS.

Pastikan:

- Seluruh kelas aktif memiliki Wali Kelas.
- Guru memiliki assigned classes.
- Assignment dates sesuai tahun ajaran.
- Tidak ada overlap assignment yang dilarang.

Akun utama `guru` harus memiliki beberapa kelas yang bisa digunakan untuk pengujian presensi.

Akun utama `wali_kelas` harus memiliki kelas binaan yang lengkap.

Sediakan minimal satu kelas di luar scope kedua akun untuk negative authorization testing.

---

# 18. ATTENDANCE DATA

Isi presensi dengan variasi realistis.

Gunakan approved statuses:

- HADIR.
- SAKIT.
- IZIN.
- ALPA.

Contoh distribusi awal:

| Status | Proporsi |
| ------ | -------: |
| HADIR  |      92% |
| SAKIT  |       3% |
| IZIN   |       3% |
| ALPA   |       2% |

Gunakan distribusi berbeda antar-siswa, kelas dan tanggal.

Persentase tersebut merupakan parameter pembangkitan sintetis, bukan statistik resmi sekolah.

## Date coverage

Isi presensi sejak awal tahun ajaran aktif hingga tanggal saat ini.

Target sekitar 60–90 hari pembelajaran historis jika rentang tahun ajaran memungkinkan.

Jangan membuat presensi masa depan.

Gunakan hari pembelajaran Senin–Jumat sebagai asumsi lokal apabila kalender akademik resmi tidak tersedia.

Jangan mengklaim asumsi tersebut sebagai kalender resmi sekolah.

## Required attendance conditions

Sediakan:

- Presensi lengkap untuk sebagian besar kelas.
- Siswa sakit.
- Siswa izin.
- Siswa alpa.
- Siswa dengan histori ketidakhadiran.
- Tanggal yang belum dicatat untuk initial save.
- Tanggal yang dapat dikoreksi sesuai ketentuan.
- Data historis yang tidak dapat dikoreksi tanpa kewenangan.

Buat beberapa koreksi melalui mekanisme yang sah.

Gunakan domain services dan history hooks.

Patuhi CCR-20261114-01.

Gunakan:

- roster_version.
- expected_roster_version.

Sesuai actual approved contract.

Jangan melewati optimistic concurrency.

Jangan mengaktifkan pending correction policy.

Jangan langsung memalsukan history untuk mendapatkan jumlah record tertentu.

---

# 19. STUDENT AFFAIRS

Buat sekitar 60 kasus kesiswaan.

Gunakan kasus yang wajar:

- Keterlambatan masuk kelas.
- Ketidakhadiran tanpa keterangan.
- Ketidaksesuaian atribut sekolah.
- Keterlambatan pengumpulan tugas.
- Pembinaan kedisiplinan.
- Pendampingan akademik.
- Klarifikasi ketidakhadiran.
- Pembinaan tanggung jawab belajar.

Gunakan siswa sintetis yang telah tersedia.

Jangan menggunakan tuduhan berat, diagnosis, trauma atau informasi kesehatan sensitif.

Gunakan status:

- BARU.
- DIPROSES.
- SELESAI.
- DIBATALKAN.

Buat histori penanganan sesuai workflow.

Gunakan actual transition actions:

- MULAI_PENANGANAN.
- CATAT_TINDAKAN.
- SELESAIKAN.
- BATALKAN.

Pastikan:

- Timestamp konsisten.
- Aktor sesuai RBAC.
- Version konsisten.
- Tidak ada impossible state transitions.
- Tidak ada perubahan terminal state yang dilarang.

Buat catatan tindakan natural.

Contoh:

"Telah dilakukan pembinaan mengenai kedisiplinan dan tanggung jawab mengikuti kegiatan pembelajaran."

Gunakan mekanisme DEC-TECH-18 untuk melindungi catatan privat.

Jangan menonaktifkan masking.

Pimpinan dan Administrator tidak boleh memperoleh akses konseling privat hanya karena database berisi data pengujian.

Jangan membuat kasus otomatis berdasarkan threshold alpa yang masih pending.

---

# 20. ADMINISTRATION SERVICE TYPES

Buat sekitar 8–12 jenis layanan yang relevan.

Contoh kandidat:

- Surat Keterangan Aktif Sekolah.
- Surat Keterangan Siswa.
- Surat Keterangan Pindah Sekolah.
- Surat Keterangan Kelulusan.
- Surat Keterangan Beasiswa.
- Legalisasi Dokumen.
- Surat Pengantar Administrasi.
- Permohonan Salinan Dokumen.
- Surat Keterangan Pegawai.
- Permohonan Informasi Administrasi.

Gunakan schema yang tersedia.

Periksa requires_approval.

Patuhi keputusan bisnis yang telah disetujui.

Jika katalog layanan resmi belum tersedia, gunakan konfigurasi yang sah untuk pengujian terisolasi dan dokumentasikan sebagai asumsi.

Jangan menyatakan katalog tersebut sebagai layanan resmi SMA Negeri 1 Bunut.

Jangan mengaktifkan pending business policies.

---

# 21. SERVICE REQUESTS & WORKFLOW HISTORY

Buat sekitar 150 permohonan administrasi.

Gunakan nama pemohon dari siswa atau pegawai sintetis yang relevan.

Isi actual fields:

- Service type.
- Applicant name.
- Student reference jika tersedia.
- Purpose.
- Status.
- Version.
- Created timestamp.
- Updated timestamp.

Gunakan deskripsi natural.

Contoh:

- Melengkapi persyaratan administrasi beasiswa.
- Melengkapi dokumen pendaftaran pendidikan lanjutan.
- Permohonan legalisasi dokumen pendidikan.
- Melengkapi persyaratan kegiatan akademik.

Gunakan seluruh status yang disetujui:

- DIAJUKAN.
- DIPROSES.
- MENUNGGU_PERSETUJUAN.
- DISETUJUI.
- DITOLAK.
- SELESAI.

Sediakan:

- Antrean permohonan baru untuk Tata Usaha.
- Permohonan yang sedang diproses.
- Permohonan menunggu persetujuan Pimpinan.
- Permohonan disetujui.
- Permohonan ditolak.
- Permohonan selesai dengan dokumen terkait.

Buat service events melalui workflow yang sah.

## Approval workflow

DIAJUKAN → DIPROSES → MENUNGGU_PERSETUJUAN → DISETUJUI → SELESAI.

## Rejection workflow

DIAJUKAN → DIPROSES → MENUNGGU_PERSETUJUAN → DITOLAK.

Gunakan aktor sesuai kewenangan.

Jangan memberikan approval kepada Tata Usaha.

Jangan melanjutkan DITOLAK menjadi SELESAI.

Jangan mengaktifkan penomoran surat resmi yang masih pending.

Jangan memalsukan persetujuan sekolah yang sesungguhnya.

---

# 22. PHYSICAL PRIVATE DOCUMENTS

Buat sekitar 100–150 dokumen sintetis yang benar-benar tersedia secara fisik.

Jangan hanya membuat metadata tanpa file.

Gunakan ReportLab, Pillow atau existing libraries yang sesuai.

Format:

- PDF.
- PNG jika diperlukan.
- JPEG jika diperlukan.

Contoh isi:

- Lampiran pengajuan administrasi.
- Ringkasan keperluan siswa.
- Formulir pengajuan.
- Dokumen pendukung.
- Arsip administrasi pengujian.

Gunakan format dokumen yang rapi.

Jangan menggunakan tanda tangan kepala sekolah nyata, stempel resmi atau nomor surat resmi yang belum disahkan.

Dokumen hasil seeding harus memiliki penanda bahwa dokumen tersebut tidak berlaku sebagai dokumen resmi.

Penanda cukup berada pada file dokumen atau metadata yang sesuai, bukan pada seluruh UI aplikasi.

Gunakan:

- PRIVATE_MEDIA_ROOT.
- UUID storage key.
- Existing storage service.

Pastikan:

- Metadata valid.
- Physical file tersedia.
- MIME type benar.
- File size valid.
- File dapat diunduh oleh role berwenang.
- Role tidak berwenang tetap ditolak.
- Tidak ada public media URL untuk dokumen privat.
- Upload dan storage validation tetap berlaku.

Gunakan isolated private media directory untuk dataset pengujian.

---

# 23. ACTIVITY LOGS & HISTORICAL DATA

Isi activity logs melalui aktivitas seeding yang benar-benar dijalankan.

Gunakan existing audit hooks dan domain services.

Cakup:

- Account creation.
- Academic year creation.
- Student creation.
- Enrollment.
- Assignment.
- Attendance.
- Attendance correction.
- Case creation.
- Case transitions.
- Service request creation.
- File upload.
- Approval.
- Rejection.
- Completion.

Jangan membuat log login palsu seolah-olah pengguna nyata telah mengakses sistem.

Jangan memalsukan security events.

Jangan mengarang timestamp historis yang bertentangan dengan event sebenarnya.

Jika synthetic historical records diperlukan, catat provenance pada level teknis.

Jangan menyimpan password, JWT atau catatan konseling privat dalam activity logs.

---

# 24. DASHBOARD & REPORT CONSISTENCY

Pastikan seluruh enam dashboard menampilkan data dari API dan database nyata.

## Administrator

Metrik master data dan akun sesuai kontrak.

## Guru

Informasi kelas penugasan dan presensi sesuai scope.

## Wali Kelas

Ringkasan kelas binaan dan rekap kehadiran.

## Kesiswaan

Distribusi kasus dan antrean penanganan.

## Tata Usaha

Permohonan berdasarkan status dan arsip sesuai scope.

## Pimpinan

Agregasi sekolah dan antrean persetujuan sesuai RBAC.

Gunakan actual DashboardMetricsResponse.

Jangan mengarang KPI.

Jika dashboard kosong padahal database sudah berisi data, investigasi:

- Backend query.
- Object scope.
- Date filters.
- Enrollment.
- Assignment.
- Cache invalidation.
- Frontend query keys.

Verifikasi:

- Rekap presensi.
- Filter kelas.
- Filter tanggal.
- Ekspor Excel.
- Laporan administrasi PDF.
- Private document download.
- Audit logs.
- Server-side pagination.
- Search.
- Aggregation consistency.

Bandingkan hasil API dengan database.

Jangan mengubah perhitungan agar dashboard terlihat lebih menarik.

---

# 25. REUSABLE DJANGO SEED COMMAND

Periksa management commands yang sudah tersedia.

Jika belum terdapat seeder lengkap, implementasikan reusable command.

Suggested command:

`python manage.py seed_school_data`

Gunakan nama aktual sesuai konvensi repository.

Suggested options:

- --seed.
- --profile.
- --students.
- --employees.
- --classes.
- --academic-years.
- --attendance-days.
- --cases.
- --requests.
- --dry-run.

Jangan mendokumentasikan opsi yang belum diimplementasikan.

Sediakan minimal:

- Small profile untuk automated tests.
- Full profile untuk pengujian aplikasi lokal.
- Deterministic random seed.
- Dry-run atau equivalent safe preflight.
- Database target verification.
- Progress reporting.
- Idempotent rerun.

Seeder harus:

- Reproducible.
- Aman dijalankan ulang.
- Tidak membuat duplicate records.
- Tidak menimpa data pengguna tanpa izin.
- Mengikuti foreign key dependencies.
- Mengikuti business invariants.
- Mengikuti transaction rules.
- Memiliki clear error handling.

Jangan menjalankan seeder otomatis setiap aplikasi startup.

Jangan menggunakan Faker pada runtime HTTP.

Source code seeder disimpan pada direktori backend yang sesuai.

Jangan menyimpan source code seeder dalam docs/guide.

---

# 26. SAFE SEEDING & DATABASE PROTECTION

Sebelum menjalankan seeder:

1. Verifikasi environment aktif.
2. Verifikasi database engine.
3. Verifikasi database target.
4. Verifikasi lokasi database.
5. Verifikasi existing record counts.
6. Verifikasi private media root.
7. Pastikan target diizinkan.
8. Backup data existing apabila diperlukan.

Seeder wajib menolak production environment.

Jika data pengujian tidak dapat dibedakan dari existing records secara aman, gunakan dedicated synthetic database.

DILARANG:

- flush pada database pengguna.
- DROP DATABASE.
- TRUNCATE CASCADE.
- Penghapusan seluruh pengguna.
- Penghapusan seluruh private media.
- Penghapusan data sekolah existing.
- Reset otomatis.
- Overwrite akun existing yang tidak diketahui kepemilikannya.

Jika opsi reset diperlukan, gunakan hanya untuk target sintetis terisolasi dengan konfirmasi eksplisit.

Jangan mengubah OpenAPI atau DBML hanya demi seeding.

Jangan menambahkan seed metadata field ke business model tanpa kebutuhan dan governance yang sah.

---

# 27. SEEDING PERFORMANCE & PROGRESS

Dataset dapat mencapai puluhan ribu attendance records.

Optimalkan:

- Query count.
- Batch insertion.
- Transaction boundaries.
- Memory usage.
- Foreign key lookups.
- Duplicate detection.
- History generation.
- Cache invalidation.

Gunakan bulk_create apabila tidak melewati validation, history, audit atau business invariants.

Gunakan existing bulk history mechanism jika tersedia.

Gunakan domain services untuk state transitions.

Jangan menghilangkan history demi performa.

Tampilkan progress yang informatif:

```text
[01/12] Memeriksa environment
[02/12] Menyiapkan roles
[03/12] Menyiapkan tahun ajaran
[04/12] Membuat rombongan belajar
[05/12] Membuat pegawai
[06/12] Membuat akun pengguna
[07/12] Membuat siswa dan enrollment
[08/12] Membuat penugasan guru
[09/12] Mengisi data presensi
[10/12] Mengisi kasus kesiswaan
[11/12] Mengisi permohonan dan dokumen
[12/12] Memverifikasi integritas data
```

Tampilkan:

- Total target.
- Created.
- Reused.
- Failed.
- Progress percentage.
- Execution duration.

Jangan mencetak password.

---

# 28. BACKEND RUNNING PROCEDURE

Gunakan PowerShell Windows.

Backend path:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\backend`

Verifikasi dan dokumentasikan:

1. Masuk ke backend directory.
2. Aktifkan existing virtual environment.
3. Pilih environment.
4. Periksa database.
5. Periksa Redis.
6. Jalankan Django system check.
7. Jalankan migrasi.
8. Jalankan seeder.
9. Jalankan backend.
10. Verifikasi healthcheck.

Contoh prosedur awal:

```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo\backend"

.\.venv\Scripts\Activate.ps1

$env:DJANGO_ENV = "development"

python manage.py check
python manage.py migrate
python manage.py seed_school_data
python manage.py runserver 127.0.0.1:8000
```

Sesuaikan dengan actual environment loader dan command yang benar-benar diimplementasikan.

Jangan menjalankan migrasi atau seeder sebelum database target diverifikasi.

Sediakan alternatif menjalankan backend melalui Granian.

Gunakan actual ASGI application path dan installed Granian version.

Jangan mengarang command.

Backend target URL:

`http://127.0.0.1:8000/api`

Verifikasi actual healthcheck endpoint dan OpenAPI documentation path.

---

# 29. FRONTEND RUNNING PROCEDURE

Frontend path:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend`

Periksa:

- package.json.
- package-lock.json.
- node_modules.
- Vite configuration.
- frontend/.env.
- API base URL.
- Backend proxy target.
- Port.

Contoh awal:

```powershell
cd "D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend"

npm run dev
```

Gunakan actual package script.

Jangan menjalankan npm install apabila dependencies sudah tersedia dan berfungsi.

Frontend target:

`http://localhost:3000`

Pastikan frontend:

- Berhasil dibuka.
- Terhubung dengan backend nyata.
- Tidak memiliki duplicate /api prefix.
- Tidak mengalami CORS error pada konfigurasi yang benar.
- Dapat login.
- Dapat mengambil data.
- Dapat melakukan mutasi.
- Dapat mengunggah dan mengunduh file sesuai permission.

---

# 30. OPTIONAL ONE-COMMAND STARTUP

Jika memungkinkan tanpa menambah kompleksitas berlebihan, implementasikan PowerShell helper.

Suggested path:

`scripts/start-local.ps1`

Script harus:

- Menentukan root project secara dinamis.
- Memeriksa Python virtual environment.
- Memeriksa Node.js.
- Memeriksa environment files.
- Memeriksa Redis.
- Memeriksa database.
- Memeriksa port availability.
- Menjalankan backend.
- Menjalankan frontend.
- Menampilkan service URLs.
- Menampilkan status startup.
- Menangani shutdown terhadap proses yang dibuat script.

Jangan menghentikan seluruh proses Python atau Node.js.

Jangan menghentikan proses yang bukan milik startup script.

Jangan menjalankan seeder otomatis pada setiap startup.

Seeding dilakukan melalui command terpisah.

Jangan hardcode password.

Jika file ownership tidak mengizinkan helper script, cukup sediakan prosedur manual yang telah diverifikasi.

---

# 31. LOCAL BROWSER VERIFICATION

Setelah seeding selesai, jalankan backend dan frontend.

Gunakan Playwright atau browser aktual.

Uji seluruh enam role utama.

## Administrator

- Login.
- Dashboard.
- Manajemen akun.
- Tahun ajaran.
- Kelas.
- Pegawai.
- Siswa.
- Enrollment.
- Teacher assignments.
- Audit logs.

## Guru

- Login.
- Dashboard.
- Kelas penugasan.
- Attendance roster.
- Input presensi.
- Bulk save.
- Rekap.
- Export sesuai permission.

## Wali Kelas

- Login.
- Dashboard.
- Kelas binaan.
- Rekap kehadiran.
- Informasi kasus sesuai scope.

## Kesiswaan

- Login.
- Dashboard.
- Case list.
- Case detail.
- Pembuatan kasus.
- Penanganan.
- Pencatatan tindakan.
- Timeline.
- Penyelesaian kasus.

## Tata Usaha

- Login.
- Dashboard.
- Daftar permohonan.
- Permohonan baru.
- Upload.
- Pemrosesan.
- Pengajuan persetujuan.
- Arsip.
- Download.
- Laporan.

## Pimpinan

- Login.
- Dashboard.
- Antrean persetujuan.
- Detail permohonan sesuai scope.
- Persetujuan.
- Penolakan.
- Laporan.

## Multi-role

- Login.
- Role union.
- Navigation context.
- Object scope.
- Privacy boundaries.

Pastikan tidak ada:

- Blank page.
- Critical JavaScript errors.
- Fake API response.
- Incorrect API path.
- Unexpected HTTP 500.
- Unauthorized access.
- Cross-user leakage.
- Private counseling leakage.

Jangan mengklaim seluruh fitur teruji apabila hanya membuka dashboard.

Untuk mutasi penting, verifikasi perubahan database setelah tindakan browser.

---

# 32. DATABASE INTEGRITY VERIFICATION

Setelah seeding, jalankan actual database queries.

Laporkan counts:

- Roles.
- Users.
- Employees.
- Academic years.
- Active academic years.
- Classes.
- Students.
- Active students.
- Alumni.
- Enrollments.
- Class assignments.
- Attendance records.
- Historical attendance records.
- Cases.
- Case events.
- Service types.
- Service requests.
- Service events.
- Documents.
- Physical private files.
- Activity logs.

Bandingkan target dan actual counts.

Verifikasi:

- No orphan records.
- No invalid foreign keys.
- No duplicate identifiers.
- No invalid enum values.
- No invalid date ranges.
- No impossible state transitions.
- No document metadata without physical file.
- No prohibited enrollment overlap.
- No conflicting assignments.
- Exactly one active academic year.
- Dashboard aggregate consistency.

Jangan mengarang hasil query.

Catat verification summary di TECHNICAL_GUIDE.md.

Jangan membuat laporan seeding tambahan.

---

# 33. SEEDER AUTOMATED TESTS

Buat permanent automated tests untuk seeder.

Cakup:

- Successful seed execution.
- Deterministic generation.
- Idempotent rerun.
- Unique student identifiers.
- Academic year constraints.
- Enrollment integrity.
- Assignment integrity.
- Attendance validity.
- Valid state transitions.
- Physical document existence.
- Password hashing.
- Role assignments.
- Production environment rejection.
- Data preservation.
- No duplicate records.

Gunakan isolated automated test database.

Gunakan small profile agar test suite tetap cepat.

Jangan menjalankan full dataset pada setiap unit test.

Jangan mengubah existing tests agar cocok dengan seeded dataset.

---

# 34. FINAL REGRESSION

Pertahankan baseline yang telah dilaporkan:

- Backend: 110 PASS, 1 SKIPPED.
- Frontend: 74 Vitest PASS.
- Browser: 6 Playwright PASS.
- Integration: 8 gates.
- N2N: 20 checks.
- Multi-worker: 9 verification steps.

Jalankan actual relevant suites.

## Backend

- Django system check.
- Migration consistency.
- Full applicable pytest.
- Seeder tests.
- Ruff check.
- Ruff format check.

## Frontend

- Typecheck.
- Existing Vitest suite.
- Existing Playwright suite.
- Production build.
- Lint dan format checks jika tersedia.

## Integration

- Live healthcheck.
- Login enam role.
- API connectivity.
- Seed integrity.
- Dashboard consistency.
- Private documents.
- Report exports.
- Workflow verification.

Jangan menghapus existing valid tests.

Jika test gagal:

1. Reproduce.
2. Investigasi source code.
3. Periksa actual contract.
4. Periksa RBAC.
5. Periksa fixture.
6. Identifikasi root cause.
7. Perbaiki melalui pemilik kode yang sah.
8. Jalankan regression test.
9. Jalankan suite terdampak.

Jangan menonaktifkan security atau validation agar test lulus.

Jika menemukan critical security issue, laporkan dan jangan klaim kesiapan penggunaan tanpa penyelesaian yang diperlukan.

---

# 35. SIMPLIFIED DOCUMENTATION OUTPUT

Seluruh panduan wajib disimpan pada:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\docs\guide`

Buat hanya:

```text
docs/
└── guide/
    ├── TECHNICAL_GUIDE.md
    ├── USER_GUIDE.md
    └── ACCOUNTS.local.md
```

Jangan membuat:

- README.md.
- RUNNING_GUIDE.md.
- DATABASE_SEEDING_GUIDE.md.
- USER_ACCOUNTS_GUIDE.md.
- USER_OPERATION_GUIDE.md.
- SYSTEM_TESTING_GUIDE.md.
- TROUBLESHOOTING.md.
- SEEDING_REPORT.md.
- LOCAL_SETUP_REPORT.md.
- File laporan tambahan lainnya.

Gabungkan seluruh informasi ke dua dokumen master.

ACCOUNTS.local.md hanya digunakan untuk menyimpan kredensial pengujian lokal.

Jangan membuat subfolder images baru.

Jika screenshot diperlukan, gunakan existing frontend/evidence atau integration evidence directory yang sesuai.

Referensikan screenshot dari dokumen master menggunakan relative path.

Jangan menduplikasi screenshot yang sudah tersedia dan masih relevan.

---

# 36. TECHNICAL_GUIDE.MD — MASTER TECHNICAL DOCUMENT

Lokasi:

`docs/guide/TECHNICAL_GUIDE.md`

Gabungkan seluruh panduan teknis dalam satu dokumen.

Gunakan struktur berikut:

## BAB 1 — Gambaran Sistem

- Nama aplikasi.
- Arsitektur singkat.
- Teknologi.
- Struktur project.
- Runtime configuration.

## BAB 2 — Quick Start

Letakkan langkah tercepat menjalankan sistem di bagian awal.

Cakup:

- Redis startup.
- Backend startup.
- Frontend startup.
- Browser URL.
- Lokasi kredensial lokal.

Quick Start harus dapat langsung digunakan tanpa membaca seluruh dokumen.

## BAB 3 — Prerequisites

- Python.
- Virtual environment.
- Node.js.
- npm.
- Existing dependencies.
- Redis.
- Database.

## BAB 4 — Environment Configuration

- backend/.env.
- backend/.env.integration.
- frontend/.env.
- Environment loader.
- DATABASE_URL.
- REDIS_URL.
- VITE_API_BASE_URL.
- BACKEND_PROXY_TARGET.
- ENV_FILE.
- DJANGO_ENV.
- Private media configuration.

Gunakan placeholder untuk credentials sensitif.

## BAB 5 — Database Configuration

- SQLite WAL.
- PostgreSQL 16 WSL2.
- PostgreSQL 17 Windows.
- Cara mengganti database.
- Cara memverifikasi database aktif.
- Migration.
- Backup.
- Database isolation.

Bedakan konfigurasi yang sudah diuji dan yang masih belum terverifikasi.

## BAB 6 — Redis Configuration

- Distribusi WSL2 aktual.
- Service startup.
- Connectivity.
- Redis verification.
- Effective cache settings.

## BAB 7 — Database Seeding

- Faker locale.
- Seed command.
- Available command options.
- Small dan full profiles.
- Random seed.
- Data generation order.
- Idempotency.
- Safe database selection.
- Backup.
- Rerun procedure.
- Data relationship explanation.

## BAB 8 — Hasil Populasi Database

Gunakan tabel:

| Entitas | Target | Actual | Status |
| ------- | -----: | -----: | ------ |

Isi berdasarkan query database aktual.

Jelaskan asal sintetis data dan tujuan pengujian.

## BAB 9 — Running Backend

- PowerShell commands.
- Virtual environment.
- Environment selection.
- Django system check.
- Migrations.
- Seeder.
- Django runserver.
- Granian alternative.
- Healthcheck.
- API documentation.

## BAB 10 — Running Frontend

- PowerShell commands.
- Environment.
- Vite.
- API connectivity.
- Browser access.
- Production build jika diperlukan.

## BAB 11 — One-Command Startup

Dokumentasikan helper apabila benar-benar dibuat.

Jika tidak dibuat, gunakan manual startup procedure.

## BAB 12 — Technical Verification

- Backend tests.
- Frontend tests.
- Seeder tests.
- Browser tests.
- Database integrity.
- Actual API verification.
- Redis.
- Relevant integration checks.
- Known limitations.

## BAB 13 — Troubleshooting

Cakup:

- Redis tidak aktif.
- Backend gagal startup.
- Port sudah digunakan.
- Database connection error.
- PostgreSQL authentication error.
- Missing environment variables.
- Migration error.
- Seeder error.
- Duplicate records.
- Frontend API connection error.
- CORS.
- Login gagal.
- Dashboard kosong.
- Private file missing.
- Export gagal.
- HTTP 401.
- HTTP 403.
- HTTP 409.
- HTTP 422.
- HTTP 429.
- HTTP 500.

Gunakan solusi berdasarkan actual source code.

## BAB 14 — Shutdown, Backup & Maintenance

- Cara menghentikan backend.
- Cara menghentikan frontend.
- Cara menghentikan proses helper.
- Database backup.
- Private file backup.
- Cara menggunakan ulang dataset.
- Cara mencegah data loss.

## BAB 15 — Final Setup Status

- Runtime URLs.
- Database engine.
- Redis status.
- Actual record counts.
- Actual test results.
- Known blockers.
- Final readiness decision.

Gunakan bahasa Indonesia yang jelas.

Jangan menulis panduan terlalu teoritis.

Gunakan command yang sudah diverifikasi.

---

# 37. USER_GUIDE.MD — MASTER USER DOCUMENT

Lokasi:

`docs/guide/USER_GUIDE.md`

Gabungkan seluruh panduan penggunaan sistem untuk enam role.

Gunakan bahasa Indonesia yang mudah dipahami pengguna sekolah.

Hindari istilah teknis seperti JWT, DTO, Redis, payload dan database query.

Gunakan struktur:

## BAB 1 — Pengenalan Aplikasi

- Tujuan aplikasi.
- Fungsi utama.
- Pengguna sistem.
- Cara mengakses aplikasi.

## BAB 2 — Login dan Navigasi

- Cara login.
- Mengenali dashboard.
- Menggunakan sidebar.
- Mengakses profil.
- Logout.
- Mengatasi login gagal.

## BAB 3 — Pemetaan Role dan Hak Akses

Buat tabel yang menjelaskan:

| Role | Menu | Aksi yang diperbolehkan | Batasan akses |
| ---- | ---- | ----------------------- | ------------- |

Gunakan actual RBAC dan menu frontend.

Jangan mengarang fitur.

## BAB 4 — Panduan Administrator

Jelaskan langkah:

- Mengelola akun.
- Mengatur role.
- Mengelola tahun ajaran.
- Mengelola kelas.
- Mengelola pegawai.
- Mengelola siswa.
- Mengatur penempatan.
- Mengatur penugasan.
- Mengelola jenis layanan sesuai kewenangan.
- Melihat audit aktivitas.

## BAB 5 — Panduan Guru

Jelaskan:

- Melihat kelas penugasan.
- Memilih tanggal.
- Mengisi presensi.
- Memeriksa data sebelum menyimpan.
- Melakukan koreksi sesuai aturan.
- Membaca rekap.
- Mengunduh laporan sesuai izin.
- Menangani konflik penyimpanan.

## BAB 6 — Panduan Wali Kelas

Jelaskan:

- Melihat kelas binaan.
- Melihat data siswa sesuai scope.
- Melihat rekap presensi.
- Melihat kasus yang diizinkan.
- Melakukan tindakan yang diperbolehkan.
- Memahami pembatasan catatan privat.

## BAB 7 — Panduan Kesiswaan

Jelaskan:

- Melihat daftar kasus.
- Membuat kasus.
- Memulai penanganan.
- Mencatat tindakan.
- Melihat timeline.
- Menyelesaikan kasus.
- Membatalkan kasus sesuai kewenangan.
- Menjaga kerahasiaan informasi.

## BAB 8 — Panduan Tata Usaha

Jelaskan:

- Melihat daftar permohonan.
- Membuat permohonan.
- Mengunggah lampiran.
- Memproses permohonan.
- Mengajukan persetujuan.
- Menyelesaikan permohonan.
- Mengelola arsip.
- Mengunduh dokumen.
- Membuat laporan sesuai fitur.

## BAB 9 — Panduan Pimpinan

Jelaskan:

- Melihat dashboard.
- Membuka antrean persetujuan.
- Memeriksa permohonan.
- Menyetujui.
- Menolak dengan alasan.
- Melihat statistik.
- Mengunduh laporan sesuai kewenangan.

## BAB 10 — Alur Kerja Antar-Role

Jelaskan workflow secara sederhana:

### Workflow Akademik

Administrator → Master Data → Enrollment → Teacher Assignment.

### Workflow Presensi

Guru → Pencatatan Presensi → Wali Kelas → Rekap → Laporan sesuai kewenangan.

### Workflow Kesiswaan

Pembuatan Kasus oleh Aktor Berwenang → Penanganan → Pencatatan Tindakan → Penyelesaian.

### Workflow Persuratan

Tata Usaha → Permohonan → Pemrosesan → Pimpinan → Persetujuan/Penolakan → Penyelesaian dan Arsip sesuai status.

Gunakan flowchart Mermaid apabila membantu.

Jangan membuat workflow yang tidak tersedia.

## BAB 11 — Panduan Pengujian Manual

Gabungkan seluruh manual testing scenarios.

Gunakan tabel:

| ID | Role | Preconditions | Langkah | Expected Result | Actual Result | Status | Catatan |
| -- | ---- | ------------- | ------- | --------------- | ------------- | ------ | ------- |

Cakup:

- Login.
- Accounts.
- Master Data.
- Enrollment.
- Assignment.
- Attendance.
- Attendance conflict.
- Recap.
- Student affairs.
- Privacy.
- Service requests.
- Approval.
- Rejection.
- Upload.
- Download.
- Reports.
- Audit.
- Multi-role.
- Unauthorized access.

Biarkan kolom Actual Result, Status dan Catatan kosong untuk pengujian manual pengguna yang belum dilakukan.

Jangan mengarang hasil UAT, SUS atau pengujian pengguna sekolah.

## BAB 12 — Masalah Umum Pengguna

Jelaskan dengan bahasa sederhana:

- Lupa password.
- Tidak dapat login.
- Tidak menemukan menu.
- Tidak dapat membuka kelas tertentu.
- Tidak dapat menyimpan presensi.
- Konflik penyimpanan.
- Permohonan tidak dapat diproses.
- Dokumen tidak dapat diunduh.
- Sesi berakhir.

Jelaskan hanya tindakan yang benar-benar didukung aplikasi.

Jangan mengarang fitur reset password atau bantuan otomatis.

---

# 38. ACCOUNTS.LOCAL.MD — LOCAL CREDENTIALS

Lokasi:

`docs/guide/ACCOUNTS.local.md`

File ini wajib dilindungi Git.

Tambahkan ignore rule yang diperlukan sebelum file dibuat.

Isi:

| Username | Password lokal | Role | Penugasan kelas | Keterangan |
| -------- | -------------- | ---- | --------------- | ---------- |

Sediakan minimal:

- admin.
- guru.
- wali_kelas.
- kesiswaan.
- tata_usaha.
- kepsek.
- guru_walikelas.

Gunakan actual credentials yang sudah dibuat dan diuji.

Tambahkan akun pengujian lain jika diperlukan.

Password harus mudah digunakan dan memenuhi validation aplikasi.

Jangan memasukkan:

- PostgreSQL password.
- Redis password.
- Django secret key.
- JWT.
- Access token.
- Refresh token.
- API secret.

Berikan peringatan singkat dalam file bahwa credentials tersebut hanya boleh digunakan pada pengujian lokal.

Jangan commit atau push file ini.

Verifikasi menggunakan Git check-ignore dan pemeriksaan tracked files.

Jangan hanya mengasumsikan .gitignore sudah berfungsi.

---

# 39. SCREENSHOT & VISUAL EVIDENCE

Jika diperlukan, gunakan screenshot frontend aktual.

Prioritaskan:

- Login.
- Enam dashboard.
- Master data.
- Presensi.
- Kasus kesiswaan.
- Permohonan.
- Persetujuan.
- Arsip.

Gunakan existing frontend/evidence.

Jangan membuat banyak file dokumentasi baru hanya untuk screenshot.

Referensikan gambar yang relevan dari USER_GUIDE.md.

Jangan menampilkan:

- Password.
- JWT.
- Database credentials.
- Environment secrets.
- Data pribadi nyata.

Jangan menggunakan gambar Pencil sebagai bukti aplikasi yang sedang berjalan.

---

# 40. FINAL DELIVERABLES

Pekerjaan dianggap selesai apabila:

1. Backend dapat dijalankan.
2. Frontend dapat dijalankan.
3. Redis nyata dapat digunakan.
4. Frontend terhubung dengan API aktual.
5. Database lokal sudah terisi data realistis.
6. Seluruh entitas yang relevan memiliki data.
7. Seluruh enam role memiliki akun yang dapat digunakan.
8. Reusable seeder tersedia.
9. Seeder aman dijalankan ulang.
10. Data relational integrity terverifikasi.
11. Private documents tersedia secara fisik.
12. Dashboard berasal dari database.
13. Report exports berfungsi.
14. Workflow utama dapat diuji.
15. Existing valid regression tests dipertahankan.
16. Dua dokumen master tersedia.
17. File kredensial lokal terlindungi Git.

Dokumentasi akhir hanya:

- docs/guide/TECHNICAL_GUIDE.md.
- docs/guide/USER_GUIDE.md.
- docs/guide/ACCOUNTS.local.md.

Tidak boleh membuat laporan Markdown tambahan yang menduplikasi isi dokumen master.

Source code, tests, environment files dan startup scripts tetap berada pada direktori implementasi yang sesuai.

---

# 41. FINAL EXECUTION SUMMARY

Pada akhir pekerjaan, tampilkan ringkasan pada terminal atau chat.

## Runtime

- Frontend URL.
- Backend URL.
- Healthcheck URL.
- Database engine.
- Redis status.

## Seed results

- Total users.
- Total employees.
- Total academic years.
- Total classes.
- Total students.
- Total enrollments.
- Total assignments.
- Total attendance records.
- Total cases.
- Total service requests.
- Total documents.
- Total audit records.

## Account verification

Tampilkan:

- Username.
- Role.
- Assigned class apabila relevan.
- Login verification status.

Jangan mencetak password aktif pada log umum.

Arahkan pengguna ke ACCOUNTS.local.md.

## Verification

- Backend test results.
- Frontend test results.
- Seeder test results.
- Playwright results.
- Integration checks.
- Seed integrity.
- Known limitations.

## Documentation

Tampilkan tiga path dokumen yang telah dibuat.

Jika server ditinggalkan berjalan, tampilkan actual PID, port dan cara menghentikan proses terkait dengan aman.

---

# 42. FINAL READINESS STATUS

Gunakan:

`READY — LOCAL_APPLICATION_RUNNING_AND_POPULATED`

Hanya jika:

- Backend berjalan.
- Frontend berjalan.
- Redis terhubung.
- Database terisi.
- Login enam role berhasil.
- Data dari API tampil pada aplikasi.
- Seeder berhasil dijalankan.
- Integritas data terverifikasi.
- Workflow utama dapat digunakan.
- Dokumentasi selesai.

Jika sebagian pekerjaan berhasil tetapi masih terdapat verification gaps:

`CONDITIONALLY_READY — LOCAL_APPLICATION_AVAILABLE_WITH_OPEN_ITEMS`

Jika aplikasi belum dapat digunakan:

`BLOCKED — LOCAL_SETUP_REQUIRES_ATTENTION`

Jangan mengklaim READY apabila hanya membuat dokumentasi.

Jangan menganggap local readiness sebagai production readiness.

Jangan mengklaim UAT, SUS atau evaluasi penelitian telah dilakukan.

---

# 43. FINAL EXECUTION INSTRUCTION

Mulai sekarang.

Jangan membangun ulang proyek.

Jangan mengganti framework.

Jangan mengubah business rules, RBAC atau kontrak tanpa governance yang sah.

Gunakan environment yang sudah tersedia.

Gunakan SQLite WAL sebagai default database lokal.

Gunakan Redis WSL2 yang sudah tersedia.

Sediakan PostgreSQL sebagai alternatif sesuai environment aktual.

Isi seluruh database domain menggunakan Faker Indonesia.

Buat data yang realistis, lengkap, konsisten dan saling terhubung.

Buat aplikasi terasa seperti sistem administrasi sekolah yang digunakan sehari-hari.

Jangan menggunakan mock API atau hardcoded frontend data.

Jangan menampilkan tulisan demo, dummy, mockup atau simulasi pada UI operasional.

Seluruh data harus benar-benar tersimpan di database.

Buat akun seluruh role dengan password sederhana khusus pengujian lokal.

Jangan mengurangi keamanan password atau RBAC.

Implementasikan reusable seeder.

Jalankan seeder secara nyata pada database lokal yang aman.

Verifikasi seluruh relasi data.

Verifikasi physical private documents.

Jalankan backend dan frontend.

Verifikasi login seluruh role.

Verifikasi workflow utama melalui browser.

Jika ditemukan bug, perbaiki root cause dan jalankan regression tests.

Buat hanya tiga file panduan di:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\docs\guide`

Yaitu:

1. TECHNICAL_GUIDE.md.
2. USER_GUIDE.md.
3. ACCOUNTS.local.md.

Gabungkan seluruh panduan teknis ke TECHNICAL_GUIDE.md.

Gabungkan seluruh panduan penggunaan dan manual testing scenarios ke USER_GUIDE.md.

Simpan password akun pengujian hanya pada ACCOUNTS.local.md yang terlindungi Git dan mekanisme environment lokal yang aman.

Jangan membuat dokumen panduan tambahan.

Jangan berhenti setelah membuat script.

Selesaikan pekerjaan sampai aplikasi benar-benar dapat digunakan untuk pengujian fitur berdasarkan data yang tersimpan dalam database.

Laporkan final readiness berdasarkan bukti aktual.
