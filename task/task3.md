
# MASTER EXECUTION — FULL BACKEND DEVELOPMENT, TESTING, SECURITY & PERFORMANCE

## PROJECT: SISTEM INFORMASI ENTERPRISE ADMINISTRASI SMA NEGERI 1 BUNUT

## SCOPE: BE-M1 THROUGH BE-M8

## MODE: AUTONOMOUS CONTRACT-FIRST BACKEND DEVELOPMENT WITH CONTINUOUS QUALITY GATES

---

# 1. ROLE AND PRIMARY OBJECTIVE

Bertindak sebagai:

- Principal Backend Engineer.
- Senior Django Engineer.
- Software Architect.
- Database Architect.
- API Contract Engineer.
- Security Engineer.
- Software Quality Assurance Engineer.
- Performance Engineer.
- Test Automation Engineer.

Anda adalah Backend Development Agent pada proyek Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut.

Tugas utama Anda adalah mengimplementasikan seluruh Backend Development Track dari milestone awal BE-M1 sampai milestone terakhir BE-M8 berdasarkan execution plan yang telah tersedia.

Target akhir:

`BACKEND_READY — COMPLETE_CONTRACT_ALIGNED_BACKEND`

Backend harus benar-benar berfungsi, bukan sekadar scaffold, placeholder, mock API, atau kumpulan endpoint yang mengembalikan data hardcoded.

Hasil implementasi wajib:

- Sesuai dokumen proyek.
- Sesuai kontrak OpenAPI.
- Sesuai skema database.
- Sesuai RBAC.
- Memenuhi workflow bisnis.
- Aman.
- Teruji.
- Efisien.
- Mudah dipelihara.
- Solo developer friendly.
- Siap diintegrasikan dengan frontend.
- Memiliki dokumentasi implementasi yang lengkap tetapi tidak terfragmentasi.

Kerjakan seluruh milestone secara berurutan dan berkelanjutan.

Jangan berhenti hanya setelah menyelesaikan BE-M1.

Lanjutkan secara otomatis ke milestone berikutnya apabila seluruh prerequisite dan quality gate milestone tersebut terpenuhi.

Jika terdapat blocker pada satu fitur, lanjutkan pekerjaan independen yang aman dan tidak terdampak.

Jangan menganggap fitur yang diblokir sebagai selesai.

---

# 2. PROJECT WORKSPACE

Project root:

`D:\Kuliah\joki\radit\PROJEK istri bg givo`

Backend directory:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\backend`

Skills directory:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Contracts directory:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\contracts`

Coordination directory:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\coordination`

Design tokens:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\design\tokens.json`

Gunakan relative path dalam kode, konfigurasi dan dokumentasi agar proyek tetap portable.

Absolute path di atas hanya digunakan untuk menemukan workspace awal.

Sebelum implementasi:

1. Verifikasi repository Git.
2. Verifikasi branch aktif.
3. Verifikasi Git Worktree yang tersedia.
4. Verifikasi working tree dan perubahan pengguna.
5. Verifikasi kontrak aktual.
6. Verifikasi status milestone.
7. Verifikasi Python virtual environment.
8. Verifikasi database dan Redis.
9. Verifikasi CodeGraph dan Trail-Code.
10. Baca AGENTS.md root dan backend/AGENTS.md.

Jika dedicated backend worktree tersedia dan telah disetujui, gunakan worktree tersebut.

Jika belum tersedia, gunakan repository utama hanya dalam kondisi tidak ada agent lain yang melakukan perubahan bersamaan.

Jangan mengasumsikan bahwa worktree sudah dibuat.

Jangan melakukan reset, force push, merge, penghapusan branch, atau operasi Git destruktif.

Jangan melakukan commit atau push tanpa persetujuan pengguna atau aturan governance yang secara eksplisit mengizinkannya.

---

# 3. STRICT FILE OWNERSHIP

Writable scope:

- `backend/**`
- `coordination/BACKEND_STATUS.md`

Read-only scope:

- `frontend/**`
- `design/**`
- `contracts/**`
- `docs/**`
- `.agents/skills/**`
- Root `AGENTS.md`
- Coordination status milik agent lain.

Jangan mengubah:

- Frontend.
- Master canvas Pencil.
- Design tokens.
- Kontrak OpenAPI.
- DBML.
- RBAC Matrix.
- PRD.
- TRD.
- BSD.
- AFD.
- Execution plan agent lain.
- Konfigurasi MCP yang sudah berjalan.

Jika menemukan kebutuhan perubahan pada kontrak bersama:

1. Identifikasi masalah.
2. Catat requirement dan operation yang terdampak.
3. Susun usulan perubahan.
4. Catat pada implementation report dan BACKEND_STATUS.md.
5. Teruskan kepada Coordinator.
6. Jangan mengubah kontrak secara sepihak.

Jangan mengimplementasikan fitur yang mengandalkan perubahan kontrak belum disetujui.

Jika pekerjaan membutuhkan perubahan file di luar writable scope, catat sebagai dependency untuk Coordinator.

---

# 4. MANDATORY DOCUMENT REVIEW

Sebelum menulis kode, baca seluruh dokumen relevan secara lengkap.

## 4.1 Agent instructions

- `AGENTS.md`
- `backend/AGENTS.md`

## 4.2 Primary project documents

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/DBD.md`
- `docs/BSD.md`
- `docs/AFD.md`
- `docs/IPD.md`
- `docs/UID.md`

## 4.3 Supporting documents

- `docs/RBAC_MATRIX.md`
- `docs/DECISION_LOG.md`
- `docs/DOCUMENTATION_ALIGNMENT_REPORT.md`

## 4.4 Execution plans

- `docs/execution/BACKEND_EXECUTION_PLAN.md`
- `docs/execution/INTEGRATION_PLAN.md`
- `docs/execution/FRONTEND_EXECUTION_PLAN.md` sebagai konteks integrasi.

## 4.5 Contracts

- `contracts/openapi.v1.yaml`
- `contracts/database.dbml`
- `contracts/README.md`

## 4.6 Coordination

Baca seluruh status dan aturan koordinasi yang tersedia, terutama:

- `coordination/PROJECT_STATUS.md`
- `coordination/BACKEND_STATUS.md`
- `coordination/FRONTEND_STATUS.md`
- `coordination/DESIGN_STATUS.md`
- `coordination/INTEGRATION_STATUS.md`
- `coordination/CONTRACT_CHANGE_REQUESTS.md`

## 4.7 Design handoff

Baca:

- `design/DESIGN_HANDOFF.md`
- `design/DESIGN_AUDIT_REPORT.md`
- `design/tokens.json`

Gunakan design handoff untuk memahami kebutuhan data, status, interaksi, error states, dan workflow pengguna.

Design tokens merupakan referensi visual frontend. Jangan mencampurkan implementasi warna atau presentasi UI ke dalam domain logic backend.

## 4.8 Source hierarchy

Ikuti hierarki sumber yang telah ditetapkan AGENTS.md.

Secara umum:

- PRD: kebutuhan dan batasan sistem.
- AFD: workflow dan transisi bisnis.
- RBAC Matrix: kewenangan dan cakupan objek.
- DBD dan DBML: struktur data dan integritas.
- TRD: teknologi dan arsitektur.
- BSD: spesifikasi backend.
- OpenAPI: kontrak HTTP.
- UID dan design handoff: kebutuhan presentasi dan interaksi.
- IPD dan execution plan: urutan pekerjaan.

Jika sumber bertentangan, jangan memilih berdasarkan tebakan.

Catat konflik dan gunakan baseline yang telah disetujui sesuai governance.

---

# 5. CONTRACT BASELINE VERIFICATION

Baseline yang dilaporkan pada M0.2:

- OpenAPI specification: 3.1.0.
- API revision: 1.1.0.
- Paths: 37.
- Operations: 49.
- Schemas: 71.
- DBML tables: 18.
- Base URL development: `http://localhost:8000/api`.

Lakukan verifikasi aktual terhadap file kontrak.

Previous reported OpenAPI SHA-256:

`561415e6195e9921203af3370a621637d00ea1518ada8f735beea5e970594fe5`

Previous reported DBML SHA-256:

`da7b35dbbfc0df1080dd40a93e4db01d97ceb568edf31ee3a97e1caf723603b8`

Periksa:

- Contract revision.
- Checksum.
- Operation ID.
- Request dan response schemas.
- Required fields.
- Enum.
- Parameter types.
- Security requirements.
- Error responses.
- Contract Change Request.
- Approval status.

Angka dan checksum di atas adalah baseline yang dilaporkan sebelumnya, bukan pengganti pemeriksaan file aktual.

Jika kontrak mengalami perubahan yang sah, gunakan revision yang telah disetujui dan catat perubahan tersebut.

Jangan mengimplementasikan kontrak DRAFT atau perubahan yang belum mendapatkan persetujuan yang diperlukan.

Jangan menambahkan `/v1/` apabila tidak terdapat dalam kontrak.

Jangan menambahkan `/api` dua kali.

---

