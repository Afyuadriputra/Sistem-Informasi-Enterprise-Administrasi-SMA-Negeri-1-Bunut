
# MASTER TASK — CONTRACT-FIRST PARALLEL DEVELOPMENT & MULTI-AGENT PROJECT PREPARATION

## 1. Peran Anda

Bertindak sebagai Senior Software Architect, Technical Lead, System Analyst, AI Agent Workflow Architect, dan Quality Assurance Engineer.

Anda bertanggung jawab mempersiapkan proyek **Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut** agar dapat dikembangkan oleh AI agent secara independen, bertahap, paralel, terisolasi, dan konsisten dengan seluruh dokumentasi proyek.

Gunakan pendekatan:

- Contract-First Development.
- Parallel Frontend and Backend Development.
- Multi-Agent Workflow.
- Modular Monolith Architecture.
- Atomic Design.
- Test-Driven Development.
- Documentation-Driven Development.
- Git Worktree Isolation.
- Explicit File Ownership.
- Milestone-Based Quality Gates.
- Solo Developer Friendly Architecture.

## 2. Lokasi dan kondisi proyek

Current project root:

`D:\Kuliah\joki\radit\PROJEK istri bg givo`

Kondisi saat ini:

- Belum memasuki tahap coding aplikasi.
- Belum terdapat implementasi frontend.
- Belum terdapat implementasi backend.
- Terdapat tujuh dokumen utama pada folder `docs/`.
- Terdapat berbagai AI Agent Skills pada `.agents/skills/`.
- Terdapat `skills-lock.json`.

Lakukan pemeriksaan kondisi aktual direktori sebelum melakukan perubahan.

Jangan mengasumsikan Git, dependency, runtime, database, maupun layanan lainnya sudah tersedia sebelum diperiksa.

## 3. Tujuan utama

Persiapkan sistem kerja yang memungkinkan seluruh skenario berikut:

### Scenario A — Backend First

Backend Agent dapat mengerjakan backend terlebih dahulu tanpa membutuhkan implementasi frontend.

### Scenario B — Frontend First

Frontend Agent dapat mengerjakan frontend terlebih dahulu berdasarkan UID, PRD, AFD, dan kontrak OpenAPI yang telah disepakati, tanpa menunggu backend selesai.

### Scenario C — Parallel Development

Backend Agent dan Frontend Agent dapat mengerjakan modul yang sama ataupun berbeda secara bersamaan tanpa mengubah file milik agent lain.

### Scenario D — Interrupted Development

Pekerjaan dapat dihentikan kapan saja dan dilanjutkan pada sesi AI agent berikutnya berdasarkan execution plan, task ID, progress report, dan status terakhir.

### Scenario E — Incremental Integration

Frontend dan backend dapat diintegrasikan per modul tanpa harus menunggu seluruh aplikasi selesai.

Seluruh skenario harus didukung oleh dokumentasi, pembagian tanggung jawab, kontrak API, pengelolaan dependensi, dan quality gates yang jelas.

## 4. Batasan tahap pekerjaan

Current phase:

`M0 — DOCUMENTATION ALIGNMENT & PARALLEL DEVELOPMENT PREPARATION`

PENTING: Tahap ini merupakan persiapan proyek, bukan implementasi aplikasi.

DILARANG:

- Membuat implementasi Django.
- Membuat implementasi React.
- Membuat business logic.
- Membuat model ORM.
- Membuat migration database.
- Mengimplementasikan endpoint API.
- Membuat halaman frontend.
- Menginstal dependency aplikasi.
- Menjalankan server aplikasi.
- Membuat database atau Redis instance.
- Menghapus atau mengganti AI Agent Skills yang tersedia.
- Mengubah tech stack tanpa persetujuan.
- Mengarang hasil pengujian.
- Menganggap keputusan sekolah yang belum tervalidasi sebagai fakta.
- Melakukan commit, push, reset, atau perubahan Git destruktif tanpa persetujuan.