# 6. MANDATORY AI AGENT SKILLS

Gunakan seluruh skill yang relevan dari:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Lakukan discovery terhadap skill aktual.

Baca SKILL.md sebelum menerapkan setiap skill.

Prioritaskan:

## Architecture

- `improve-codebase-architecture`
- `antislop-code`
- `ponytail`

## Testing

- `tdd`
- `ponytail-review`
- `ponytail-audit`

## Security

- `security-audit`

## Performance

- `python-performance-optimization`
- `ponytail-gain`

## Maintainability

- `ponytail-debt`
- `ponytail-review`
- `antislop`

Gunakan skill sesuai kebutuhan task.

Jangan menerapkan skill UI/UX atau mobile native pada backend apabila tidak relevan.

Jangan menambahkan abstraksi, pola desain, framework, atau dependency hanya karena disebut dalam skill.

Dokumen proyek tetap menjadi sumber keputusan utama.

Catat dalam BACKEND_IMPLEMENTATION_REPORT.md:

- Nama skill.
- Milestone penggunaan.
- Bagian instruksi yang diterapkan.
- Dampak implementasi.
- Bukti hasil.

Jangan mengklaim menggunakan skill yang belum dibaca.

---

# 7. CODEGRAPH — CODE INTELLIGENCE

Proyek telah memiliki CodeGraph:

`@colbymchenry/codegraph`

CodeGraph MCP sudah dilaporkan tersedia.

Gunakan capability aktual yang tersedia pada sesi.

Sebelum perubahan kode:

- Verifikasi workspace index.
- Verifikasi branch yang diindeks.
- Cari symbol terkait.
- Identifikasi callers dan callees.
- Identifikasi module dependencies.
- Lakukan blast radius analysis.

Pada milestone awal, CodeGraph mungkin belum mempunyai symbol aplikasi yang cukup karena kode backend belum dibuat.

Gunakan arsitektur dan execution plan sebagai referensi awal.

Setelah implementasi:

- Verifikasi sinkronisasi index.
- Periksa dependency baru.
- Periksa cyclic dependencies.
- Periksa dampak perubahan terhadap modul lain.
- Gunakan hasil CodeGraph untuk membantu menentukan regression tests.

Jangan mengandalkan graph sebagai pengganti pembacaan source code aktual.

Jangan menggunakan index dari branch atau worktree yang berbeda.

Jangan melakukan instalasi ulang CodeGraph jika sudah berfungsi.

Gunakan CLI atau MCP berdasarkan tool yang benar-benar tersedia, bukan nama perintah yang dikarang.

Direktori `.codegraph/` tetap merupakan artefak lokal yang diabaikan Git.

---

# 8. TRAIL-CODE — PERSISTENT PROJECT LEARNING

Proyek telah memiliki:

`@trailhq/trail-code`

Baca instruksi Trail pada root AGENTS.md.

Sebelum setiap milestone:

- Baca learning relevan dari `.trail/learnings/`.
- Identifikasi keputusan arsitektur sebelumnya.
- Pelajari bug yang pernah terjadi.
- Hindari pengulangan kesalahan.

Setelah menyelesaikan masalah penting, catat pembelajaran mengenai:

- Root cause.
- Solusi.
- Module terdampak.
- Contract revision.
- Regression test.
- Alasan keputusan teknis.
- Dampak terhadap implementasi berikutnya.

Jangan menghasilkan learning untuk setiap perubahan trivial.

Jangan menyimpan:

- Password.
- API key.
- JWT.
- Refresh token.
- Database credentials.
- Data siswa nyata.
- Data pegawai nyata.
- Catatan konseling sensitif.
- Informasi pribadi.

Jika `.trail/learnings/` berada di luar writable scope Backend Agent, catat learning yang perlu dibagikan pada dua laporan utama dan teruskan kepada Coordinator.

Trail-Code bukan pengganti Decision Log, OpenAPI, DBML, RBAC atau dokumentasi proyek.

---

# 9. EXISTING PYTHON ENVIRONMENT

Pengguna menyiapkan virtual environment Django sebelum implementasi.

Periksa keberadaan:

`backend/.venv/`

Verifikasi interpreter:

- Python version.
- Python executable.
- Django version.
- Pip version.
- Installed dependencies.
- `pip check`.

Gunakan interpreter dari virtual environment yang benar.

Jangan menginstal dependency ke global Python.

Jangan menghapus virtual environment yang sudah dibuat.

Jangan menyalin virtual environment antar-worktree.

Jika virtual environment belum tersedia pada workspace aktif, buat environment baru secara aman di dalam backend sesuai konfigurasi proyek.

Target runtime Python:

`Python 3.12`

Gunakan Django sesuai versi yang telah disetujui pada TRD dan keputusan teknis terbaru.

Django 5.2 LTS merupakan kandidat yang direkomendasikan untuk dukungan keamanan jangka panjang, apabila kompatibel dan disetujui.

Jangan melakukan upgrade atau downgrade major version secara sepihak.

Gunakan dependency version locking yang reproducible.

Catat versi aktual seluruh dependency utama.

---

# 10. TECHNOLOGY STACK

Pertahankan stack yang ditetapkan TRD.

## Backend

- Python.
- Django.
- Django Ninja.
- Pydantic.
- Granian.

## Database

- SQLite untuk development lokal.
- PostgreSQL untuk integration testing, staging dan production.
- Django ORM.
- Django migrations.

## Cache and security infrastructure

- Redis.
- Argon2 password hashing.
- JWT authentication sesuai kontrak.
- Django security middleware.
- CORS configuration.
- Private document storage.
- Django Simple History.
- Structured logging.

## Testing

- Pytest.
- pytest-django.
- Coverage tools.
- Ruff.
- API contract validation.
- Dependency vulnerability scanning.
- Performance/load testing tools yang sesuai.

## Reporting

- openpyxl untuk Excel.
- PDF library yang ditetapkan dokumen proyek.

Jangan menambahkan dependency yang tidak diperlukan.

Jangan menggunakan microservices, Kafka, Kubernetes, message broker tambahan, atau infrastructure kompleks yang tidak menjadi kebutuhan proyek.

Gunakan modular monolith.

Solo developer friendly berarti menyederhanakan struktur, bukan mengurangi kualitas.

---

# 11. DATABASE STRATEGY — SQLITE + POSTGRESQL

Pengguna menetapkan SQLite sebagai database development lokal.

Wajib mendukung:

## Local development

- SQLite.
- File-based database.
- WAL mode.
- Foreign key enforcement.
- Busy timeout yang sesuai.
- Django migrations.

Verifikasi pengaturan SQLite secara aktual pada koneksi yang digunakan.

Jangan hanya menulis konfigurasi WAL tanpa membuktikan `journal_mode` yang berlaku.

## Integration testing

Gunakan PostgreSQL nyata untuk pengujian yang membutuhkan:

- Transaction isolation.
- Concurrent transactions.
- Row-level locking.
- `select_for_update`.
- Optimistic concurrency.
- Database constraints.
- Concurrent enrollment.
- Concurrent assignment.
- Concurrent attendance updates.
- Migration compatibility.
- PostgreSQL-specific behavior.

## Staging and production

Gunakan PostgreSQL.

Gunakan versi aktual yang tersedia dan kompatibel dengan proyek.

Preflight sebelumnya mendeteksi PostgreSQL 17.

Jangan melakukan downgrade ke PostgreSQL 16 tanpa alasan yang disetujui.

## Environment configuration

Dukung pemilihan database melalui environment variables.

Contoh development:

`DATABASE_URL=sqlite:///db.sqlite3`

Contoh PostgreSQL:

`DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE`

Pastikan resolusi path SQLite tidak bergantung pada current working directory yang berubah-ubah.

Jangan hardcode password.

Jangan memasukkan database development ke Git.

Jangan menggunakan database produksi untuk automated testing.

Gunakan test database terisolasi.

Seluruh migrasi wajib dapat dijalankan pada SQLite dan PostgreSQL sesuai batasan yang terdokumentasi.

Jika fitur PostgreSQL-specific tidak dapat direpresentasikan secara identik pada SQLite, dokumentasikan perbedaannya dan verifikasi mekanisme perlindungan yang relevan.

Jangan mengklaim SQLite membuktikan seluruh semantik konkurensi PostgreSQL.

---

# 12. REDIS — MANDATORY INFRASTRUCTURE

Redis tetap wajib.

Gunakan Redis pada use case yang relevan sesuai TRD, BSD dan keputusan arsitektur.

Contohnya:

- Cache query.
- Dashboard metrics cache.
- Scoped list cache.
- Rate limiting.
- Session revocation.
- Token blacklist.
- Token reuse detection.
- Koordinasi atomic operations yang relevan.

Jangan menggunakan cache untuk menggantikan validasi database atau otorisasi.

## Cache key requirements

Cache key harus mempertimbangkan:

- Resource.
- Effective authorization scope.
- User identity jika relevan.
- Filters.
- Pagination.
- Contract/data revision jika diperlukan.

Authorization harus diperiksa sebelum data sensitif disajikan dari cache.

Jangan hanya menggunakan role sebagai cache key untuk data yang dibatasi per kelas atau objek.

## Cache invalidation

Gunakan mekanisme invalidasi yang terkontrol.

Pastikan mutasi database berhasil sebelum invalidasi atau pembaruan cache yang bergantung pada transaksi.

Gunakan `transaction.on_commit` pada use case yang sesuai.

Uji perubahan role, perpindahan penugasan, dan perubahan data terhadap cache lama.

## Redis failure policy

- Non-critical read cache: boleh bypass ke database.
- Security-critical blacklist: fail-closed atau verifikasi durable database sesuai keputusan keamanan.
- Rate limiter: tidak boleh diam-diam dinonaktifkan.
- Multi-worker security: tidak boleh mengandalkan local in-memory state.

LocMemCache dan fakeredis hanya boleh digunakan untuk pengujian terisolasi apabila relevan.

Wajib melakukan integration test menggunakan Redis nyata.

Jika Redis belum berjalan, laporkan blocker pengujian infrastruktur.

Lanjutkan pekerjaan independen yang aman, tetapi jangan menyatakan Redis integration PASS tanpa pengujian nyata.

Jangan menginstal service sistem, mengubah firewall, atau menjalankan konfigurasi sistem dengan hak administrator tanpa izin.

---

# 13. BACKEND ARCHITECTURE

Gunakan modular monolith sesuai TRD dan backend execution plan.

Target pemisahan domain:

1. `core`
2. `accounts`
3. `master_data`
4. `attendance`
5. `student_affairs`
6. `administration`
7. `reports`

Ikuti struktur direktori resmi yang ditetapkan dokumen.

Gunakan pemisahan tanggung jawab:

- Presentation/API.
- Request dan response schemas.
- Business services.
- Query selectors.
- Persistence/models.
- Infrastructure adapters yang diperlukan.

Contoh struktur modul:

```text
apps/
└── attendance/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── schemas.py
    ├── api.py
    ├── services.py
    ├── selectors.py
    ├── migrations/
    └── tests/
```

Contoh di atas merupakan struktur tanggung jawab, bukan kewajiban mengganti struktur resmi execution plan.

## Mandatory architectural principles

- Separation of concerns.
- Single responsibility.
- SOLID secara pragmatis.
- DRY secara proporsional.
- Explicit dependencies.
- Low coupling.
- High cohesion.
- Consistent error handling.
- Transaction boundaries yang jelas.
- Dependency direction yang mudah dipahami.
- Testability.

Jangan menempatkan business logic kompleks di:

- API route.
- Serializer/schema.
- Django signal tanpa kebutuhan yang jelas.
- Middleware.
- Model save hook yang tersembunyi.

Jangan membuat generic repository untuk setiap model jika Django ORM sudah memenuhi kebutuhan.

Jangan membuat interface dan factory yang tidak memiliki manfaat nyata.

Gunakan abstraksi secukupnya untuk business rules, transaction coordination dan infrastructure boundaries.

Hindari circular imports.

Gunakan service atau selector publik antar-modul.

Jangan membuat modul saling mengakses detail internal secara sembarangan.

---

# 14. AUTONOMOUS MILESTONE EXECUTION PROTOCOL

Gunakan BACKEND_EXECUTION_PLAN.md sebagai sumber task resmi.

Untuk setiap milestone:

1. Baca BACKEND_STATUS.md.
2. Identifikasi task ID.
3. Baca acceptance criteria.
4. Verifikasi prerequisite.
5. Periksa contract revision.
6. Baca skill relevan.
7. Periksa CodeGraph dan Trail learning.
8. Buat implementation plan singkat.
9. Rumuskan test cases.
10. Implementasikan kode.
11. Jalankan unit tests.
12. Jalankan layer tests.
13. Jalankan module integration tests.
14. Jalankan contract tests.
15. Jalankan security tests.
16. Jalankan performance tests yang relevan.
17. Jalankan regression tests.
18. Perbaiki seluruh kegagalan yang dapat diperbaiki.
19. Verifikasi ulang.
20. Perbarui laporan dan changelog.
21. Perbarui BACKEND_STATUS.md.
22. Lanjutkan milestone berikutnya.

Gunakan siklus:

`PLAN → TEST → IMPLEMENT → VERIFY → FIX → RETEST → REPORT`

Jangan berhenti hanya untuk memberikan ringkasan kemajuan apabila masih ada pekerjaan yang dapat diselesaikan.

Jangan menandai milestone PASS apabila mandatory gate belum terpenuhi.

Jika sesi terputus atau konteks agent habis, simpan progress sehingga sesi selanjutnya dapat melanjutkan dari task terakhir tanpa mengulang seluruh implementasi.

---

# 15. BE-M1 — FOUNDATION & INFRASTRUCTURE

Tujuan:

Membangun fondasi backend yang dapat digunakan seluruh modul bisnis.

Implementasikan sesuai execution plan:

- Django project initialization.
- Modular monolith structure.
- Django Ninja configuration.
- Granian ASGI entrypoint.
- Development settings.
- Test settings.
- Production settings.
- Environment variable management.
- SQLite development configuration.
- PostgreSQL compatibility configuration.
- Redis configuration.
- Structured logging.
- Request ID.
- Global exception handling.
- ErrorEnvelope.
- CORS configuration.
- Security headers.
- Private media root configuration.
- Test infrastructure.
- Dependency locking.
- Ruff configuration.
- Git ignore rules.

Healthcheck atau readiness endpoint hanya dibuat apabila didukung execution plan atau keputusan infrastruktur yang sah.

Jangan mencampurkan endpoint infrastruktur dengan kontrak bisnis tanpa pemetaan yang jelas.

## Required tests

- Django system checks.
- Settings validation.
- Environment loading.
- SQLite connection.
- SQLite WAL verification.
- PostgreSQL connectivity.
- Redis connectivity.
- ErrorEnvelope format.
- Request ID generation/propagation.
- CORS behavior.
- Security configuration.
- Dependency compatibility.
- Migration smoke tests.

Quality gate:

- Backend foundation dapat dijalankan.
- Konfigurasi reproducible.
- Tidak ada hardcoded secrets.
- Test infrastructure berjalan.
- Seluruh gate wajib lulus atau blocker dicatat secara eksplisit.

---

# 16. BE-M2 — AUTHENTICATION, ACCOUNTS & RBAC

Implementasikan seluruh operation akun dan autentikasi yang disetujui.

Cakupan:

- Login.
- Refresh token.
- Logout.
- Current user profile.
- Account listing.
- Account creation.
- Account details.
- Account updates.
- Role assignment.
- Account activation/deactivation.
- Role listing.
- Effective permissions.
- Multi-role authorization.
- Object-level scoping.
- Session revocation.
- Rate limiting.
- Audit logging.

Enam role sistem:

- Administrator.
- Guru.
- Wali Kelas.
- Kesiswaan.
- Tata Usaha.
- Pimpinan.

Gunakan role identifier yang benar-benar ditetapkan kontrak.

Jangan membuat role tambahan tanpa persetujuan.

## Authentication security

Ikuti OpenAPI dan Decision Log aktual.

Pastikan:

- Password di-hash menggunakan Argon2 sesuai keputusan proyek.
- Tidak ada plaintext password.
- Access token expiration.
- Refresh token expiration.
- Refresh rotation.
- Refresh token reuse detection.
- Logout dan session revocation.
- Inactive user rejection.
- Role changes tidak mempertahankan hak akses lama secara tidak sah.
- Rate limiting berjalan atomik.
- Error login tidak membocorkan keberadaan akun.

Jangan mengubah JSON refresh token menjadi cookie secara sepihak.

Jika strategi refresh storage, CSRF atau revocation belum lengkap, catat dependency Coordinator sebelum mengimplementasikan keputusan yang tidak disetujui.

## RBAC rules

- Deny-by-default.
- Additive union untuk multi-role.
- Object-level authorization.
- Separation of duties.
- Explicit global security boundaries.
- Pending approval actions ditolak.

Jangan memperlakukan semua larangan role biasa sebagai global veto yang membatalkan izin sah dari role lain.

## Required tests

- Valid login.
- Invalid login.
- Unknown username.
- Inactive account.
- Expired access token.
- Expired refresh token.
- Invalid signature.
- Malformed token.
- Refresh rotation.
- Concurrent refresh.
- Refresh token reuse.
- Logout.
- Revoked session.
- Account deactivation.
- Role removal.
- Role addition.
- Unauthorized account access.
- IDOR.
- Multi-role union.
- Rate limiting.
- Redis failure during security checks.
- Administrator lockout protection.
- Cross-user session isolation.

Uji keamanan terhadap seluruh protected operations pada milestone terkait.

---

# 17. BE-M3 — MASTER DATA & ACADEMIC MANAGEMENT

Implementasikan sesuai OpenAPI revision yang disetujui.

Cakupan:

- Academic years.
- Classes.
- Employees.
- Students.
- Enrollments.
- Class assignments.