Diperbolehkan membuat dokumentasi, kontrak API dalam YAML, DBML, struktur folder minimal, template koordinasi, dan aturan AI agent.

Jangan melanjutkan ke coding aplikasi sebelum M0 mendapatkan sign-off.

## 5. Baca seluruh sumber kebenaran proyek

Wajib membaca secara lengkap:

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/DBD.md`
- `docs/BSD.md`
- `docs/AFD.md`
- `docs/IPD.md`
- `docs/UID.md`

Pahami:

- Tujuan penelitian DSRM dan TOGAF.
- Ruang lingkup sistem.
- Enam role pengguna.
- FR-01 sampai FR-10.
- NFR-01 sampai NFR-06.
- Struktur modular monolith Django.
- Struktur frontend Atomic Design.
- Skema database dan relasi.
- Endpoint API.
- Workflow kehadiran dan kesiswaan.
- Workflow layanan tata usaha.
- Autentikasi dan otorisasi.
- Audit trail.
- Redis caching dan rate limiting.
- Pengujian dan evaluasi.
- Seluruh 25 hukum dan prinsip UX.
- Golden ratio.
- Standar anti-AI slop.
- Design system.
- Screen S01 sampai S18.

Jangan mengabaikan satu dokumen pun.

Tetapkan hierarki kepemilikan keputusan:

- PRD: kebutuhan, ruang lingkup dan kewenangan bisnis.
- AFD: workflow dan transisi proses.
- DBD: desain data dan integritas.
- BSD: spesifikasi backend.
- TRD: arsitektur, teknologi dan standar teknis.
- UID: visual, interaksi dan pengalaman pengguna.
- IPD: roadmap dan tahapan penelitian.
- OpenAPI: kontrak komunikasi frontend-backend yang telah disepakati.

Jika terdapat konflik, jangan memilih salah satu secara diam-diam. Catat konflik, usulkan resolusi, identifikasi dampaknya, dan sinkronkan setelah keputusan disetujui.

## 6. Audit dan sinkronisasi dokumentasi

Lakukan cross-document consistency audit terhadap ketujuh dokumen.

Periksa minimal:

1. Ketidaksesuaian izin antara PRD, AFD, BSD, dan UID.
2. Hak wali kelas memulai penanganan kasus.
3. Hak TU mengelola data siswa.
4. Hak administrator terhadap kehadiran dan data sensitif.
5. Hak pimpinan melihat antrean persetujuan dan audit.
6. Endpoint yang dibutuhkan screen S01-S18.
7. Endpoint manajemen akun, role, dan penugasan.
8. Endpoint roster kehadiran berdasarkan kelas dan tanggal.
9. Kontrak daftar arsip dokumen.
10. Pencatatan tindakan kasus tanpa perubahan status jika dibutuhkan.
11. Alur layanan yang membutuhkan atau tidak membutuhkan persetujuan.
12. Status DITOLAK tidak otomatis berubah menjadi SELESAI.
13. Kesesuaian field version dengan mekanisme optimistic locking.
14. Konkurensi penyimpanan dan koreksi batch kehadiran.
15. Keamanan cache key berdasarkan cakupan akses efektif.
16. JWT access token, refresh token, rotation, blacklist, CSRF dan logout.
17. Perilaku aplikasi ketika Redis tidak tersedia.
18. Validasi, penyimpanan, pengunduhan dan lifecycle dokumen privat.
19. Audit history pada operasi bulk.
20. Protokol penelitian, pengujian dan pengukuran konsistensi data.
21. Sinkronisasi roadmap frontend dan backend.
22. Referensi internal, nomor bagian, metadata, dan versi dokumen.

Buat:

`docs/DOCUMENTATION_ALIGNMENT_REPORT.md`

Klasifikasikan temuan:

- P0 — Critical / Blocking.
- P1 — Important.
- P2 — Improvement.

Buat juga:

`docs/DECISION_LOG.md`

Setiap keputusan mempunyai:

- Decision ID.
- Context.
- Source document.
- Problem.
- Proposed decision.
- Alternative.
- Impact.
- Status: PROPOSED / APPROVED / REJECTED / DEFERRED.
- Dokumen dan kontrak yang terdampak.

Pisahkan keputusan teknis yang sudah tertulis dalam dokumen dari keputusan bisnis yang masih menunggu validasi sekolah.

Jangan mengklaim seluruh temuan terselesaikan apabila masih ada keputusan terbuka.

## 7. Multi-Agent Workflow Architecture

Definisikan tiga jenis AI agent.

### 7.1 Backend Agent

Tanggung jawab:

- Django.
- Django Ninja.
- Database dan ORM.
- Database migrations.
- Authentication.
- RBAC dan object-level authorization.
- Business logic.
- API implementation.
- Redis caching dan rate limiting.
- Audit trail.
- Private document storage.
- Backend testing.
- Performance optimization.

Primary writable scope:

`backend/**`

Backend Agent boleh membaca frontend, kontrak dan dokumentasi, tetapi tidak boleh mengubah file frontend.

### 7.2 Frontend Agent

Tanggung jawab:

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- shadcn/ui.
- Atomic Design.
- Design system.
- UI/UX.
- Responsive layout.
- Accessibility.
- API client.
- Generated API types.
- TanStack Query.
- Zustand.
- Frontend testing.
- Browser verification.

Primary writable scope:

`frontend/**`

Frontend Agent boleh membaca backend, kontrak dan dokumentasi, tetapi tidak boleh mengubah file backend.

### 7.3 Coordinator / Integration Agent

Tanggung jawab:

- Cross-document alignment.
- Contract management.
- Task assignment.
- Decision management.
- Dependency management.
- Integration testing.
- End-to-end testing.
- Quality gate review.
- Conflict resolution.
- Git integration workflow.
- Release readiness.

Coordinator mengelola shared contracts dan konfigurasi lintas proyek.

Coordinator tidak boleh secara otomatis mengambil alih implementasi frontend/backend. Jika diperlukan perubahan kode, buat task khusus dan delegasikan kepada pemilik scope.

## 8. File Ownership dan Scope Isolation

Buat matriks kepemilikan file secara eksplisit.

Tetapkan minimal:

- Backend Agent memiliki hak edit pada `backend/**` dan `coordination/BACKEND_STATUS.md`.
- Frontend Agent memiliki hak edit pada `frontend/**` dan `coordination/FRONTEND_STATUS.md`.
- Integration Agent memiliki hak edit pada `contracts/**`, root `AGENTS.md`, dan dokumen koordinasi bersama.
- Integration Agent mengelola `coordination/PROJECT_STATUS.md` dan `coordination/INTEGRATION_STATUS.md`.
- Perubahan baseline dokumentasi bersama harus melalui review Coordinator.
- Setiap task memiliki allowed paths yang lebih spesifik daripada scope agent.
- Perubahan file instruksi agent harus direview Coordinator.

Jika suatu task membutuhkan perubahan di luar allowed paths:

1. Hentikan perubahan tersebut.
2. Dokumentasikan kebutuhan.
3. Buat change request.
4. Serahkan kepada agent yang berwenang.

Dilarang memperbaiki kode agent lain hanya karena menemukan masalah integrasi.

Rencanakan automated scope checking berdasarkan Git diff pada tahap implementasi. Dokumentasikan mekanismenya sekarang tanpa mengimplementasikan CI aplikasi pada M0.

## 9. Contract-First API Design

Buat:

`contracts/README.md`

`contracts/openapi.v1.yaml`

OpenAPI harus mencakup kontrak yang diperlukan seluruh modul:

- Accounts.
- Master Data.
- Attendance.
- Student Affairs.
- Administration.
- Reports.
- Audit.

Setiap kontrak endpoint harus mendefinisikan:

- Operation ID.
- HTTP method.
- Path.
- Authentication.
- Authorization reference.
- Request schema.
- Response schema.
- Required dan optional fields.
- Enum.
- Validation constraints.
- Pagination.
- Filtering.
- Sorting.
- Error response.
- HTTP status code.
- Request ID.
- File upload/download schema jika relevan.
- Contoh request dan response yang sintetis.

Kontrak harus diturunkan dari PRD, BSD, DBD, AFD dan UID.

Jangan menambahkan fitur bisnis baru tanpa landasan dokumentasi.

Untuk kebutuhan yang belum disepakati, tandai sebagai DRAFT atau BLOCKED. Jangan memalsukan kontrak final hanya untuk melengkapi YAML.

Tetapkan lifecycle kontrak per modul:

- DRAFT.
- IN_REVIEW.
- APPROVED.
- FROZEN.
- IMPLEMENTED.
- VERIFIED.

Hanya kontrak APPROVED atau FROZEN yang boleh menjadi dasar implementasi frontend dan backend.

Gunakan approved design-first OpenAPI sebagai baseline bersama. Pada tahap implementasi, skema OpenAPI aktual yang dihasilkan Django Ninja wajib dibandingkan dengan baseline tersebut.

Perubahan kontrak harus menggunakan mekanisme:

1. Contract Change Request.
2. Impact Analysis.
3. Approval.
4. Contract Update.
5. Backend Task Update.
6. Frontend Task Update.
7. Contract Compatibility Test.

Dilarang mengubah endpoint, payload, status code, atau enum secara sepihak.

## 10. Database Contract

Buat:

`contracts/database.dbml`

Turunkan desain database dari DBD dan kebutuhan yang sudah disepakati.

Dokumentasikan:

- Table.
- Column.
- Data type.
- Primary key.
- Foreign key.
- Unique constraint.
- Nullable.
- Default.
- Enum.
- Index.
- Relationship.
- Historical data.
- Optimistic locking.
- Audit trail.

Jangan menentukan field bisnis yang belum disetujui sebagai keputusan final.

Django migrations nantinya menjadi sumber skema database aktual. DBML menjadi baseline desain yang harus diverifikasi kesesuaiannya terhadap implementasi.

Backend Agent tidak boleh mengubah desain database lintas modul secara sepihak tanpa review dampak.

## 11. Finalisasi RBAC Matrix

Buat:

`docs/RBAC_MATRIX.md`

Cakup enam role:

1. Administrator.
2. Guru.
3. Wali Kelas.
4. Kesiswaan.
5. Tata Usaha.
6. Pimpinan.

Pemetaan wajib sampai tingkat:

- Resource.
- Action.
- Role.
- Object scope.
- Preconditions.
- Allowed / Denied / Pending Approval.
- Related endpoint.
- Related screen.
- Test scenario.

Bedakan tindakan:

- List.
- Read.
- Create.
- Update.
- Deactivate.
- Assign.
- Record.
- Correct.
- Process.
- Approve.
- Reject.
- Cancel.
- Export.
- Download.
- Audit.

Terapkan deny-by-default.

Hak akses multi-role menggunakan gabungan izin sah sebagaimana direncanakan dalam BSD, dengan validasi cakupan objek yang sesuai.

Role aktif pada frontend hanya konteks tampilan dan bukan bukti otorisasi.

Jangan memberikan Administrator akses otomatis terhadap seluruh data sensitif.

Konflik izin yang belum diputuskan sekolah harus ditandai Pending Approval.

## 12. Backend Execution Plan

Buat:

`docs/execution/BACKEND_EXECUTION_PLAN.md`

Gunakan milestone:

- BE-M1 — Project Foundation.
- BE-M2 — Authentication & RBAC.
- BE-M3 — Master Data.
- BE-M4 — Attendance.
- BE-M5 — Student Affairs.
- BE-M6 — Administration & Private Documents.
- BE-M7 — Dashboard, Reports & Redis.
- BE-M8 — Performance, Security & Hardening.

Untuk setiap milestone, definisikan:

- Tujuan.
- Scope.
- Task ID.
- Dependency.
- Prasyarat kontrak.
- Allowed paths.
- Forbidden paths.
- Referensi dokumen.
- Business rules.
- Database impact.
- API contract.
- Implementation steps.
- Unit tests.
- Integration tests.
- Security tests.
- Performance tests jika relevan.
- Acceptance criteria.
- Definition of Done.
- Handoff report.

Backend harus dapat berjalan dan diuji secara independen tanpa frontend.

Pertahankan teknologi, struktur modular, Redis, audit, database optimization, dan keamanan yang tercantum dalam TRD.

Jangan mengurangi kualitas teknis atas alasan solo developer friendly.

## 13. Frontend Execution Plan

Buat:

`docs/execution/FRONTEND_EXECUTION_PLAN.md`

Gunakan milestone:

- FE-M1 — Project Foundation & Design System.
- FE-M2 — Authentication UI & Application Shell.
- FE-M3 — Master Data UI.
- FE-M4 — Attendance UI.
- FE-M5 — Student Affairs UI.
- FE-M6 — Administration, Approval & Archive UI.
- FE-M7 — Dashboard & Reporting UI.
- FE-M8 — Accessibility, UX & Visual Hardening.

Setiap milestone wajib mempunyai:

- Tujuan.
- Task ID.
- Scope.
- Screen ID.
- User role.
- User journey.
- Allowed paths.
- Forbidden paths.
- Dependency.
- OpenAPI dependency.
- Component inventory.
- Atomic Design mapping.
- Loading state.
- Empty state.
- Error state.
- Success state.
- Responsive behavior.
- Accessibility requirements.
- Unit/component tests.
- Browser testing.
- Visual verification.
- Acceptance criteria.
- Definition of Done.

Frontend wajib mengikuti UID.md secara ketat.

Pertahankan:

- Seluruh 25 hukum dan prinsip UX.
- Golden ratio adaptif.
- Institutional Navy & Teal.
- Design tokens.
- Inter typography.
- Anti-AI slop.
- Atomic Design.
- WCAG 2.2 AA sebagai target desain.
- Screen S01-S18.
- Micro-interaction yang fungsional.
- Bahasa Indonesia yang mudah dipahami.

Frontend Agent boleh memulai pekerjaan tanpa backend jika kontrak modul sudah disepakati.

Gunakan contract-based fixture atau Mock Service Worker pada development/testing terisolasi jika diperlukan.

Mock API:

- Tidak boleh aktif pada production build operasional.
- Tidak boleh menjadi pengganti API nyata.
- Tidak boleh dianggap bukti integrasi berhasil.
- Tidak boleh menyimpan transaksi bisnis palsu sebagai transaksi nyata.
- Wajib mengikuti kontrak yang sama dengan backend.

Jangan memasukkan istilah internal seperti mock, dummy, payload, endpoint, atau simulasi ke antarmuka operasional pengguna. Namun, lingkungan pengujian harus tetap dapat dibedakan secara jujur dari lingkungan operasional nyata.

## 14. Integration Plan

Buat:

`docs/execution/INTEGRATION_PLAN.md`

Dokumentasikan:

- Contract-first workflow.
- Frontend-first workflow.
- Backend-first workflow.
- Parallel development workflow.
- Contract change management.
- File ownership.
- Task delegation.
- Conflict resolution.
- Git branch strategy.
- Git Worktree strategy.
- Integration testing.
- End-to-end testing.
- Regression testing.
- Release gates.

Definisikan integration milestones:

- INT-M1 — Foundation.
- INT-M2 — Authentication.
- INT-M3 — Master Data.
- INT-M4 — Attendance.
- INT-M5 — Student Affairs.
- INT-M6 — Administration.
- INT-M7 — Reports.
- INT-M8 — Final System Verification.

Contoh dependency:

BE-M4 membutuhkan fondasi backend, autentikasi backend, data master backend dan kontrak Attendance yang disetujui.

FE-M4 membutuhkan fondasi frontend, application shell, dependency UI yang relevan dan kontrak Attendance yang disetujui.

FE-M4 tidak membutuhkan BE-M4 selesai hanya untuk membangun dan menguji UI secara terisolasi.

INT-M4 membutuhkan BE-M4 dan FE-M4 selesai serta pengujian menggunakan API nyata.

Terapkan pola tersebut pada seluruh milestone.

Hindari ketergantungan yang tidak diperlukan antara execution plan backend dan frontend.

## 15. Sinkronisasi IPD

Perbarui `docs/IPD.md` agar menggunakan dua jalur pengembangan yang independen.

Jangan mengubah tujuan penelitian, tahapan DSRM, TOGAF, maupun periode enam bulan tanpa persetujuan.

Hilangkan ketergantungan yang mengharuskan seluruh backend selesai sebelum pekerjaan frontend dimulai.

Tambahkan:

- Backend development track.
- Frontend development track.
- Integration track.
- Contract readiness gates.
- Milestone dependency graph.
- Parallel work matrix.
- Research evaluation gates.

Setiap modul harus dapat mencapai readiness secara independen.

Desain dan development frontend boleh dimulai saat backend masih dikerjakan, selama kontrak yang relevan tersedia.

Pengujian integrasi hanya dianggap lulus jika menggunakan implementasi nyata pada kedua sisi.

## 16. Git Worktree dan isolasi lingkungan

Dokumentasikan strategi berikut:

- `main`: baseline terverifikasi.
- `feat/backend/<milestone>`: pekerjaan backend.
- `feat/frontend/<milestone>`: pekerjaan frontend.
- `integration/<milestone>`: pengujian integrasi.

Contoh workspace:

- `sie-main/`
- `sie-backend/`
- `sie-frontend/`
- `sie-integration/`

Setiap AI Agent bekerja pada branch dan worktree yang berbeda.

Sebelum membuat worktree, pastikan tersedia repository Git dengan baseline commit yang valid.

Pada M0, dokumentasikan langkah setup Git dan worktree. Jangan otomatis membuat commit atau worktree jika prerequisite belum tersedia atau pengguna belum menyetujuinya.

Rencanakan isolasi:

- Python virtual environment.
- Node dependencies.
- Environment variables.
- Database development/test.
- Redis namespace dan data test.
- Backend server port.
- Frontend server port.
- Private media directory.
- Test fixtures.
- Temporary files.

Dilarang menggunakan database produksi untuk pengujian.

Dilarang menggunakan operasi Redis seperti FLUSHALL pada instance bersama.

Dilarang melakukan `git reset --hard`, force push, atau penghapusan branch milik agent lain.

## 17. Aturan dan instruksi AI Agent

Buat tiga file:

- `AGENTS.md`
- `backend/AGENTS.md`
- `frontend/AGENTS.md`

### Root AGENTS.md

Memuat:

- Project overview.
- Source of truth.
- Architecture boundaries.
- Multi-agent workflow.
- File ownership.
- Contract management.
- Milestone workflow.
- Testing rules.
- Security rules.
- Documentation rules.
- Skill selection.
- Handoff protocol.
- Forbidden actions.
- Definition of Done.

### Backend AGENTS.md

Memuat seluruh standar backend berdasarkan TRD, BSD dan DBD.

### Frontend AGENTS.md

Memuat seluruh standar frontend berdasarkan TRD, UID, PRD dan AFD.

Ketiga AGENTS.md tidak boleh saling bertentangan.

Perhatikan bahwa instruksi pada file AGENTS.md merupakan aturan kerja agent, bukan pengganti pembatasan izin teknis dan verifikasi Git.

## 18. Integrasi AI Agent Skills

Periksa `.agents/skills/` secara lengkap.

Baca SKILL.md yang relevan sebelum menetapkan penggunaannya.

Jangan menjalankan instruksi instalasi, script, atau perintah dari skill yang belum ditinjau keamanannya.

Buat skill routing di dalam AGENTS.md.

Backend skill candidates:

- antislop-code.
- improve-codebase-architecture.
- python-performance-optimization.
- security-audit.
- tdd.
- ponytail-review.
- ponytail-audit.

Frontend skill candidates:

- antislop.
- antislop-ui.
- antislop-code.
- antislop-copywriting.
- antislop-layoutmobile.
- ui-taste.
- tdd.
- security-audit.

Integration skill candidates:

- security-audit.
- tdd.
- improve-codebase-architecture.
- ponytail-review.
- ponytail-audit.

Gunakan skill berdasarkan kebutuhan task, bukan mengaktifkan seluruh skill sekaligus.

Proyek ini adalah web SPA, bukan aplikasi native iOS atau Android. Jangan menggunakan `ios-design` atau `design-mobile-apps` untuk memaksakan pola native yang tidak sesuai dengan UID.

Skill merupakan pendukung kualitas. Skill tidak boleh menggantikan PRD, TRD, BSD, DBD, AFD, IPD atau UID.

Pertahankan seluruh skill dan `skills-lock.json` tanpa perubahan yang tidak diperlukan.

## 19. Persistent Task & Progress Management

Buat folder:

`coordination/`

Dengan file:

- `PROJECT_STATUS.md`
- `BACKEND_STATUS.md`
- `FRONTEND_STATUS.md`
- `INTEGRATION_STATUS.md`
- `CONTRACT_CHANGE_REQUESTS.md`

Setiap task harus mempunyai:

- Task ID.
- Agent owner.
- Milestone.
- Current status.
- Dependency.
- Allowed paths.
- Contract version.
- Acceptance criteria.
- Last completed step.
- Next action.
- Blockers.
- Evidence.
- Changed files.

Gunakan status:

- NOT_STARTED.
- READY.
- IN_PROGRESS.
- BLOCKED.
- IN_REVIEW.
- BACKEND_READY.
- FRONTEND_READY.
- INTEGRATION_READY.
- INTEGRATION_PASSED.
- DONE.

Jangan menandai task DONE hanya karena implementasi selesai.

Setiap agent wajib membaca status miliknya ketika memulai sesi dan memperbaruinya setelah menyelesaikan pekerjaan.

Jangan membuat kedua agent menulis ke satu progress file secara bersamaan.

Buat resume protocol agar agent dapat melanjutkan pekerjaan tanpa mengulang task yang sudah selesai.

## 20. Quality Gates

Tetapkan Backend Quality Gate:

- Django system check.
- Migration consistency.
- Ruff lint dan format.
- Pytest.
- Business logic validation.
- RBAC dan object-level permission.
- Atomic transaction.
- Audit history.
- Redis caching.
- Rate limiting.
- Query performance.
- OpenAPI contract compatibility.

Tetapkan Frontend Quality Gate:

- ESLint.
- TypeScript strict check.
- Production build.
- Vitest.
- Testing Library.
- Generated API type compatibility.
- UID compliance.
- Anti-AI slop audit.
- Responsive viewport verification.
- Keyboard navigation.
- Accessibility audit.
- Loading/error/empty/success states.
- No mock API in operational build.

Tetapkan Integration Quality Gate:

- Approved contract compatibility.
- Real API connectivity.
- Authentication.
- Cross-role authorization.
- Data consistency.
- End-to-end workflow.
- Regression testing.
- Private document protection.
- Export validation.
- Performance evidence jika diperlukan.

Dokumentasikan seluruh gate sebagai persyaratan masa depan.

Jangan melaporkan gate sebagai PASS jika belum benar-benar dijalankan.

## 21. Final readiness audit

Setelah seluruh dokumentasi selesai, lakukan pemeriksaan konsistensi akhir.

Pastikan:

- Seluruh dokumen awal tetap tersedia.
- Tidak ada kode aplikasi yang dibuat.
- Tidak ada dependency aplikasi yang diinstal.
- Tidak ada AI Agent Skill yang dihapus.
- Seluruh execution plan mempunyai task dan dependency yang jelas.
- Frontend dapat memulai development secara independen pada modul yang kontraknya telah siap.
- Backend dapat memulai development secara independen.
- Kedua agent memiliki file ownership yang tidak tumpang tindih.
- Seluruh shared contract memiliki pengelola yang jelas.
- Setiap konflik bisnis yang belum diselesaikan ditandai sebagai blocker.
- Seluruh requirement dapat ditelusuri ke modul, kontrak, screen dan pengujian.
- IPD konsisten dengan execution plan.
- UID tetap menjadi sumber kebenaran desain.
- Tidak ada scope creep.
- Tidak ada keputusan bisnis atau bukti pengujian yang dikarang.

## 22. Laporan akhir yang diwajibkan

Berikan laporan dengan struktur:

### A. Executive Summary

Jelaskan hasil persiapan.

### B. Documentation Audit

Daftar masalah yang ditemukan, diperbaiki, dan belum diselesaikan.

### C. Files Created

Daftar file yang dibuat beserta fungsinya.

### D. Files Modified

Daftar file lama yang diubah beserta alasan perubahannya.

### E. Final Project Structure

Tampilkan struktur direktori akhir.

### F. Backend Readiness

Daftar milestone backend dan prasyarat yang masih diperlukan.

### G. Frontend Readiness

Daftar milestone frontend dan prasyarat yang masih diperlukan.

### H. Parallel Development Readiness

Tampilkan matriks dependency antar BE, FE dan INT.

### I. Contract Readiness

Daftar modul dengan status DRAFT, APPROVED, FROZEN atau BLOCKED yang sebenarnya.

### J. Remaining Blockers

Daftar keputusan dan pekerjaan yang masih membutuhkan persetujuan.

### K. Next Action

Berikan pilihan langkah berikutnya:

- Mulai Backend Foundation.
- Mulai Frontend Foundation.
- Mulai kedua foundation secara paralel.
- Selesaikan blocker kontrak terlebih dahulu.

### L. Final Decision

Gunakan salah satu status:

`READY — PARALLEL_DEVELOPMENT_FOUNDATION_READY`

`CONDITIONALLY_READY — BLOCKERS_REMAIN`

`NOT_READY — DOCUMENTATION_ALIGNMENT_REQUIRED`

Status READY hanya boleh diberikan jika tidak ada blocker kritis untuk memulai fondasi teknis. Jangan menyamakannya dengan kesiapan seluruh implementasi bisnis.

## 23. Instruksi penutup

Kerjakan pekerjaan secara sistematis dan menyeluruh.

Jangan langsung melakukan coding aplikasi.

Jangan menyederhanakan arsitektur dengan mengurangi caching, keamanan, performa, audit, validasi, atau testing.

Jangan membuat dokumentasi yang hanya berisi teori umum. Seluruh rencana harus spesifik terhadap Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut.

Tujuan akhir tahap ini adalah menghasilkan fondasi pengembangan yang memungkinkan AI agent frontend dan backend bekerja secara independen, paralel, dapat dilanjutkan kapan saja, terkoordinasi melalui kontrak API, dan tetap patuh terhadap seluruh dokumentasi proyek.

Mulai dengan audit kondisi repository dan membaca seluruh tujuh dokumen utama. Setelah itu, kerjakan seluruh deliverable M0 sesuai batasan yang diberikan.