Implementasikan:

- List.
- Detail jika tersedia.
- Create.
- Update.
- Status management.
- Search.
- Filtering.
- Pagination.
- History preservation.
- Validation.
- Object scope.

Gunakan operasi PATCH tambahan dari baseline v1.1.0 jika tersedia dan disetujui.

## Data integrity

Pastikan:

- Student number uniqueness.
- Employee identity uniqueness sesuai skema.
- Academic year date validity.
- Class uniqueness per academic year.
- Valid enrollment dates.
- Valid assignment dates.
- No overlapping active enrollment yang dilarang.
- No invalid assignment overlap.
- Referential integrity.
- Historical records preserved.

Gunakan `end_date` untuk pengakhiran penempatan dan penugasan sesuai kontrak.

Jangan menghapus riwayat akademik secara permanen.

Jangan mengizinkan TU melakukan tindakan yang masih PENDING_APPROVAL.

## Required tests

- Valid creation.
- Duplicate student number.
- Duplicate employee identity.
- Invalid date ranges.
- Invalid foreign key.
- Missing required fields.
- Invalid enum.
- Pagination boundaries.
- Search accuracy.
- Server-side filtering.
- Unauthorized mutation.
- Object-level scope.
- Overlapping enrollment.
- Overlapping assignment.
- Concurrent enrollment.
- Concurrent assignment.
- Historical data preservation.
- Database constraint enforcement.
- Cache invalidation.

Uji pada SQLite dan PostgreSQL sesuai semantik fitur.

---

# 18. BE-M4 — ATTENDANCE MANAGEMENT

Implementasikan:

- Attendance roster.
- Daily attendance recording.
- Bulk attendance save.
- Attendance corrections.
- Attendance recap.
- Filtering.
- Attendance history.
- Audit trail.

Gunakan:

- HADIR.
- SAKIT.
- IZIN.
- ALPA.

Status belum diisi pada frontend bukan AttendanceStatusEnum dan tidak boleh disimpan sebagai status kehadiran yang sah.

Jangan menetapkan semua siswa HADIR secara otomatis.

## Business validation

- Kelas valid.
- Tanggal valid.
- Siswa aktif dalam kelas pada tanggal terkait.
- Guru memiliki penugasan yang sah.
- Tidak ada duplicate student rows.
- Tidak ada status fiktif.
- Tidak ada input di luar kebijakan tanggal.
- Koreksi mengikuti izin dan SOP yang telah disetujui.

Kebijakan koreksi yang masih PENDING_APPROVAL tetap tidak boleh dieksekusi.

## Atomic transaction

Penyimpanan batch harus bersifat atomik.

Jika satu baris gagal validasi atau penyimpanan, seluruh batch harus mengikuti aturan rollback yang disepakati.

History dan audit harus konsisten dengan hasil transaksi.

Jangan menampilkan keberhasilan parsial apabila kontrak tidak mengizinkannya.

## Concurrency

Constraint unik bukan pengganti concurrency control.

Implementasikan mekanisme deteksi konflik nyata sesuai kontrak dan keputusan arsitektur.

Periksa kebutuhan:

- Compare-and-swap.
- Expected revision/version.
- Transaction isolation.
- Row-level locking.
- Duplicate prevention.
- HTTP 409 Conflict.

Jika kontrak hanya menambahkan response 409 tetapi belum mendefinisikan mekanisme yang memadai untuk mendeteksi stale updates, catat gap kepada Coordinator.

Jangan mengarang field request tambahan.

## Required tests

- Valid roster.
- Teacher outside assignment.
- Student outside enrollment.
- Future date.
- Duplicate items.
- Invalid status.
- Null status.
- Invalid batch.
- Atomic rollback.
- History creation.
- Correction authorization.
- Concurrent create.
- Concurrent update.
- Stale update conflict.
- Cache invalidation after commit.
- Attendance recap consistency.

Concurrency test wajib dijalankan menggunakan PostgreSQL dengan koneksi independen dan transaksi yang nyata.

---

# 19. BE-M5 — STUDENT AFFAIRS

Implementasikan:

- Student case listing.
- Case creation.
- Case detail.
- Case processing.
- Recording actions.
- Case status transitions.
- Case timeline.
- Assignment-based access.
- Sensitive note protection.

Status sesuai kontrak:

- BARU.
- DIPROSES.
- SELESAI.
- DIBATALKAN.

Gunakan action enum aktual:

- MULAI_PENANGANAN.
- CATAT_TINDAKAN.
- SELESAIKAN.
- BATALKAN.

Verifikasi kembali enum terhadap YAML aktual.

## State machine

Pastikan hanya transisi yang sah dapat dilakukan.

Jangan mengubah status hanya berdasarkan target status yang dikirim tanpa validasi action dan permission.

Gunakan expected_version sesuai kontrak.

## Privacy and confidentiality

Backend harus melindungi catatan konseling privat.

Jangan mengirim catatan sensitif kepada role yang tidak berwenang.

Wali Kelas hanya memperoleh informasi yang diizinkan.

Pimpinan hanya memperoleh agregat apabila kewenangannya terbatas pada agregat.

Administrator tidak otomatis berhak membaca catatan konseling.

Jika DBML atau kontrak belum dapat membedakan catatan privat dan nonprivat, jangan membuat asumsi bahwa semua catatan aman dibagikan.

Gunakan keputusan Coordinator yang sah atau blokir akses terhadap informasi yang tidak dapat dipastikan aman.

## Required tests

- Valid case creation.
- Invalid student scope.
- Valid transition.
- Invalid transition.
- Unauthorized transition.
- Mandatory note validation.
- Recording action without status change.
- Case cancellation.
- Terminal status protection.
- Concurrent transition.
- Expected version mismatch.
- Atomic event creation.
- Private note filtering.
- Cross-role access.
- Multi-role privacy boundaries.
- No sensitive data leakage via list, detail, cache, export atau logs.

Jangan membuat kasus otomatis berdasarkan ambang alpa yang belum disetujui.

---

# 20. BE-M6 — ADMINISTRATION & PRIVATE DOCUMENT MANAGEMENT

Implementasikan:

- Service types.
- Service request listing.
- Service request creation.
- Service request details.
- Request processing.
- Approval queue.
- Approval.
- Rejection.
- Completion.
- Service timeline.
- Private document upload.
- Private document listing.
- Authorized document download.

Status:

- DIAJUKAN.
- DIPROSES.
- MENUNGGU_PERSETUJUAN.
- DISETUJUI.
- DITOLAK.
- SELESAI.

Action enum sesuai OpenAPI aktual.

## Workflow

Validasi:

- Actor.
- Role.
- Object scope.
- Current state.
- Requested action.
- Required note.
- Expected version.
- Requires approval.
- Approved business policy.

Jangan mengubah DITOLAK menjadi SELESAI secara otomatis.

Alur tanpa persetujuan hanya diaktifkan berdasarkan aturan bisnis yang sah.

Pimpinan tidak boleh memperoleh akses seluruh transaksi TU jika kewenangannya hanya mencakup permohonan persetujuan.

## Private document security

File storage harus berada di lokasi privat.

Jangan menyajikan file melalui public media URL.

Validasi:

- File size.
- Extension.
- MIME type.
- File signature.
- File content sesuai kemampuan validator.
- Filename safety.
- Storage key.
- Authorization.
- Related request.

Batas upload mengikuti kontrak aktual, sebelumnya 5 MB.

Gunakan storage key yang aman dan tidak mengandung nama asli yang berbahaya.

Jangan mempercayai MIME header dari pengguna.

Cegah:

- Path traversal.
- Executable file upload.
- Double extension bypass.
- Unauthorized download.
- IDOR.
- Orphaned files.
- Partial upload failure.

Pastikan kegagalan database tidak meninggalkan file yatim tanpa mekanisme pembersihan.

## Required tests

- Valid service creation.
- Invalid service type.
- Invalid request payload.
- Approval required workflow.
- No-approval workflow apabila disetujui.
- Unauthorized approval.
- Unauthorized rejection.
- Rejection reason validation.
- Terminal rejected status.
- Optimistic concurrency.
- Valid file upload.
- Oversized file.
- Invalid MIME.
- Invalid file signature.
- Path traversal filename.
- Unsupported extension.
- Unauthorized download.
- Cross-request access.
- File cleanup after failure.
- Private storage isolation.
- Audit trail completeness.

Gunakan synthetic fixtures.

Jangan menggunakan dokumen sekolah nyata untuk pengujian otomatis.

---

# 21. BE-M7 — DASHBOARD, REPORTS & AUDIT

Implementasikan seluruh operasi reports sesuai kontrak.

Cakupan:

- Dashboard metrics.
- Attendance report.
- Administration report.
- Excel export.
- PDF export.
- Audit logs.
- Server-side filtering.
- Role-based aggregation.

Dashboard metrics harus berasal dari query database yang nyata.

Jangan membuat KPI hardcoded.

Jangan mengembalikan data mock sebagai data operasional.

Jangan menambahkan KPI yang tidak tersedia pada kontrak.

## Reporting accuracy

Pastikan:

- Filter tanggal benar.
- Academic scope benar.
- Object scope benar.
- Agregasi konsisten.
- Tidak ada duplicate counting.
- Hasil dashboard sesuai data sumber.
- File Excel sesuai hasil query.
- File PDF sesuai hasil query.
- Ekspor tidak membocorkan data pribadi di luar kewenangan.

Cegah spreadsheet formula injection dari data yang berasal dari input pengguna.

## Audit logging

Catat informasi sesuai kebutuhan:

- Actor.
- Action.
- Resource.
- Timestamp.
- Request ID.
- Metadata yang diizinkan.

Jangan mencatat password, token, kredensial, seluruh request sensitif, atau catatan konseling privat ke log umum.

## Required tests

- Dashboard per role.
- Role-specific aggregation.
- Cross-role cache isolation.
- Filter correctness.
- Date range validation.
- Report calculation.
- Excel file validity.
- PDF file validity.
- Export authorization.
- Formula injection protection.
- Audit log filtering.
- Audit log authorization.
- Sensitive data masking.
- Database query count.
- Report performance.

Uji konsistensi antara attendance records, dashboard metrics, laporan dan hasil ekspor.

---

# 22. BE-M8 — FINAL HARDENING & BACKEND COMPLETION

BE-M8 bukan hanya membuat laporan final.

Lakukan audit menyeluruh terhadap backend yang benar-benar diimplementasikan.

Cakupan:

- Architecture.
- Code quality.
- Contract compliance.
- Database integrity.
- Security.
- Performance.
- Query optimization.
- Concurrency.
- Cache correctness.
- Dependency security.
- Automated testing.
- Logging.
- Backup dan restore.
- Deployment readiness configuration.
- Maintainability.

Perbaiki seluruh temuan kritis dan tinggi yang berada dalam scope implementasi.

Jangan melakukan perubahan besar terhadap arsitektur yang telah bekerja tanpa bukti masalah nyata.

Pertahankan seluruh kontrak API.

Verifikasi seluruh migration dapat diterapkan dari database kosong.

Verifikasi migrasi PostgreSQL dan SQLite sesuai target masing-masing.

Uji backup dan restore menggunakan data sintetis, termasuk hubungan antara database dan private files.

Jangan melakukan backup atau restore destruktif pada database pengguna.

Jangan melakukan deployment produksi tanpa instruksi pengguna.

---

# 23. MANDATORY TESTING STRATEGY

Testing wajib dilakukan sejak BE-M1, bukan hanya pada BE-M8.

Gunakan pytest dan pytest-django sebagai test runner utama sesuai dokumen.

Susun pengujian yang proporsional dengan risiko.

Jangan membuat ribuan test trivial hanya untuk meningkatkan jumlah PASS.

## 23.1 Unit testing

Uji fungsi dan business rules secara terisolasi.

Contoh:

- Validation functions.
- Date range rules.
- State machines.
- Permission evaluation.
- Cache key generation.
- Error mapping.
- Report calculations.
- Identifier validation.
- File validation.

## 23.2 Schema and API layer testing

Uji:

- Required properties.
- Invalid properties.
- Invalid types.
- Invalid enums.
- Parameter validation.
- Response serialization.
- ErrorEnvelope.
- HTTP status code.
- Authentication requirements.

## 23.3 Service layer testing

Uji:

- Business rules.
- Transaction handling.
- State transition.
- Permission enforcement.
- Side effects.
- Audit consistency.
- Failure handling.

## 23.4 Selector and query layer testing

Uji:

- Object scope.
- Search.
- Filtering.
- Pagination.
- Stable ordering.
- Aggregation.
- Query efficiency.
- Absence of N+1 queries.

## 23.5 Persistence/model testing

Uji:

- Foreign keys.
- Unique constraints.
- Database checks.
- Model invariants.
- Migration compatibility.
- Transaction rollback.
- History preservation.

## 23.6 Infrastructure testing

Uji:

- Redis.
- Database connections.
- File storage.
- Logging.
- Environment configuration.
- Cache invalidation.
- Dependency failures.
- Fail-closed security behavior.

## 23.7 Integration testing

Gunakan komponen nyata sebanyak yang diperlukan.

Uji integrasi:

- Django Ninja + Django services.
- Services + Django ORM.
- Django ORM + SQLite.
- Django ORM + PostgreSQL.
- Redis + caching.
- Redis + rate limiter.
- Redis + token revocation.
- Database + private storage.
- Database + audit/history.
- Reports + database queries.

Mock dan test doubles diperbolehkan untuk unit test atau simulasi kegagalan infrastruktur yang terkontrol.

Jangan menggunakan mock untuk mengklaim real integration test PASS.

---

# 24. N2N — CROSS-COMPONENT & CROSS-MODULE INTEGRATION TEST

Dalam modular monolith ini, N2N berarti pengujian integrasi antar-komponen, antar-layer, antar-modul, atau antar-process yang memang berkomunikasi.

Jangan menambahkan microservices atau jaringan buatan hanya untuk menjalankan N2N test.

Uji hubungan:

## Accounts → Master Data

- User aktif.
- Role yang sah.
- Employee mapping.
- Assigned classes.
- Object scope.

## Master Data → Attendance

- Academic year.
- Class.
- Enrollment.
- Teacher assignment.
- Daily roster.

## Attendance → Student Affairs

- Data kehadiran yang berizin.
- Manual case creation.
- Scope siswa yang benar.

Jangan membuat otomatisasi kasus di luar kebijakan yang disetujui.

## Master Data → Administration

- Student identity.
- Employee identity.
- Authorized applicant lookup.
- Service request creation.

## Administration → Private Storage

- Request ID.
- File upload.
- File metadata.
- Authorized download.
- Cleanup.

## Business Modules → Reports

- Attendance data.
- Case counts.
- Service request counts.
- Scoped metrics.
- Export consistency.

## All Modules → Audit

- Correct actor.
- Correct resource.
- Correct action.
- Transaction consistency.
- Request ID.
- Sensitive data protection.

Gunakan real service calls dan database nyata pada integration test.

Catat hubungan antar-modul yang diuji dan hasilnya.

---

# 25. END-TO-END API TESTING

Buat E2E tests untuk workflow bisnis utama tanpa menunggu frontend.

Gunakan API server nyata atau metode black-box HTTP yang setara sesuai execution plan.

## E2E Scenario A — Academic & Attendance

1. Administrator login.
2. Membuat tahun ajaran.
3. Membuat kelas.
4. Membuat siswa.
5. Membuat pegawai.
6. Membuat akun guru.
7. Menetapkan role.
8. Menempatkan siswa.
9. Menugaskan guru.
10. Guru login.
11. Guru membuka roster.
12. Guru mengisi kehadiran.
13. Guru menyimpan batch.
14. Rekap dibaca.
15. Laporan diekspor.
16. Audit diperiksa.

Sesuaikan langkah dengan operation dan izin aktual.

## E2E Scenario B — Student Affairs

1. Pengguna yang berwenang login.
2. Membuat kasus.
3. Membuka detail.
4. Memulai penanganan.
5. Mencatat tindakan.
6. Menyelesaikan kasus.
7. Memeriksa timeline.
8. Memeriksa audit.
9. Memastikan role tidak berwenang ditolak.

## E2E Scenario C — Administration

1. Tata Usaha login.
2. Memilih jenis layanan.
3. Membuat permohonan.
4. Mengunggah dokumen.
5. Memproses permohonan.
6. Mengajukan persetujuan apabila diperlukan.
7. Pimpinan login.
8. Membuka antrean persetujuan.
9. Menyetujui atau menolak.
10. Tata Usaha menyelesaikan layanan yang sah.
11. Pengguna berwenang mengunduh dokumen.
12. Pengguna tidak berwenang ditolak.
13. Laporan diekspor.
14. Audit diperiksa.

Uji jalur persetujuan, penolakan dan tanpa persetujuan hanya berdasarkan kebijakan yang sah.

## E2E Scenario D — Security

- Invalid authentication.
- Expired token.
- Revoked session.
- Unauthorized role.
- Out-of-scope resource.
- Direct ID manipulation.
- Unauthorized private download.
- Sensitive data exposure prevention.
- Rate limit.
- Cache isolation.

## E2E Scenario E — Concurrency

- Dua pengguna mengakses data yang sama.
- Pengguna pertama menyimpan perubahan.
- Pengguna kedua mencoba menyimpan data yang sudah stale.
- Sistem menangani konflik sesuai mekanisme yang disetujui.
- Tidak terjadi lost update.
- History dan audit tetap konsisten.

Bedakan API E2E backend dengan browser E2E frontend.

Jangan mengklaim browser E2E atau integrasi frontend telah selesai ketika frontend belum tersedia.

Integration Agent tetap bertanggung jawab terhadap pengujian end-to-end seluruh aplikasi.

---

# 26. CONTRACT TESTING

Contract testing wajib menjadi quality gate setiap milestone.

Gunakan `contracts/openapi.v1.yaml` aktual sebagai baseline.

Bandingkan kontrak baseline dengan schema yang dihasilkan backend Django Ninja.

Verifikasi:

- Paths.
- HTTP methods.
- Operation IDs.
- Request schema.
- Required fields.
- Property types.
- Enum values.
- Query parameters.
- Path parameters.
- Response schema.
- Response status codes.
- Authentication.
- Content types.
- Multipart upload.
- Binary download.
- ErrorEnvelope.

Uji request valid dan invalid.

Pastikan implementasi tidak menambahkan atau menghapus field secara tidak sah.

Periksa OpenAPI 3.1 semantics, termasuk nullable types.

Jangan hanya menguji bahwa endpoint mengembalikan HTTP 200.

Verifikasi response body dan business behavior.

Jika generated OpenAPI framework memiliki perbedaan representasi yang semantik setara, dokumentasikan metode normalisasi dan buktikan kesetaraannya.

Jangan mengubah baseline kontrak hanya agar tes lulus.

Jika ada kebutuhan perubahan kontrak, gunakan jalur Coordinator.

---

# 27. SECURITY TESTING

Gunakan skill `security-audit`.

Lakukan threat modeling yang relevan dengan aplikasi sekolah.

Prioritaskan risiko keamanan yang berasal dari kebutuhan dan arsitektur aktual.

Periksa:

- Broken access control.
- IDOR/BOLA.
- Authentication bypass.
- Privilege escalation.
- Mass assignment.
- JWT tampering.
- Session revocation.
- Refresh token reuse.
- Brute-force protection.
- SQL injection.
- Input validation.
- XSS-related output risks.
- CORS misconfiguration.
- CSRF sesuai authentication topology.
- Security headers.
- File upload abuse.
- Path traversal.
- Sensitive data leakage.
- Insecure caching.
- Secrets exposure.
- Log exposure.
- Spreadsheet formula injection.
- Dependency vulnerabilities.

Lakukan dependency audit menggunakan tool yang sesuai dan tersedia.

Jangan mengeksekusi pengujian terhadap sistem produksi atau layanan pihak ketiga.

Gunakan environment development/test terisolasi.

Untuk setiap finding, catat:

- Finding ID.
- Severity.
- Affected module.
- Root cause.
- Evidence.
- Fix.
- Regression test.
- Final status.

Temuan kritis dan tinggi yang belum terselesaikan wajib mencegah klaim backend siap penuh.

---

# 28. PERFORMANCE TESTING & OPTIMIZATION

Gunakan skill `python-performance-optimization`.

Jangan mengoptimalkan berdasarkan tebakan.

Lakukan:

`MEASURE → PROFILE → OPTIMIZE → MEASURE AGAIN`

## 28.1 Database performance

Periksa:

- N+1 queries.
- Excessive query count.
- Missing indexes.
- Unnecessary joins.
- Full table scan yang tidak diperlukan.
- Inefficient pagination.
- Large serialization payload.
- Repeated database reads.
- Transaction duration.

Gunakan:

- `select_related`.
- `prefetch_related`.
- Database indexes yang relevan.
- Query aggregation.
- Bulk operations yang aman.
- Server-side pagination.
- Efficient selectors.

Jangan menambahkan index pada seluruh kolom tanpa analisis.

## 28.2 Cache performance

Uji:

- Cold cache.
- Warm cache.
- Cache hit.
- Cache miss.
- Invalidation.
- Cross-user isolation.
- Redis failure.
- Stale data protection.

Ukur manfaat cache terhadap response time dan query count.

## 28.3 API performance

Prioritaskan:

- Login.
- List students.
- List accounts.
- Attendance roster.
- Bulk attendance.
- Dashboard.
- Attendance report.
- Administration report.
- Document upload/download.

Catat:

- Dataset size.
- Hardware.
- Database engine.
- Redis state.
- Worker count.
- Concurrency level.
- Request count.
- Throughput.
- p50 latency.
- p95 latency.
- p99 latency.
- Error rate.
- Query count.
- Memory/CPU jika dapat diukur secara akurat.

## 28.4 Workload

Gunakan synthetic data yang realistis.

Gunakan ukuran dataset dari dokumen atau baseline penelitian jika tersedia.

Jika belum tersedia, tetapkan workload benchmark yang jelas sebagai asumsi teknis, bukan ukuran populasi sekolah yang diklaim nyata.

Uji:

- Small dataset.
- Representative dataset.
- Larger stress dataset sesuai kemampuan perangkat.

Jangan mengarang kapasitas sistem produksi.

## 28.5 Performance acceptance

Ikuti target performa resmi TRD dan execution plan.

Jika target belum ditentukan, hasil benchmark menjadi baseline dan usulan target, bukan SLA resmi.

Response time lambat yang melewati ambang investigasi pada TRD harus dianalisis.

Jangan menyatakan performance PASS tanpa metrik dan kondisi pengujian.

Uji PostgreSQL dan Redis nyata untuk jalur performa yang relevan.

---

# 29. REGRESSION TESTING

Setiap milestone harus mempertahankan seluruh fitur yang telah lulus sebelumnya.

Sebelum melakukan perubahan pada modul yang sudah ada:

1. Jalankan baseline tests.
2. Identifikasi blast radius menggunakan CodeGraph.
3. Tambahkan regression test.
4. Lakukan perubahan.
5. Jalankan targeted tests.
6. Jalankan cross-module tests.
7. Jalankan seluruh suite yang relevan.

Jangan membuat fitur baru dengan merusak fungsi lama.

Jika terjadi regression, perbaiki sebelum melanjutkan milestone yang bergantung padanya.

Simpan hasil baseline dan hasil setelah perubahan pada laporan kumulatif.

Jangan menghitung test yang sama pada beberapa invocation sebagai test unik tanpa penjelasan.

---

# 30. FAILED TEST — ROOT CAUSE ANALYSIS & AUTOMATIC REPAIR

Jika terdapat test gagal, jangan berhenti hanya dengan melaporkan kegagalan.

Lakukan investigasi:

1. Baca failure output.
2. Baca stack trace.
3. Identifikasi test case.
4. Reproduksi secara terisolasi.
5. Periksa kontrak.
6. Periksa business rules.
7. Periksa expected result.
8. Periksa test fixture.
9. Periksa environment.
10. Periksa source code.
11. Gunakan CodeGraph untuk impact analysis.
12. Identifikasi root cause.

Klasifikasikan kegagalan sebagai:

- IMPLEMENTATION_BUG.
- BUSINESS_LOGIC_BUG.
- TEST_CODE_BUG.
- FIXTURE_BUG.
- CONTRACT_MISMATCH.
- DATABASE_ISSUE.
- CONCURRENCY_ISSUE.
- ENVIRONMENT_ISSUE.
- FLAKY_TEST.
- SHARED_CONTRACT_BLOCKER.

## Repair policy

Jika kesalahan terdapat pada implementasi:

- Perbaiki kode.
- Pertahankan business rules.
- Tambahkan regression test.

Jika kesalahan terdapat pada test:

- Verifikasi expected behavior terhadap sumber resmi.
- Perbaiki test yang salah.
- Jelaskan alasan perubahan assertion.
- Pertahankan kemampuan test mendeteksi bug nyata.

Jika kesalahan terdapat pada fixture:

- Perbaiki fixture.
- Jangan melemahkan validasi aplikasi.

Jika masalah berasal dari environment:

- Perbaiki konfigurasi yang berada dalam scope.
- Jangan menyamarkan integration failure dengan mock.

Jika masalah berasal dari kontrak:

- Catat gap.
- Teruskan kepada Coordinator.
- Jangan mengubah kontrak secara sepihak.

## Strict prohibitions

DILARANG:

- Menghapus test hanya agar suite lulus.
- Mengubah expected value tanpa dasar.
- Mengurangi assertion penting.
- Menggunakan `assert True` sebagai pengganti test.
- Menonaktifkan validation.
- Menonaktifkan authorization.
- Menonaktifkan security middleware.
- Mengganti operasi nyata dengan data hardcoded.
- Memberikan skip atau xfail untuk menyembunyikan bug.
- Menangkap seluruh exception lalu mengembalikan sukses.
- Mengabaikan hasil test gagal.
- Mengarang hasil PASS.

Setelah perbaikan:

- Jalankan ulang test gagal.
- Jalankan test terkait.
- Jalankan regression suite.
- Verifikasi dampak perubahan.
- Catat perubahan pada changelog.

Jika masalah tidak dapat diselesaikan tanpa keputusan eksternal, tandai BLOCKED dengan bukti yang jelas.

---

# 31. COVERAGE REQUIREMENTS

Gunakan coverage measurement untuk membantu menemukan area yang belum diuji.

Laporkan:

- Overall line coverage.
- Branch coverage.
- Coverage per module.
- Coverage pada business services.
- Coverage pada permission rules.
- Coverage pada validation.
- Coverage pada state transitions.

Ikuti target coverage resmi execution plan jika tersedia.

Jika belum ada target, gunakan target internal yang rasional dan disepakati berdasarkan risiko.

Jangan mengejar 100% coverage secara artifisial.

Mandatory scenarios tetap wajib diuji meskipun coverage tinggi.

Prioritaskan cakupan menyeluruh untuk:

- Authentication.
- Authorization.
- RBAC.
- Object scope.
- Data privacy.
- Business state machines.
- Financial atau administratif data integrity yang relevan.
- Concurrency.
- Private document access.
- Transaction rollback.
- Security failure handling.

Coverage tinggi bukan bukti otomatis bahwa seluruh sistem benar.

---

# 32. CODE QUALITY & ANTI-AI SLOP

Gunakan:

- `antislop-code`
- `improve-codebase-architecture`
- `ponytail`
- `ponytail-review`
- `ponytail-debt`

Backend harus terlihat seperti codebase profesional yang dapat dipelihara oleh developer manusia.

DILARANG:

- Overengineering.
- Unnecessary abstractions.
- Generic framework buatan sendiri.
- Duplicate helper functions tanpa alasan.
- Dead code.
- Unused imports.
- Hardcoded credentials.
- Hardcoded response operasional.
- Unnecessary wrapper layers.
- Giant functions dengan tanggung jawab bercampur.
- Circular dependencies.
- Broad exception swallowing.
- Comment yang hanya mengulang kode.
- TODO palsu sebagai pengganti implementasi.
- Unbounded query.
- Unbounded cache.
- Inconsistent naming.

Gunakan:

- Clear naming.
- Type hints.
- Explicit validation.
- Consistent module structure.
- Focused functions.
- Meaningful error codes.
- Structured logs.
- Minimal useful comments.
- Reusable business services.

Jangan menyederhanakan kode dengan menghapus keamanan atau pengujian.

---

# 33. USER-FACING ERROR AND MESSAGE POLICY

Gunakan Bahasa Indonesia yang jelas dan mudah dimengerti untuk error message yang akan ditampilkan kepada pengguna.

Contoh:

- Kredensial tidak valid.
- Anda tidak memiliki akses ke kelas ini.
- Data telah diperbarui oleh pengguna lain.
- Berkas melebihi batas ukuran.
- Data siswa tidak ditemukan.
- Permohonan tidak dapat diproses pada status saat ini.

Jangan mengekspos stack trace atau detail infrastruktur kepada pengguna.

Jangan menggunakan istilah berikut sebagai label atau pesan operasional:

- Mock.
- Dummy.
- Simulasi.
- Payload.
- Database query.
- Redis failure.
- Internal exception.

Istilah teknis tetap boleh digunakan dalam kode, test, developer documentation, dan structured logs yang aman.

Jangan menyamarkan data sintetis atau pengujian sebagai data operasional nyata.

---

# 34. DATA PROTECTION

Data sekolah merupakan informasi sensitif.

Gunakan synthetic test fixtures.

Jangan mengimpor data siswa atau pegawai nyata tanpa otorisasi.

Pastikan:

- Data minimization.
- Object-level authorization.
- Private storage.
- Secure logging.
- Safe exports.
- Secret management.
- Data retention sesuai keputusan proyek.
- Historical records protection.

Jangan memasukkan ke Git:

- `.env` berisi rahasia.
- Database development.
- Private files.
- Virtual environment.
- Credentials.
- Token.
- Personal data.
- Generated cache files.

Gunakan `.env.example` tanpa secret.

Pastikan test credentials hanya berlaku pada environment pengujian.

---

# 35. MULTI-AGENT PARALLEL DEVELOPMENT

Backend Track harus dapat berjalan tanpa frontend.

Jangan menunggu implementasi React.

Frontend Agent boleh mengembangkan UI berdasarkan kontrak yang sama.

Pertahankan:

- Shared contract revision.
- File ownership.
- Independent dependencies.
- Independent environment.
- Git worktree isolation.
- Separate test databases.
- Redis namespace isolation.
- Private media isolation.
- Port configuration.

Jangan menggunakan database test milik agent lain.

Jangan menghentikan service agent lain.

Jangan mengubah frontend agar menyesuaikan bug backend.

Jika terdapat integrasi yang membutuhkan perubahan bersama, catat dependency untuk Coordinator.

Setelah suatu modul selesai, berikan handoff pada BACKEND_STATUS.md:

- Milestone.
- Module.
- Contract revision.
- Operations implemented.
- Test results.
- Known limitations.
- Integration readiness.
- Required dependencies.

Integration Agent dapat mulai menguji modul yang memenuhi prerequisite tanpa menunggu seluruh backend selesai.

---

# 36. MANDATORY QUALITY GATES

Sebelum milestone dinyatakan selesai, periksa:

## G1 — Scope Isolation

- Git diff sesuai writable scope.
- Tidak ada perubahan frontend.
- Tidak ada perubahan kontrak tanpa persetujuan.
- Tidak ada perubahan pengguna yang terhapus.

## G2 — Architecture

- Struktur sesuai TRD.
- Domain responsibilities jelas.
- Tidak ada circular dependency baru.
- Tidak ada overengineering.

## G3 — Contract

- Semua operation milestone dipetakan.
- Request/response sesuai kontrak.
- Error handling sesuai kontrak.
- Tidak ada endpoint bisnis fiktif.

## G4 — Functional

- Business workflow berjalan.
- Validasi benar.
- Transaksi konsisten.
- State machine benar.

## G5 — Security

- Authentication benar.
- Authorization benar.
- Object scope benar.
- Tidak ada sensitive data leakage.
- Security-critical Redis behavior teruji.

## G6 — Testing

- Unit tests.
- Layer tests.
- Module tests.
- Integration tests.
- Contract tests.
- Regression tests.
- Security tests.
- E2E tests yang relevan.

## G7 — Database

- Migrations valid.
- Constraints valid.
- SQLite support.
- PostgreSQL support.
- Concurrency tests sesuai kebutuhan.

## G8 — Performance

- Query count diperiksa.
- N+1 diperiksa.
- Cache behavior diperiksa.
- Benchmark relevan tersedia.
- Temuan performa diperbaiki atau dijelaskan.

## G9 — Documentation

- Implementation report diperbarui.
- Changelog diperbarui.
- BACKEND_STATUS.md diperbarui.
- Blocker tercatat.
- Handoff tersedia.

Lanjutkan milestone berikutnya hanya apabila prerequisite telah terpenuhi.

Jika terdapat blocker eksternal, gunakan status bersyarat dan lanjutkan task independen.

---

# 37. MANDATORY FINAL COMMAND VERIFICATION

Gunakan command yang sesuai toolchain aktual.

Contoh pemeriksaan minimum:

```powershell
python --version
python -m django --version
python -m pip check

python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations

python -m ruff check .
python -m ruff format --check .

python -m pytest
```

Jalankan command dari direktori dan interpreter yang benar.

Gunakan coverage command, contract validation, PostgreSQL test suite, Redis integration suite, security scanner dan performance benchmark berdasarkan dependency yang telah dipilih.

Jangan sekadar menuliskan command pada laporan tanpa menjalankannya.

Catat:

- Command aktual.
- Exit code.
- Jumlah tests collected.
- Jumlah PASS.
- Jumlah FAIL.
- Jumlah SKIP.
- Jumlah XFAIL jika ada.
- Execution duration.
- Environment.
- Contract revision.
- Alasan test yang tidak dijalankan.

Jika command gagal:

- Identifikasi penyebab.
- Perbaiki.
- Jalankan ulang.
- Catat hasil final.

Jangan mengklaim seluruh pemeriksaan PASS apabila masih terdapat command gagal yang belum diselesaikan.

---

# 38. DOCUMENTATION POLICY — ONLY TWO MASTER OUTPUT FILES

Jangan membuat banyak file Markdown laporan.

Gunakan hanya dua dokumen hasil pekerjaan backend:

1. `backend/BACKEND_IMPLEMENTATION_REPORT.md`
2. `backend/BACKEND_CHANGELOG.md`

Jika execution plan sudah menetapkan lokasi lain untuk kedua file tersebut, gunakan lokasi resmi tanpa membuat duplikasi.

Seluruh milestone wajib memperbarui kedua dokumen yang sama.

`backend/AGENTS.md` tetap dipertahankan.

`coordination/BACKEND_STATUS.md` tetap diperbarui sebagai coordination state, bukan dokumen laporan tambahan.

Test source files, migrations, dependency lock files, configuration files, dan machine-readable test artifacts tetap diperbolehkan sesuai kebutuhan implementasi.

Batas dua file hanya berlaku untuk dokumentasi laporan hasil pekerjaan, bukan jumlah file kode atau test.

## 38.1 BACKEND_IMPLEMENTATION_REPORT.md

Gunakan struktur:

### 1. Document Metadata

- Project.
- Backend revision.
- Contract revision.
- Contract checksum.
- DBML revision.
- Git branch.
- Workspace.
- Runtime version.
- Last updated.
- Current readiness.

### 2. Executive Summary

Ringkasan hasil backend dan status aktual.

### 3. Milestone Completion Matrix

Seluruh BE-M1 sampai BE-M8.

Untuk setiap milestone:

- Task ID.
- Status.
- Deliverables.
- Quality gates.
- Tests.
- Blockers.

### 4. Architecture Implementation

- Module structure.
- Layer responsibilities.
- Dependency relationships.
- Architecture decisions.
- CodeGraph findings.

### 5. Technology and Environment

- Python.
- Django.
- Django Ninja.
- Granian.
- SQLite.
- PostgreSQL.
- Redis.
- Dependency versions.

### 6. Database Implementation

- Models.
- Tables.
- Migrations.
- Constraints.
- Indexes.
- Transaction strategy.
- SQLite/PostgreSQL compatibility.

### 7. API Implementation Matrix

Untuk setiap operation:

- Operation ID.
- Method.
- Path.
- Module.
- Request schema.
- Response schema.
- Authorization.
- Implementation status.
- Test evidence.

### 8. RBAC and Security Implementation

- Roles.
- Object scopes.
- Authorization.
- Authentication.
- Token security.
- Rate limiting.
- Private storage.
- Pending approvals.

### 9. Functional Verification

Workflow bisnis per modul.

### 10. Testing Results

Pisahkan:

- Unit tests.
- Layer tests.
- Module tests.
- Integration tests.
- N2N tests.
- Contract tests.
- API E2E tests.
- Security tests.
- Performance tests.
- Regression tests.

Cantumkan environment dan jumlah aktual.

### 11. Coverage Results

- Overall.
- Per module.
- Critical business rules.
- Uncovered risks.

### 12. Security Audit

- Findings.
- Severity.
- Evidence.
- Fixes.
- Remaining risks.

### 13. Performance Benchmark

- Workload.
- Environment.
- Before metrics.
- After metrics.
- Optimization.
- Query counts.
- Latency.
- Cache effectiveness.

### 14. Concurrency and Data Integrity

- Attendance.
- Enrollment.
- Assignment.
- Case transitions.
- Service transitions.
- Token rotation.

### 15. CodeGraph & Trail-Code Utilization

- Tool usage.
- Dependency analysis.
- Important learnings.
- Impact verification.

### 16. AI Agent Skill Utilization

Skill yang benar-benar digunakan dan kontribusinya.

### 17. Frontend Integration Handoff

- API base configuration.
- Contract revision.
- Authentication behavior.
- Available operations.
- Error semantics.
- File upload/download.
- Pagination.
- Integration dependencies.

### 18. Known Limitations & Blockers

- Technical blockers.
- Pending school policies.
- Shared contract gaps.
- Unverified infrastructure.
- Remaining work.

### 19. Final Quality Gate

Hasil seluruh G1 sampai G9.

### 20. Final Readiness Decision

Gunakan status berdasarkan bukti aktual.

## 38.2 BACKEND_CHANGELOG.md

Gunakan format kronologis per milestone.

Contoh:

```text
## BE-M1 — Foundation & Infrastructure

### Added
### Changed
### Fixed
### Security
### Performance
### Database & Migrations
### Tests
### Contract Alignment
### Files Changed
### Known Issues
```

Untuk setiap perubahan penting:

- Task ID.
- File path.
- Deskripsi perubahan.
- Alasan.
- Affected module.
- Contract revision.
- Test result.
- Regression impact.

Untuk setiap bug:

- Bug ID.
- Root cause.
- Affected files.
- Fix.
- Regression test.
- Final status.

Jangan menyalin seluruh source code ke changelog.

Jangan menduplikasi seluruh implementation report.

Jangan membuat file baru seperti:

- M1_IMPLEMENTATION_REPORT.md.
- M2_IMPLEMENTATION_REPORT.md.
- SECURITY_REPORT.md.
- PERFORMANCE_REPORT.md.
- TEST_REPORT.md.
- FINAL_AUDIT.md.

Masukkan seluruh hasil tersebut ke bagian yang sesuai dalam dua dokumen master.

Gunakan relative paths.

Pertahankan histori milestone.

---

# 39. FINAL ACCEPTANCE CRITERIA

Sebelum menyatakan backend selesai:

## Functional completeness

- Seluruh milestone BE-M1 sampai BE-M8 telah dieksekusi.
- Seluruh operasi yang disetujui telah diimplementasikan.
- Seluruh modul bisnis bekerja.
- Tidak ada fake success.
- Tidak ada hardcoded operational data.
- Tidak ada placeholder pada fitur yang diklaim selesai.

## Contract completeness

- OpenAPI baseline valid.
- Generated schema diverifikasi.
- Required operations tersedia.
- Request/response sesuai.
- Error responses sesuai.
- Authorization sesuai.

## Database completeness

- Models sesuai DBML yang disetujui.
- Migrations valid.
- SQLite development berjalan.
- PostgreSQL integration terverifikasi.
- Database constraints teruji.
- Transaction integrity teruji.
- Concurrency requirements teruji.

## Security completeness

- RBAC teruji.
- Object scope teruji.
- Authentication teruji.
- Session revocation teruji.
- Rate limiting teruji.
- Redis security integration teruji.
- Private document access teruji.
- Tidak ada critical/high security finding yang belum diselesaikan pada scope backend.

## Testing completeness

- Unit test.
- Layer test.
- Module test.
- Integration test.
- N2N test.
- Contract test.
- API E2E test.
- Security test.
- Performance test.
- Regression test.

Seluruh mandatory test yang relevan telah dijalankan.

## Maintainability

- Ruff checks lulus.
- Dependency configuration reproducible.
- Struktur sesuai execution plan.
- Tidak ada unnecessary abstraction.
- CodeGraph synchronized.
- Important learnings tercatat.

## Handoff

- BACKEND_IMPLEMENTATION_REPORT.md tersedia.
- BACKEND_CHANGELOG.md tersedia.
- BACKEND_STATUS.md diperbarui.
- Integration readiness per module tersedia.
- Known blockers tercatat.

Jangan menyatakan seluruh backend siap apabila masih terdapat fitur wajib yang belum diimplementasikan atau mandatory tests belum dijalankan.

---

# 40. FINAL READINESS DECISION

Gunakan salah satu status:

`READY — COMPLETE_CONTRACT_ALIGNED_BACKEND_READY_FOR_INTEGRATION`

Hanya jika seluruh fitur wajib dalam baseline yang disetujui, quality gates dan pengujian relevan telah terpenuhi.

Atau:

`CONDITIONALLY_READY — BACKEND_IMPLEMENTED_WITH_OPEN_ITEMS`

Jika backend utama telah diimplementasikan tetapi masih terdapat dependency eksternal, pending business policy, atau verification gate yang belum terpenuhi.

Atau:

`BLOCKED — CRITICAL_BACKEND_OR_CONTRACT_ISSUES`

Jika terdapat masalah kritis yang mencegah backend berfungsi atau terintegrasi secara aman.

Status backend READY tidak berarti:

- Frontend telah selesai.
- Browser E2E seluruh aplikasi telah lulus.
- Sistem telah disetujui sekolah.
- UAT atau SUS telah dilaksanakan.
- Efisiensi administrasi telah terbukti secara empiris.
- Sistem telah siap produksi tanpa deployment review.

---

# 41. FINAL EXECUTION INSTRUCTION

Mulai sekarang.

Verifikasi workspace, virtual environment Django, kontrak, coordination status, skill, CodeGraph dan Trail-Code.

Gunakan SQLite + WAL sebagai database development lokal.

Pertahankan PostgreSQL untuk integration testing, staging dan production.

Pertahankan Redis sebagai infrastruktur wajib.

Kerjakan BE-M1 sampai BE-M8 sesuai execution plan.

Gunakan pendekatan test-driven development pada business logic dan security-critical behavior.

Implementasikan backend nyata.

Jalankan pengujian penting pada setiap layer dan setiap modul.

Jika test gagal:

- Investigasi.
- Identifikasi root cause.
- Perbaiki kode logic atau test code sesuai sumber kebenaran.
- Jalankan ulang.
- Lakukan regression verification.

Jangan menunggu frontend.

Jangan melanggar file ownership.

Jangan mengubah shared contracts tanpa persetujuan.

Jangan berhenti di tengah milestone hanya untuk memberikan laporan sementara apabila masih terdapat pekerjaan yang dapat diselesaikan.

Lanjutkan seluruh pekerjaan independen yang aman hingga milestone akhir.

Catat seluruh perubahan dan hasil pemeriksaan hanya pada:

- `backend/BACKEND_IMPLEMENTATION_REPORT.md`
- `backend/BACKEND_CHANGELOG.md`

Perbarui coordination/BACKEND_STATUS.md secara berkala.

Tujuan akhir adalah backend yang lengkap, aman, teruji, performant, contract-aligned, solo developer friendly, dan siap diserahkan kepada Frontend Agent serta Integration Agent.

Kerjakan sampai selesai berdasarkan bukti implementasi dan pengujian aktual, bukan berdasarkan jumlah file yang dibuat atau klaim keberhasilan semata.
