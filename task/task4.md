# MASTER EXECUTION — COMPLETE FRONTEND DEVELOPMENT, UI/UX IMPROVEMENT, TESTING & FINALIZATION

## PROJECT: SISTEM INFORMASI ENTERPRISE ADMINISTRASI SMA NEGERI 1 BUNUT

## SCOPE: FE-M0 THROUGH FE-M10

## MODE: AUTONOMOUS FULL DEVELOPMENT — CONTRACT-FIRST — DESIGN-DRIVEN — CONTINUOUS QUALITY IMPROVEMENT

---

# 1. ROLE AND PRIMARY OBJECTIVE

Bertindak sebagai:

- Principal Frontend Engineer.
- Senior React TypeScript Engineer.
- Senior UI/UX Designer.
- Design System Engineer.
- Interaction Designer.
- API Integration Engineer.
- Accessibility Engineer.
- Frontend Security Engineer.
- Software Quality Assurance Engineer.
- Performance Engineer.

Anda adalah Frontend Development Agent untuk proyek Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut.

Tugas utama Anda adalah mengembangkan frontend secara menyeluruh mulai dari FE-M0, implementasi seluruh fitur, integrasi API, pengujian, improvement UI/UX, hingga finalisasi.

Jangan berhenti setelah membuat scaffold, landing page, authentication page, atau dashboard.

Bangun aplikasi yang benar-benar fungsional dan dapat digunakan oleh pengguna sekolah.

Target akhir:

`READY — COMPLETE_FRONTEND_IMPLEMENTED_TESTED_AND_UX_REFINED`

Frontend harus:

- Mengikuti requirement proyek.
- Mengikuti kontrak API aktual.
- Mengikuti RBAC.
- Mengikuti workflow bisnis.
- Memanfaatkan desain Pencil.
- Memiliki UI/UX berkualitas tinggi.
- Anti AI slop.
- Responsif.
- Accessible.
- Aman.
- Performant.
- Mudah dipelihara.
- Solo developer friendly.
- Siap untuk Integration Track.

Anda diizinkan melakukan improvement UI/UX jika desain Pencil kurang sesuai ketika diterapkan pada browser.

Jangan menganggap desain Pencil sebagai desain yang tidak boleh disempurnakan.

Namun, improvement visual tidak boleh mengubah kebutuhan bisnis, kontrak API, hak akses, dan identitas design system tanpa persetujuan yang diperlukan.

Kerjakan seluruh milestone secara otomatis dan berkelanjutan.

Jika suatu milestone memiliki blocker eksternal, lanjutkan pekerjaan independen yang aman.

Jangan berhenti hanya untuk memberikan laporan sementara jika masih terdapat pekerjaan yang dapat diselesaikan.

---

# 2. PROJECT WORKSPACE

Project root:

`D:\Kuliah\joki\radit\PROJEK istri bg givo`

Frontend:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\frontend`

Backend:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\backend`

AI Agent Skills:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Design:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\design`

Design tokens:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\design\tokens.json`

Pencil master canvas:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\design\master-canvas.pen`

Contracts:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\contracts`

Coordination:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\coordination`

Gunakan absolute path hanya untuk menemukan workspace.

Gunakan relative path dalam source code, konfigurasi, script, dan dokumentasi.

---

# 3. STRICT FILE OWNERSHIP

Writable scope:

- `frontend/**`
- `coordination/FRONTEND_STATUS.md`

Read-only scope:

- `backend/**`
- `design/**`
- `contracts/**`
- `docs/**`
- `.agents/skills/**`
- Root `AGENTS.md`
- Coordination status milik agent lain.

Frontend Agent diperbolehkan:

- Membuat dan memperbaiki frontend.
- Menyempurnakan layout.
- Menyempurnakan komponen.
- Memperbaiki interaction design.
- Memperbaiki responsive behavior.
- Memperbaiki typography, spacing dan visual hierarchy.
- Membuat frontend-specific component tokens atau semantic mappings yang konsisten dengan token utama.
- Membuat visual evidence dari implementasi aktual.
- Membuat usulan improvement desain.

Frontend Agent tidak diperbolehkan:

- Mengubah backend secara sepihak.
- Mengubah OpenAPI.
- Mengubah DBML.
- Mengubah RBAC.
- Mengubah requirement bisnis.
- Mengubah file master-canvas.pen.
- Mengubah design/tokens.json.
- Mengubah configuration MCP yang sudah bekerja.
- Mengubah file ownership.

Jika improvement membutuhkan perubahan master design atau shared design tokens, catat perubahan yang diusulkan kepada Design Agent atau Coordinator.

Implementasikan improvement frontend yang tidak bertentangan dengan sumber yang disetujui.

Jangan membuat shared design drift yang tidak terdokumentasi.

---

# 4. MANDATORY DOCUMENT REVIEW

Sebelum implementasi, baca langsung:

## Agent instructions

- `AGENTS.md`
- `frontend/AGENTS.md`
- `design/AGENTS.md`

## Primary documents

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/DBD.md`
- `docs/BSD.md`
- `docs/AFD.md`
- `docs/IPD.md`
- `docs/UID.md`

## Supporting documents

- `docs/RBAC_MATRIX.md`
- `docs/DECISION_LOG.md`
- `docs/DOCUMENTATION_ALIGNMENT_REPORT.md`

## Execution plans

- `docs/execution/FRONTEND_EXECUTION_PLAN.md`
- `docs/execution/DESIGN_EXECUTION_PLAN.md`
- `docs/execution/BACKEND_EXECUTION_PLAN.md`
- `docs/execution/INTEGRATION_PLAN.md`

## Contracts

- `contracts/openapi.v1.yaml`
- `contracts/database.dbml`
- `contracts/README.md`

## Coordination

Baca seluruh file relevan pada:

`coordination/`

Terutama:

- PROJECT_STATUS.md
- FRONTEND_STATUS.md
- BACKEND_STATUS.md
- DESIGN_STATUS.md
- INTEGRATION_STATUS.md
- CONTRACT_CHANGE_REQUESTS.md

## Design deliverables

- `design/DESIGN_HANDOFF.md`
- `design/DESIGN_AUDIT_REPORT.md`
- `design/tokens.json`
- `design/master-canvas.pen`
- `design/evidence/`

## Backend deliverables

- `backend/BACKEND_IMPLEMENTATION_REPORT.md`
- `backend/BACKEND_CHANGELOG.md`

Jangan hanya membaca laporan ringkasan apabila file sumber aktual tersedia.

Gunakan source code backend secara read-only untuk memastikan perilaku API apabila diperlukan.

## Source hierarchy

- PRD menentukan kebutuhan.
- AFD menentukan workflow.
- RBAC menentukan kewenangan.
- OpenAPI menentukan kontrak HTTP.
- DBML menentukan struktur data.
- TRD menentukan teknologi.
- UID menentukan prinsip desain.
- Pencil menjadi baseline visual.
- Execution plan menentukan task dan acceptance criteria.

Jika terdapat konflik, gunakan keputusan terbaru yang disetujui sesuai governance.

Jangan mengarang keputusan bisnis untuk menyelesaikan konflik.

---

# 5. BACKEND BASELINE

Backend telah dilaporkan menyelesaikan BE-M1 sampai BE-M9.1.

Baseline terakhir:

- 7 domain modules.
- 49 business API operations.
- 1 infrastructure healthcheck.
- 71 OpenAPI schemas.
- 18 domain database tables.
- 93 automated tests passed.
- 84% line coverage.
- SQLite WAL development.
- PostgreSQL integration verification belum selesai.
- Real Redis integration verification belum selesai.

Backend status:

`CONDITIONALLY_READY — BACKEND_IMPLEMENTED_WITH_VERIFICATION_BLOCKERS`

Kontrak:

- OpenAPI 3.1.
- Revision 1.1.0.
- Development base URL: `http://localhost:8000/api`.

Verifikasi seluruh baseline terhadap kondisi aktual.

Jangan menganggap angka laporan sebagai bukti otomatis bahwa seluruh backend aman dan terverifikasi.

Known issues:

1. PostgreSQL real integration masih BLOCKED.
2. Redis real integration masih BLOCKED.
3. Authentication dapat fail-closed jika Redis tidak tersedia.
4. AttendanceBulkRequest belum memiliki stale-update precondition yang lengkap.
5. Pending school policies masih harus mengikuti keputusan Coordinator dan sekolah.
6. Desain UX-M9.3 dapat memiliki mapping lama sebelum OpenAPI v1.1.0.

Frontend harus menangani kondisi aktual secara benar.

Jangan membuat fake login, fake API success atau authorization bypass.

---

# 6. MANDATORY AI AGENT SKILLS

Gunakan skills dari:

`D:\Kuliah\joki\radit\PROJEK istri bg givo\.agents\skills`

Lakukan discovery dan baca SKILL.md dari setiap skill yang relevan.

## UI/UX

- ui-taste
- antislop
- antislop-ui
- antislop-layoutmobile
- antislop-copywriting
- design-mobile-apps

Gunakan design-mobile-apps hanya untuk prinsip interaksi mobile yang relevan pada responsive web.

Jangan mengubah aplikasi administrasi sekolah menjadi aplikasi bergaya iOS-native tanpa kebutuhan.

## Architecture

- improve-codebase-architecture
- antislop-code
- ponytail

## Testing

- tdd
- ponytail-review
- ponytail-audit

## Security

- security-audit

## Optimization

- ponytail-gain
- ponytail-debt
- ponytail-review

Jangan menggunakan skill yang tidak relevan hanya untuk memenuhi checklist.

Untuk setiap skill, catat:

- Nama skill.
- Milestone penggunaan.
- Instruksi yang diterapkan.
- Dampak implementasi.
- Bukti hasil.

Jangan mengklaim menggunakan skill yang belum dibaca.

---

# 7. PENCIL MCP — BASELINE DESIGN & VISUAL REFERENCE

Pencil MCP telah diinisialisasi.

Gunakan master canvas:

`design/master-canvas.pen`

Periksa melalui capability Pencil MCP aktual:

- Frame.
- Node ID.
- Layout.
- Dimensions.
- Typography.
- Color.
- Spacing.
- Component hierarchy.
- Screen states.
- Responsive variants.
- Visual evidence.

Jangan mengarang node ID.

Jangan menginstal ulang Pencil jika sudah berfungsi.

Jangan mengubah master canvas melalui Frontend Agent.

## Design philosophy

Pencil adalah baseline visual, bukan batas kreativitas implementasi.

Gunakan prinsip:

`PENCIL BASELINE → FUNCTIONAL IMPLEMENTATION → BROWSER REVIEW → UX IMPROVEMENT → VALIDATION`

Jangan menyalin desain secara kaku apabila menghasilkan masalah usability.

Jika desain Pencil sudah baik, pertahankan.

Jika desain Pencil kurang baik ketika diimplementasikan, lakukan improvement yang terukur.

Jika Pencil MCP tidak tersedia, gunakan evidence PNG, design handoff dan tokens sebagai fallback.

Catat keterbatasan tersebut.

---

# 8. UI/UX IMPROVEMENT AUTHORIZATION

Anda secara eksplisit diizinkan melakukan improvement UI/UX pada frontend apabila terdapat masalah nyata.

## Perubahan yang diperbolehkan

- Menyesuaikan layout grid.
- Menyesuaikan sidebar width.
- Menyesuaikan header.
- Menyempurnakan typography.
- Memperbaiki hierarchy.
- Memperbaiki spacing.
- Memperbaiki whitespace.
- Mengurangi kartu yang tidak diperlukan.
- Menyederhanakan dashboard.
- Memperbaiki table density.
- Memperbaiki form layout.
- Memperbaiki navigation.
- Memperbaiki mobile layout.
- Memperbaiki accessibility.
- Memperbaiki modal atau drawer.
- Memperbaiki empty state.
- Memperbaiki loading state.
- Memperbaiki error state.
- Memperbaiki button placement.
- Memperbaiki interaction feedback.
- Memperbaiki micro-interactions.
- Memperbaiki copywriting.
- Memperbaiki iconography.

## Perubahan yang dilarang

- Menghilangkan fitur wajib.
- Mengubah workflow bisnis.
- Membuat role baru.
- Memberi hak akses yang tidak disetujui.
- Mengarang API endpoint.
- Mengarang KPI.
- Mengarang field.
- Mengubah data model.
- Mengubah request atau response contract.
- Mengubah pending policy menjadi aktif.
- Mengganti seluruh identitas design system tanpa persetujuan.

## Improvement decision framework

Untuk setiap perubahan yang signifikan, evaluasi:

1. Apa masalah desain sebelumnya?
2. Siapa pengguna yang terdampak?
3. Mengapa desain tersebut kurang efektif?
4. Apa improvement yang diusulkan?
5. Apakah perubahan konsisten dengan tokens?
6. Apakah perubahan mengurangi cognitive load?
7. Apakah perubahan tetap sesuai RBAC?
8. Apakah perubahan tetap sesuai API?
9. Apakah improvement terbukti pada browser?
10. Apakah automated tests tetap lulus?

Jangan melakukan redesign hanya karena preferensi estetika pribadi.

Jangan mendesain ulang seluruh aplikasi apabila hanya beberapa komponen yang bermasalah.

Dokumentasikan before/after dan alasan perubahan.

---

# 9. CODEGRAPH & TRAIL-CODE

## CodeGraph

Proyek telah memiliki:

`@colbymchenry/codegraph`

Gunakan capability aktual untuk:

- AST navigation.
- Symbol search.
- Dependency mapping.
- Caller/callee analysis.
- Blast radius analysis.
- Circular dependency detection.
- Duplicate component detection.
- Shared hook impact analysis.
- Regression planning.

Verifikasi index sesuai branch dan workspace aktif.

Setelah perubahan besar, verifikasi sinkronisasi index.

Jangan menggunakan index dari worktree lain sebagai sumber kode aktual.

## Trail-Code

Proyek telah memiliki:

`@trailhq/trail-code`

Baca learning relevan sebelum setiap milestone.

Catat pembelajaran penting mengenai:

- Architecture decisions.
- Root cause bug.
- UI/UX decisions.
- API integration findings.
- Security fixes.
- Performance improvements.
- Regression prevention.

Jangan menyimpan secrets, token, credentials, data pribadi siswa atau catatan konseling pada learning.

Jika shared `.trail/learnings/` berada di luar writable scope, masukkan usulan learning dalam laporan untuk Coordinator.

Jangan mengarang command atau hasil tool.

---

# 10. TECHNOLOGY STACK

Gunakan stack yang telah ditetapkan TRD.

## Core

- React.
- TypeScript.
- Vite.
- React Router.

## Styling

- Tailwind CSS.
- shadcn/ui.
- Radix UI.
- Lucide React.
- clsx.
- tailwind-merge.

## State management

- TanStack Query v5.
- Zustand untuk client state yang membutuhkan global state.
- React local state untuk state komponen.

## Forms

- React Hook Form.
- Zod.

## API

- Axios.
- openapi-typescript.
- Generated API types.

## Data presentation

- TanStack Table.
- Recharts apabila tersedia data yang relevan.
- Sonner.

## Quality assurance

- Vitest.
- React Testing Library.
- Testing Library User Event.
- Playwright.
- ESLint.
- Prettier.
- axe-core atau tool accessibility yang sesuai.
- Coverage tools.

MSW atau request interception hanya diperbolehkan untuk automated testing yang terisolasi.

Jangan mengaktifkan mock API pada runtime operasional.

Gunakan dependency locking.

Pilih satu package manager sesuai baseline.

Jangan mencampur npm, pnpm dan yarn lockfiles.

Jangan mengganti framework atau major version tanpa kebutuhan yang jelas.

---

# 11. FRONTEND ARCHITECTURE

Gunakan Atomic Design dan feature-based organization sesuai TRD.

Struktur konseptual:

```text
frontend/
├── src/
│   ├── app/
│   ├── components/
│   │   ├── atoms/
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── templates/
│   ├── features/
│   │   ├── auth/
│   │   ├── accounts/
│   │   ├── master-data/
│   │   ├── attendance/
│   │   ├── student-affairs/
│   │   ├── administration/
│   │   └── reports/
│   ├── pages/
│   ├── lib/
│   ├── stores/
│   ├── types/
│   └── main.tsx
├── tests/
├── e2e/
└── evidence/
```

Gunakan struktur aktual sesuai execution plan.

Pertahankan separation of concerns antara:

- Presentation.
- Components.
- Feature logic.
- API client.
- Query hooks.
- Mutation hooks.
- Form schemas.
- State management.
- Routing.
- Generated types.

Jangan menempatkan seluruh aplikasi dalam App.tsx.

Jangan membuat giant components.

Jangan membuat abstraction dan folder hierarchy yang tidak memberikan manfaat.

Solo developer friendly berarti sederhana, jelas, dan maintainable tanpa mengurangi kualitas.

---

# 12. DESIGN SYSTEM — INSTITUTIONAL NAVY & TEAL

Gunakan:

`design/tokens.json`

Sebagai sumber kebenaran token utama.

Baseline referensi:

- Primary: #173B63.
- Primary hover: #102D4D.
- Accent: #12665C.
- Background: #F5F7FA.
- Surface: #FFFFFF.
- Foreground: #172B42.
- Muted foreground: #475569.
- Border: #DCE3EB.
- Focus: #1D4ED8.

Verifikasi nilai aktual.

Implementasikan mapping ke:

- CSS custom properties.
- Tailwind theme.
- Semantic colors.
- Typography.
- Spacing.
- Border radius.
- Shadows.
- Component variants.
- Focus styles.
- Motion durations.

Gunakan Inter atau font aktual yang ditetapkan tokens.

Gunakan fallback yang aman.

Jangan menggunakan terlalu banyak font.

Jangan membuat warna berbeda secara acak pada setiap halaman.

Jangan menggunakan warna kontras rendah untuk teks penting.

Jika ada token yang tidak memenuhi kebutuhan aksesibilitas, gunakan semantic mapping yang aman dalam frontend dan catat usulan koreksi token utama kepada Coordinator.

---

# 13. ANTI AI SLOP — VISUAL QUALITY STANDARD

Gunakan skills ui-taste, antislop-ui, antislop-layoutmobile, dan antislop-copywriting.

Frontend harus terlihat seperti perangkat lunak administrasi sekolah profesional buatan manusia.

Hindari:

- Gradient berlebihan.
- Glassmorphism tanpa kebutuhan.
- Neon glow.
- Decorative floating objects.
- Hero section besar pada dashboard.
- Dashboard dengan terlalu banyak kartu.
- Rounded corners berlebihan.
- Icon containers yang tidak diperlukan.
- Ilustrasi generik AI.
- Chart dekoratif.
- KPI tanpa fungsi.
- Copywriting generik.
- Layout terlalu kosong.
- Spacing yang tidak konsisten.
- Animasi berlebihan.
- UI yang terlihat seperti template SaaS generik.

Prioritaskan:

- Practical layouts.
- Clear typography.
- Efficient tables.
- Readable forms.
- Familiar navigation.
- Meaningful whitespace.
- Clear primary actions.
- Consistent component hierarchy.
- Functional dashboard.
- Natural interaction.
- Institutional character.

Jangan menambahkan dekorasi jika tidak membantu pengguna menyelesaikan pekerjaan.

---

# 14. 25 UI/UX PRINCIPLES

Terapkan sesuai UID.md:

1. Aesthetic-Usability Effect.
2. Choice Overload.
3. Chunking.
4. Cognitive Load.
5. Doherty Threshold.
6. Fitts's Law.
7. Flow.
8. Goal-Gradient Effect.
9. Hick's Law.
10. Jakob's Law.
11. Law of Common Region.
12. Law of Proximity.
13. Law of Prägnanz.
14. Law of Similarity.
15. Law of Uniform Connectedness.
16. Mental Model.
17. Miller's Law.
18. Occam's Razor.
19. Pareto Principle.
20. Parkinson's Law.
21. Peak-End Rule.
22. Postel's Law.
23. Serial Position Effect.
24. Tesler's Law.
25. Von Restorff Effect.

Tunjukkan penerapan aktual, bukan hanya menyebut teori.

Contoh:

- Hick: menu sesuai role.
- Fitts: target aksi mudah dijangkau.
- Proximity: label dan validation message berdekatan.
- Chunking: form panjang dikelompokkan.
- Doherty: feedback segera diberikan.
- Jakob: pola navigasi familiar.
- Cognitive Load: informasi sekunder tidak mengganggu tugas utama.

Jangan menggunakan Postel's Law untuk melemahkan validasi atau security.

Penerapan teori tidak menggantikan evaluasi UAT dan SUS.

---

# 15. RESPONSIVE, GOLDEN RATIO & INTERACTION DESIGN

Gunakan golden ratio secara adaptif pada primary content dan supporting panel.

Jangan memaksakan rasio 62:38 pada tabel yang membutuhkan seluruh ruang.

Gunakan distribusi warna 60/30/10 secara proporsional jika sesuai tokens.

## Desktop

- Sidebar yang efisien.
- Header yang tidak terlalu tinggi.
- Data table dengan ruang memadai.
- Consistent content width.
- Action placement yang jelas.

## Tablet

- Compact sidebar atau drawer.
- Responsive content.
- Table scrolling pada container yang tepat.
- Form yang tetap mudah digunakan.

## Mobile

- Navigation drawer.
- Single-column layout jika sesuai.
- Touch-friendly controls.
- Clear primary actions.
- Tidak ada unintended page overflow.
- Form tidak terlalu sempit.
- Tabel tetap dapat digunakan.

Uji viewport:

- 320 px.
- 375 px.
- 390 px.
- 768 px.
- 1024 px.
- 1280 px.
- 1440 px.
- 1920 px.

Gunakan 1440, 768 dan 390 sebagai canonical visual review sizes jika sesuai UID.

Gunakan micro-interactions dari tokens.

Hormati prefers-reduced-motion.

Jangan menggunakan motion yang menghambat tugas pengguna.

---

# 16. FULL MILESTONE ROADMAP

Kerjakan:

| Milestone | Fokus                                          |
| --------- | ---------------------------------------------- |
| FE-M0     | Preflight & Design Audit                       |
| FE-M1     | Foundation & Design System                     |
| FE-M2     | Authentication & Application Shell             |
| FE-M3     | Master Data                                    |
| FE-M4     | Attendance                                     |
| FE-M5     | Student Affairs                                |
| FE-M6     | Administration & Documents                     |
| FE-M7     | Dashboard, Reports & Audit                     |
| FE-M8     | Security, Accessibility, Performance & Testing |
| FE-M9     | UI/UX Improvement & Design Refinement          |
| FE-M10    | Final Regression & Handoff                     |

FE-M0, FE-M9 dan FE-M10 merupakan tambahan execution stages untuk Frontend Track.

Jangan mengubah shared execution plan secara sepihak.

Catat pemetaan milestone tambahan pada FRONTEND_STATUS.md dan dua laporan frontend sesuai governance.

---

# 17. FE-M0 — PREFLIGHT, DESIGN AUDIT & IMPLEMENTATION READINESS

Sebelum coding:

1. Verifikasi Git repository.
2. Verifikasi branch.
3. Verifikasi worktree.
4. Verifikasi working tree.
5. Periksa frontend existing.
6. Verifikasi Node.js.
7. Verifikasi package manager.
8. Verifikasi dependency baseline.
9. Verifikasi OpenAPI revision.
10. Hitung contract checksum.
11. Verifikasi design tokens.
12. Verifikasi Pencil MCP.
13. Periksa master canvas.
14. Verifikasi seluruh evidence design.
15. Verifikasi CodeGraph.
16. Verifikasi Trail-Code.
17. Baca skills.
18. Periksa backend readiness.
19. Identifikasi integration blockers.
20. Susun implementation mapping.

Jangan menghapus kode existing jika sudah tersedia.

Jangan mengulang scaffolding tanpa alasan.

Jika dedicated worktree tersedia, gunakan worktree tersebut.

Jika belum tersedia, jangan menjalankan beberapa agent yang menulis pada working tree yang sama secara simultan.

Jangan melakukan reset, force push, merge, atau operasi Git destruktif.

## Initial design audit

Periksa seluruh 18 screen groups dan enam dashboard.

Klasifikasikan setiap screen:

- KEEP_AS_BASELINE.
- MINOR_REFINEMENT_REQUIRED.
- RESPONSIVE_REFINEMENT_REQUIRED.
- ACCESSIBILITY_FIX_REQUIRED.
- CONTRACT_ALIGNMENT_REQUIRED.
- MAJOR_UX_IMPROVEMENT_REQUIRED.

Jangan melakukan redesign menyeluruh pada FE-M0.

Identifikasi masalah yang dapat diperbaiki langsung selama implementasi.

## Deliverables

Masukkan ke implementation report:

- Workspace readiness.
- Contract revision.
- Design revision.
- Screen inventory.
- Initial design findings.
- Implementation plan.
- Dependency status.
- Integration blockers.

Setelah FE-M0, langsung lanjutkan FE-M1 jika prerequisite terpenuhi.

---

# 18. FE-M1 — FOUNDATION & DESIGN SYSTEM

Implementasikan:

- React TypeScript initialization atau reuse existing project.
- Vite.
- TypeScript strict mode.
- Tailwind CSS.
- shadcn/ui primitives.
- Semantic design tokens.
- Global styles.
- Typography.
- Atomic Design.
- React Router.
- TanStack Query provider.
- API client foundation.
- Zustand jika diperlukan.
- Environment validation.
- Error boundary.
- Generated OpenAPI types.
- Vitest.
- React Testing Library.
- Playwright.
- ESLint.
- Prettier.

Bangun reusable components:

- Button.
- Input.
- Select.
- Checkbox.
- Radio.
- Badge.
- StatusBadge.
- FormField.
- SearchField.
- FilterField.
- Spinner.
- Skeleton.
- EmptyState.
- ErrorState.
- Dialog.
- Drawer.
- Tooltip.
- DataTable.
- Pagination.

Uji component states, accessibility, token mapping, API URL composition dan build.

Quality gate:

- Typecheck PASS.
- Lint PASS.
- Format check PASS.
- Unit/component tests PASS.
- Production build PASS.

---

# 19. FE-M2 — AUTHENTICATION, RBAC & APPLICATION SHELL

Implementasikan:

- Login.
- Refresh.
- Logout.
- Current user profile.
- Protected routes.
- Permission-aware navigation.
- Application sidebar.
- Header.
- Breadcrumb.
- Profile menu.
- Context selector jika didukung.
- Session expired handling.
- Forbidden page.
- Responsive drawer.
- Skip link.

Enam role:

1. Administrator.
2. Guru.
3. Wali Kelas.
4. Kesiswaan.
5. Tata Usaha.
6. Pimpinan.

Gunakan role identifier aktual dari backend.

Jangan membuat Administrator universal bypass.

Implementasikan additive union untuk multi-role sesuai RBAC.

Role context selector hanya mengubah konteks presentasi apabila tidak ada API role switching resmi.

## Authentication security

- Access token memory-only sesuai keputusan yang disetujui.
- Refresh token mengikuti transport dan storage policy resmi.
- Jangan menyimpan token di localStorage atau persistent store tanpa persetujuan.
- Jangan menyimpan token pada URL.
- Jangan mencatat token ke console.
- Jangan membuat authentication bypass.

Backend menggunakan refresh token rotation dan family reuse detection.

Implementasikan single-flight refresh.

Pastikan beberapa request 401 tidak menyebabkan refresh token yang sama digunakan berulang kali.

Uji:

- Concurrent 401.
- Refresh success.
- Refresh failure.
- Logout ketika refresh berlangsung.
- Late response dari sesi lama.
- Account change.
- Role changes.
- Session expiration.
- Cross-user cache isolation.

Jangan secara otomatis mengulang mutasi non-idempotent.

Jika Redis tidak tersedia, catat real authentication integration sebagai BLOCKED.

Jangan membuat fake login.

---

# 20. FE-M3 — MASTER DATA & ACADEMIC MANAGEMENT

Implementasikan sesuai OpenAPI dan RBAC:

- Account management sesuai milestone resmi.
- Tahun ajaran.
- Kelas.
- Pegawai.
- Siswa.
- Penempatan siswa.
- Penugasan guru.

Cakupan:

- List.
- Detail jika tersedia.
- Create.
- Update.
- Search.
- Server-side filters.
- Server-side pagination.
- Activation/deactivation sesuai kontrak.
- End-date lifecycle.
- Form validation.
- Confirmation.
- Error handling.

Gunakan PATCH operations yang ditambahkan pada baseline M0.2 jika sudah disetujui.

Gunakan field aktual.

Jangan mengarang nisn, full_name, birth_date, address, subject_name atau field lain jika tidak tersedia.

Perhatikan:

- Unique identity.
- Date range.
- Academic year validity.
- Enrollment overlap.
- Assignment overlap.
- Historical data preservation.
- Role restrictions.

Jangan melakukan filtering hanya terhadap satu halaman kemudian mengklaim mencakup seluruh sekolah.

Uji setiap workflow CRUD yang didukung, validation, permission, pagination, search, filters dan mutation failure.

---

# 21. FE-M4 — ATTENDANCE MANAGEMENT

Implementasikan:

- Pemilihan kelas.
- Pemilihan tanggal.
- Attendance roster.
- Input status.
- Catatan.
- Review sebelum penyimpanan.
- Bulk save.
- Attendance recap.
- Report export sesuai role.

Status:

- HADIR.
- SAKIT.
- IZIN.
- ALPA.

Verifikasi enum aktual.

Periksa kebijakan default status pada PRD, Decision Log dan desain terbaru.

Jika default HADIR merupakan keputusan resmi, pertahankan dengan konfirmasi pengguna sebelum menyimpan.

Jika terdapat konflik kebijakan, catat kepada Coordinator.

Jangan menyimpan status hanya karena halaman dibuka.

Jangan mengirim null sebagai AttendanceStatusEnum.

## Usability

- Quick status selection.
- Readable student identity.
- Status legend.
- Keyboard navigation.
- Attendance summary.
- Unsaved changes warning.
- Clear save button.
- Accessible mobile layout.
- Duplicate submission prevention.

## Concurrency

AttendanceBulkRequest saat ini dilaporkan belum memiliki expected_version atau ETag precondition yang lengkap.

Jangan mengarang field.

Tangani response 409 sesuai kontrak.

Pertahankan draft ketika konflik terjadi.

Minta pengguna meninjau data terbaru sebelum mengirim ulang.

Jangan mengklaim lost-update prevention telah teratasi hanya dengan refetch.

Pending correction policy tidak boleh diaktifkan secara sepihak.

---

# 22. FE-M5 — STUDENT AFFAIRS

Implementasikan:

- Case list.
- Search/filter.
- Create case.
- Case detail.
- Case timeline.
- Case assignment sesuai kontrak.
- Case transitions.
- Action notes.
- Completion.
- Cancellation.

Status baseline:

- BARU.
- DIPROSES.
- SELESAI.
- DIBATALKAN.

Action:

- MULAI_PENANGANAN.
- CATAT_TINDAKAN.
- SELESAIKAN.
- BATALKAN.

Verifikasi terhadap YAML aktual.

Gunakan payload:

- action.
- note.
- expected_version.

Jangan menggunakan target_status jika tidak didukung.

## Privacy

Patuhi DEC-TECH-18.

Wali Kelas hanya menerima informasi dalam scope perwalian dan izin yang sah.

Jangan menampilkan catatan konseling yang tidak disediakan server.

Jangan menyimpan catatan privat dalam persistent browser storage.

Jangan membocorkan informasi privat melalui:

- Logs.
- Analytics.
- Error reports.
- Shared caches.
- Previous session state.

Uji masked notes, unauthorized access, version conflict, mandatory note, valid/invalid transitions dan terminal state.

Jangan menambahkan kasus otomatis berdasarkan alpa jika kebijakan belum disetujui.

---

# 23. FE-M6 — ADMINISTRATION & PRIVATE DOCUMENTS

Implementasikan:

- Service types sesuai izin.
- Operational service request list.
- New service request.
- Request detail.
- Processing workflow.
- Approval queue.
- Approval.
- Rejection.
- Completion.
- Request timeline.
- Private document upload.
- Document archive.
- Authorized download.

Status baseline:

- DIAJUKAN.
- DIPROSES.
- MENUNGGU_PERSETUJUAN.
- DISETUJUI.
- DITOLAK.
- SELESAI.

Action:

- PROSES.
- AJUKAN_PERSETUJUAN.
- SETUJUI.
- TOLAK.
- SELESAIKAN.

Verifikasi workflow aktual.

DITOLAK harus diperlakukan sebagai terminal state sesuai keputusan bisnis.

Jangan memberi hak approval kepada Administrator atau Tata Usaha tanpa izin resmi.

Pimpinan hanya mengakses objek dalam scope persetujuannya.

Jangan membuat digital signature, stamp atau document generation workflow yang tidak didukung.

## Private file upload

Implementasikan:

- File selection.
- Type validation.
- Size validation.
- Progress jika didukung.
- Pending state.
- Error handling.
- Success confirmation.

Batas upload mengikuti kontrak aktual, sebelumnya 5 MB.

Gunakan multipart/form-data.

Client validation tidak menggantikan server validation.

## Private download

Gunakan authorized API client.

Tangani binary response dengan benar.

Gunakan Content-Disposition dan safe filename.

Jangan membuat public media URL.

Jangan memasukkan JWT ke query string.

Revoke Blob object URL setelah digunakan.

Uji valid upload, malformed file handling, oversized upload, unauthorized download, version conflict dan seluruh state transitions.

---

# 24. FE-M7 — SIX DASHBOARDS, REPORTS & AUDIT

Implementasikan dashboard untuk:

## Administrator

- Account management.
- Master data.
- Audit access.
- Authorized school aggregates.

## Guru

- Assigned classes.
- Attendance entry.
- Attendance recap.
- Authorized class information.

## Wali Kelas

- Kelas perwalian.
- Rekap siswa binaan.
- Informasi kasus yang diizinkan.

## Kesiswaan

- Case management.
- Case status.
- Authorized metrics.

## Tata Usaha

- Service requests.
- Processing queue.
- Documents.
- Reports.

## Pimpinan

- Approval queue.
- Authorized aggregates.
- Reports.

Gunakan DashboardMetricsResponse aktual.

Jangan mengarang:

- Online users.
- Jadwal mengajar.
- Countdown koreksi.
- SLA.
- Trend data.
- Database statistics.
- Redis statistics.
- Counseling metrics.
- KPI lainnya yang tidak didukung.

Jangan menggunakan chart hardcoded.

Gunakan Recharts hanya apabila data dan kebutuhan visual tersedia.

## Reports

Implementasikan:

- Attendance report.
- Administration report.
- Date filters.
- Class filter jika tersedia.
- Excel export.
- PDF export.

Gunakan data dan binary endpoint backend.

## Audit

Implementasikan:

- Audit log list.
- Filters.
- Pagination.
- Timestamp.
- Actor.
- Action.
- Resource.
- Request ID jika tersedia.

Jangan menampilkan sensitive payload.

Uji dashboard keenam role, metric mapping, missing data, cache isolation, export, filter, permission dan error states.

---

# 25. API CLIENT & CONTRACT-FIRST IMPLEMENTATION

Gunakan centralized Axios API client.

Environment:

`VITE_API_BASE_URL`

Gunakan actual base URL backend.

Jangan membuat `/api/api/`.

Jangan menggunakan `/api/v1/` jika kontrak tidak menentukan prefix tersebut.

Generate TypeScript dari:

`contracts/openapi.v1.yaml`

Sediakan reproducible generation script.

Jangan membuat manual DTO yang menyimpang dari generated types.

Verifikasi seluruh:

- Method.
- Path.
- Operation ID.
- Required fields.
- Request schema.
- Response schema.
- Enum.
- Nullable fields.
- Query parameters.
- Path parameter types.
- Content type.
- Error responses.
- Security requirements.

Buat operation usage matrix untuk seluruh 49 business operations yang disetujui.

Jelaskan operasi yang digunakan oleh frontend, operasi internal, dan operasi yang tidak relevan untuk UI.

Jangan membuat halaman fiktif hanya agar setiap endpoint memiliki halaman.

## ErrorEnvelope

Gunakan:

- code.
- message.
- details.
- request_id.

Tangani:

- 
- 
- 
- 
- 
- 
- 
- 5xx.
- Network errors.
- Timeout.

Jangan menampilkan stack trace atau raw internal exception.

Hormati Retry-After.

Jangan melakukan infinite retry.

---

# 26. STATE MANAGEMENT & CACHE SECURITY

TanStack Query digunakan untuk server state.

Zustand digunakan hanya untuk client state yang membutuhkan global sharing.

Jangan menduplikasi seluruh response API ke Zustand.

Query keys harus mempertimbangkan:

- Resource.
- User identity.
- Session identity.
- Effective role/scope.
- Filters.
- Pagination.
- Date range.
- Class scope.

Implementasikan:

- Request cancellation.
- Controlled retry.
- Appropriate staleTime.
- Appropriate gcTime.
- Cache invalidation.
- Background refetch jika sesuai.
- Mutation pending state.
- Duplicate submission prevention.

Jangan menampilkan optimistic success untuk mutasi kritis:

- Attendance.
- Approval.
- Rejection.
- Case transition.
- Account role changes.
- File upload.

Tunggu konfirmasi server.

Hapus sensitive query cache ketika logout atau sesi berubah.

Cegah late response dari sesi lama.

---

# 27. ALL REQUIRED SCREENS

Pastikan seluruh screen berikut tersedia:

| ID  | Screen                          |
| --- | ------------------------------- |
| S01 | Login                           |
| S02 | Enam dashboard role             |
| S03 | Profil dan konteks              |
| S04 | Manajemen akun                  |
| S05 | Data siswa                      |
| S06 | Tahun ajaran, kelas dan pegawai |
| S07 | Penempatan dan penugasan        |
| S08 | Pencatatan absensi              |
| S09 | Rekap absensi                   |
| S10 | Daftar dan pembuatan kasus      |
| S11 | Detail kasus dan timeline       |
| S12 | Daftar permohonan               |
| S13 | Permohonan baru                 |
| S14 | Detail dan persetujuan          |
| S15 | Arsip dokumen                   |
| S16 | Laporan                         |
| S17 | Audit logs                      |
| S18 | Error dan exception states      |

Pastikan seluruh sub-screen, forms, dialogs, drawers dan states yang diwajibkan tersedia.

Untuk setiap screen, catat:

- Pencil node.
- React route.
- Component.
- Role.
- Permission.
- API mapping.
- Functional status.
- Loading.
- Empty.
- Error.
- Responsive behavior.
- Accessibility.
- Test evidence.
- Visual evidence.

18 screen groups bukan berarti hanya 18 komponen.

Jangan menandai screen selesai jika hanya memiliki route atau placeholder.

---

# 28. USER-FACING LANGUAGE POLICY

Gunakan Bahasa Indonesia yang natural dan profesional.

Konfigurasi:

- lang="id".
- Locale id-ID.
- Timezone Asia/Jakarta sesuai requirement.

Gunakan label bisnis yang mudah dipahami.

Contoh:

- Tambah Siswa.
- Tahun Ajaran.
- Rombongan Belajar.
- Simpan Kehadiran.
- Riwayat Penanganan.
- Ajukan Persetujuan.
- Unduh Dokumen.

Jangan menggunakan istilah teknis yang tidak relevan pada UI operasional:

- Mock.
- Dummy.
- Simulasi.
- Payload.
- DTO.
- API response.
- Redis failure.
- Database query.
- Internal exception.
- Endpoint.
- Backend error.

Istilah teknis boleh digunakan pada kode, test dan developer documentation.

Jangan menyamarkan data sintetis sebagai data sekolah nyata.

Jangan menggunakan lorem ipsum.

Jangan membuat fitur demo yang menyamar sebagai fitur operasional.

---

# 29. FE-M8 — SECURITY, ACCESSIBILITY, PERFORMANCE & TESTING

Lakukan hardening menyeluruh setelah functional implementation tersedia.

Periksa:

- Authentication.
- RBAC.
- Session management.
- Query cache.
- API integration.
- State management.
- Component quality.
- Responsive behavior.
- Accessibility.
- Performance.
- Dependency security.
- Browser compatibility.
- Error handling.
- Maintainability.

Jangan mengulang implementasi yang sudah benar.

Perbaiki masalah nyata berdasarkan evidence.

---

# 30. MANDATORY TESTING — EVERY LAYER

Gunakan TDD untuk logic kritis.

Jalankan pengujian sepanjang development, bukan hanya pada akhir milestone.

## Unit tests

Uji:

- Utility functions.
- Date parsing.
- Date formatting.
- Validation schemas.
- Permission evaluation.
- Error normalization.
- Query keys.
- Role union.
- Status mapping.
- Action mapping.
- API URL composition.
- Refresh coordination.
- File validation.
- Download utilities.

## Component tests

Uji seluruh Atomic Design layers:

- Atoms.
- Molecules.
- Organisms.
- Templates.
- Pages.

Periksa:

- Rendering.
- User interaction.
- Disabled state.
- Loading.
- Error.
- Validation.
- Keyboard.
- Accessibility.
- Callback behavior.

## Hooks tests

Uji:

- Query hooks.
- Mutation hooks.
- Auth hooks.
- Permission hooks.
- Session hooks.
- Form hooks.
- Debounce.
- Request cancellation.

## API layer tests

Uji:

- Request serialization.
- Response handling.
- Authentication header.
- ErrorEnvelope.
- Timeout.
- Cancellation.
- Token refresh.
- Multipart upload.
- Binary download.

## Feature tests

Uji setiap domain:

- Authentication.
- Accounts.
- Master Data.
- Attendance.
- Student Affairs.
- Administration.
- Reports.
- Audit.

Gunakan positive, negative dan boundary cases.

Jangan mengejar jumlah test secara artifisial.

---

# 31. INTEGRATION & N2N TESTING

N2N pada SPA ini berarti pengujian hubungan antar-komponen, feature modules, application boundaries, atau frontend-backend yang memang saling berkomunikasi.

Jangan menambahkan microservices untuk keperluan N2N testing.

Verifikasi:

- Login → API client → Session.
- Session → Router → Navigation.
- RBAC → Menu → Action.
- Master Data → Attendance.
- Master Data → Student Affairs.
- Master Data → Administration.
- Attendance → Recap → Dashboard.
- Case mutation → Timeline → Dashboard.
- Service request → Approval queue.
- Service request → Document archive.
- Reports → Binary download.
- Logout → Query cache cleanup.
- Error response → User feedback.

Bedakan:

1. Unit test dengan test doubles.
2. Component integration dengan fixtures.
3. Contract-based integration test.
4. Real backend integration.
5. Browser E2E dengan backend nyata.

Jangan mengklaim fixture-based testing sebagai real backend integration.

---

# 32. REAL BACKEND INTEGRATION

Gunakan backend BE-M9.1 atau baseline terbaru yang sah.

Verifikasi:

- Backend runtime.
- Healthcheck.
- API availability.
- Base URL.
- CORS.
- Authentication.
- Redis availability.
- Test database.
- Authorized test accounts.
- Contract revision.

Gunakan environment sintetis terisolasi.

Jangan menggunakan data sekolah nyata tanpa izin.

Jangan membuat perubahan pada database operasional.

Jangan mengubah konfigurasi backend untuk melemahkan security.

Jika Redis belum tersedia:

- Catat blocker.
- Jangan membuat auth bypass.
- Jangan mengganti fail-closed dengan fake success.
- Lanjutkan frontend testing yang independen.

Jika PostgreSQL belum tersedia, real frontend integration boleh menggunakan SQLite development selama backend runtime dan Redis memenuhi kebutuhan.

Catat environment aktual.

Jangan mengklaim production integration.

---

# 33. PLAYWRIGHT BROWSER E2E

Gunakan Playwright pada Chromium.

Tambahkan Firefox dan WebKit untuk workflow utama jika environment mendukung.

Pisahkan E2E fixture-based dari E2E backend nyata.

## Required scenarios

### Administrator

- Login.
- Account management.
- Role assignment.
- Master data.
- Enrollment.
- Assignment.
- Audit.
- Logout.

### Guru

- Login.
- Assigned classes.
- Attendance roster.
- Input status.
- Bulk save.
- Recap.
- Export.
- Unauthorized class rejection.

### Wali Kelas

- Kelas perwalian.
- Rekap siswa.
- Case detail sesuai izin.
- Private note protection.
- Out-of-scope rejection.

### Kesiswaan

- Case list.
- Create case sesuai izin.
- Start handling.
- Record action.
- Complete case.
- Verify timeline.

### Tata Usaha

- Service request.
- Upload file.
- Process request.
- Submit approval.
- Archive.
- Download sesuai izin.

### Pimpinan

- Approval queue.
- Approve.
- Reject pada request terpisah.
- Reports.
- Scope restrictions.

### Multi-role

- Union permission.
- Context navigation.
- Global security boundaries.
- Cache isolation.

### Error scenarios

- Invalid login.
- 
- 
- 
- 
- 
- 
- Network unavailable.
- 5xx.
- Logout.
- Browser back setelah logout.
- Session expiration.

Seluruh scenario harus mengikuti workflow yang disetujui.

Jangan menggunakan arbitrary sleep sebagai pengganti deterministic waiting.

Simpan screenshot dan trace failure apabila diperlukan.

---

# 34. ACCESSIBILITY TESTING

Target WCAG 2.2 AA sesuai UID.

Periksa:

- Semantic HTML.
- Heading hierarchy.
- Accessible names.
- Form labels.
- Keyboard navigation.
- Focus indicators.
- Dialog focus trap.
- Focus restoration.
- Error announcement.
- Status announcement.
- Screen reader behavior.
- Contrast.
- Accessible tables.
- Accessible charts.
- Reduced motion.
- Zoom 200%.
- Reflow.

Target contrast:

- Normal text minimal 4.5:1 sesuai kriteria terkait.
- Non-text contrast minimal 3:1 untuk komponen yang relevan.

Gunakan target sentuh internal 44 px jika sesuai desain.

Jangan menyatakan 44 px merupakan persyaratan universal WCAG AA.

Jalankan automated axe checks.

Lakukan manual keyboard testing.

Lakukan screen reader check jika tersedia.

Jangan mengklaim full WCAG compliance hanya berdasarkan automated tests.

---

# 35. FRONTEND SECURITY TESTING

Gunakan security-audit skill.

Periksa:

- XSS.
- Unsafe HTML.
- Unsafe URLs.
- Open redirects.
- Token leakage.
- Persistent storage leakage.
- Session race.
- Refresh token replay dari client.
- Cross-user cache leakage.
- Unauthorized routes.
- Unauthorized actions.
- IDOR-related behavior.
- Private file exposure.
- Unsafe downloads.
- Sensitive console logs.
- Dependency vulnerabilities.

Jangan menggunakan dangerouslySetInnerHTML tanpa kebutuhan sah dan sanitization.

Jangan menyimpan secrets pada VITE_ environment variables.

Jangan memasukkan akun dan password administrator ke client bundle.

Periksa production build terhadap:

- Credentials.
- Test fixtures.
- Mock API imports.
- Debug bypass.
- Sensitive logs.

Jangan mengklaim server authorization aman hanya karena tombol disembunyikan pada frontend.

Security tetap harus diverifikasi pada backend.

---

# 36. PERFORMANCE TESTING

Gunakan:

MEASURE → PROFILE → OPTIMIZE → MEASURE AGAIN.

## Bundle

Ukur:

- Initial JS bundle.
- CSS bundle.
- Total build size.
- Gzip size.
- Largest chunks.
- Duplicate dependencies.
- Route chunks.

Gunakan lazy-loading atau code splitting apabila memberi manfaat terukur.

Jangan membuat terlalu banyak chunks kecil tanpa alasan.

## Rendering

Periksa:

- Unnecessary re-render.
- Expensive calculations.
- Large tables.
- Unbounded lists.
- Excessive global state.
- Repeated formatting.
- Unstable dependencies.

Gunakan pagination sebelum virtualization.

Jangan menggunakan useMemo dan useCallback di setiap tempat tanpa alasan.

## Network

Periksa:

- Duplicate requests.
- HTTP request waterfalls.
- N+1 requests.
- Unnecessary refetch.
- Search frequency.
- Request cancellation.
- Cache invalidation scope.

## Browser metrics

Ukur jika tersedia:

- LCP.
- INP.
- CLS.
- FCP.
- TBT sebagai lab metric.
- Navigation time.
- Interaction feedback.
- Network duration.

Technical target referensi:

- LCP ≤ 2.5 detik.
- INP ≤ 200 ms.
- CLS ≤ 0.1.

Gunakan target resmi TRD/UID jika tersedia.

Jangan menyamakan lab measurements dengan real-user field metrics.

## Workloads

- Login.
- Dashboard.
- Student list.
- Search.
- Attendance roster.
- Attendance editing.
- Case list.
- Service request list.
- Reports.

Catat:

- Browser.
- Device.
- Dataset size.
- Build mode.
- Network condition.
- Backend state.
- Database.
- Redis state.
- Sample count.
- Before/after measurement.

Jangan mengklaim aplikasi cepat tanpa bukti.

---

# 37. FE-M9 — UI/UX IMPROVEMENT & DESIGN REFINEMENT

Ini merupakan milestone khusus penyempurnaan frontend setelah seluruh fitur utama tersedia.

Anda diberikan kewenangan untuk memperbaiki UI/UX yang kurang sesuai dari baseline Pencil.

Jangan sekadar melakukan audit atau memberikan rekomendasi.

Lakukan perbaikan aktual pada kode frontend.

## Step 1 — Browser review

Jalankan frontend melalui browser nyata.

Periksa:

- Seluruh 18 screen groups.
- Seluruh enam dashboard.
- Forms.
- Data tables.
- Dialogs.
- Drawers.
- Error states.
- Loading states.
- Empty states.
- Responsive variants.

Ambil screenshot implementasi sebelum improvement untuk screen yang akan diubah.

Bandingkan dengan master Pencil canvas.

## Step 2 — UX audit

Evaluasi setiap screen menggunakan:

- ui-taste.
- antislop-ui.
- antislop-layoutmobile.
- antislop-copywriting.
- 25 UI/UX principles.
- UID.md.
- Design tokens.
- Accessibility requirements.

Periksa:

- Visual hierarchy.
- Navigation clarity.
- Information density.
- Task efficiency.
- Cognitive load.
- Form usability.
- Table usability.
- Consistency.
- Readability.
- Mobile usability.
- Interaction feedback.
- Role relevance.

## Step 3 — Prioritize findings

Klasifikasikan:

- P0: Critical usability/accessibility issue.
- P1: Major usability issue.
- P2: Visual consistency issue.
- P3: Optional cosmetic refinement.

Prioritaskan P0 dan P1.

Jangan menghabiskan waktu pada perubahan kosmetik kecil jika workflow pengguna masih bermasalah.

## Step 4 — Improve UI/UX

Perbaiki desain yang terbukti kurang sesuai.

Contoh:

- Sidebar terlalu lebar → ringkas tanpa menghilangkan navigasi.
- Dashboard terlalu padat → prioritaskan tugas utama.
- Dashboard terlalu kosong → gunakan ruang untuk informasi relevan.
- Terlalu banyak KPI cards → kelompokkan secara logis.
- Form terlalu panjang → gunakan grouping.
- Table actions bertumpuk → atur prioritas dan overflow.
- Mobile attendance sulit digunakan → perbaiki responsive interaction.
- Kontras kurang → perbaiki semantic color mapping.
- Button hierarchy tidak jelas → konsistenkan primary/secondary actions.
- Empty state generik → berikan penjelasan dan tindakan relevan.
- Error teknis → ubah menjadi pesan bisnis.
- Modal terlalu besar → sesuaikan layout dan viewport.
- Typography terlalu kecil → perbaiki keterbacaan.
- Padding tidak konsisten → ikuti spacing system.

Anda boleh menghasilkan frontend yang secara visual lebih baik daripada baseline Pencil.

Tetap pertahankan:

- Institutional Navy & Teal.
- Design token governance.
- Atomic Design.
- 25 UI/UX principles.
- Workflow.
- RBAC.
- Contract alignment.

## Step 5 — Before/after validation

Untuk setiap improvement signifikan, catat:

- Finding ID.
- Affected screen.
- Original design.
- Problem.
- Improvement.
- Screenshot before.
- Screenshot after.
- Accessibility impact.
- Responsive impact.
- Performance impact.
- Functional regression result.

Jika improvement tidak memberikan manfaat atau menyebabkan regression, revisi atau batalkan perubahan tersebut.

## Step 6 — Visual consistency pass

Pastikan seluruh aplikasi konsisten pada:

- Typography.
- Colors.
- Spacing.
- Iconography.
- Buttons.
- Tables.
- Forms.
- Sidebar.
- Header.
- Status badges.
- Dialogs.
- Loading states.
- Error states.
- Interaction patterns.

Jangan memperbaiki satu halaman tetapi membuat halaman lain berbeda secara tidak konsisten.

## Step 7 — Retest

Jalankan kembali:

- Component tests.
- Feature tests.
- Visual regression.
- Responsive tests.
- Accessibility tests.
- Browser E2E.
- Security tests.
- Performance checks.
- Full regression suite.

FE-M9 hanya dinyatakan selesai setelah improvement yang dibutuhkan telah diterapkan atau temuan dinyatakan tidak memerlukan perubahan berdasarkan bukti.

---

# 38. FE-M10 — FINAL REGRESSION & INTEGRATION READINESS

Lakukan final verification terhadap seluruh frontend.

Jangan menambahkan fitur baru pada tahap ini.

## Functional verification

Periksa:

- Semua routes.
- Semua screen.
- Semua forms.
- Semua workflow.
- Semua role.
- Semua action permissions.
- Semua API consumers.
- Loading/empty/error states.

## Final visual verification

Periksa:

- Desktop.
- Tablet.
- Mobile.
- Typography.
- Layout.
- Tokens.
- Responsive behavior.
- Design consistency.
- UI/UX improvements.

## Final code review

Gunakan:

- CodeGraph.
- antislop-code.
- ponytail-review.
- ponytail-audit.
- ponytail-debt.
- improve-codebase-architecture.

Periksa:

- Dead code.
- Duplicate logic.
- Circular imports.
- Unused components.
- Duplicate hooks.
- Large components.
- Unnecessary abstractions.
- TypeScript any.
- Ignored lint rules.
- Excessive useEffect.
- Unbounded retries.
- Hardcoded data.
- Runtime mock imports.

## Final runtime verification

- Production build.
- Production preview smoke test.
- Deep links.
- Browser reload.
- Authentication.
- Protected routes.
- API connection.
- Logout.
- Report download.
- Private document workflow.

Jangan melakukan deployment produksi.

## Final handoff

Sediakan:

- Screen implementation matrix.
- Role action matrix.
- API usage matrix.
- Design improvement matrix.
- Test results.
- Performance results.
- Security findings.
- Accessibility findings.
- Known blockers.
- Integration readiness.

Masukkan semuanya ke dua laporan utama.

---

# 39. FAILED TEST — AUTOMATIC ROOT CAUSE REPAIR

Jika test gagal, jangan berhenti hanya dengan melaporkan failure.

Lakukan:

1. Reproduce.
2. Inspect error.
3. Read stack trace.
4. Inspect code.
5. Check approved contract.
6. Check business rules.
7. Check design behavior.
8. Check test assertions.
9. Check fixtures.
10. Check environment.
11. Analyze blast radius.
12. Identify root cause.
13. Fix.
14. Retest.
15. Run regression suite.

Klasifikasikan:

- LOGIC_BUG.
- UI_BUG.
- COMPONENT_BUG.
- TEST_CODE_BUG.
- FIXTURE_BUG.
- CONTRACT_MISMATCH.
- BACKEND_BUG.
- SECURITY_BUG.
- ACCESSIBILITY_BUG.
- RESPONSIVE_BUG.
- PERFORMANCE_REGRESSION.
- ENVIRONMENT_ISSUE.
- FLAKY_TEST.
- SHARED_CONTRACT_BLOCKER.

Jika code logic salah, perbaiki logic.

Jika code test salah, perbaiki expected behavior berdasarkan requirement aktual.

Jika fixture salah, koreksi fixture.

Jika backend salah, dokumentasikan dan teruskan kepada Backend Agent.

Jika kontrak tidak lengkap, teruskan kepada Coordinator.

Jangan mengubah backend atau shared contract dari Frontend Track.

DILARANG:

- Menghapus test agar lulus.
- Melemahkan assertion.
- Menonaktifkan authorization.
- Menonaktifkan validation.
- Menyembunyikan failure dengan skip.
- Mengganti API nyata dengan fake response.
- Memperbarui visual snapshot tanpa review.
- Mengarang hasil PASS.

---

# 40. COVERAGE & REGRESSION REQUIREMENTS

Laporkan:

- Line coverage.
- Branch coverage.
- Function coverage.
- Statement coverage.
- Coverage per feature.
- Coverage per critical layer.

Gunakan target resmi execution plan jika tersedia.

Jika belum tersedia, gunakan risk-based technical target dan dokumentasikan alasan.

Prioritaskan:

- Authentication.
- RBAC.
- Token refresh.
- Query cache security.
- Forms.
- Attendance.
- Case transitions.
- Approval.
- Private files.
- Error handling.

Jangan mengejar coverage tinggi menggunakan test trivial.

Setiap perubahan shared component wajib menjalankan regression test terhadap consumer yang terdampak.

Pertahankan seluruh pengujian valid dari milestone sebelumnya.

---

# 41. MILESTONE EXECUTION PROTOCOL

Untuk setiap milestone:

1. Baca FRONTEND_STATUS.md.
2. Verifikasi prerequisite.
3. Verifikasi contract revision.
4. Baca design frames.
5. Baca relevant skills.
6. Baca Trail learning.
7. Gunakan CodeGraph.
8. Susun implementation plan.
9. Rumuskan test scenarios.
10. Implementasikan.
11. Jalankan unit tests.
12. Jalankan component tests.
13. Jalankan integration tests.
14. Jalankan contract tests.
15. Jalankan browser tests yang relevan.
16. Jalankan accessibility checks.
17. Jalankan responsive checks.
18. Jalankan security checks.
19. Jalankan performance checks.
20. Perbaiki seluruh failure dalam scope.
21. Jalankan regression suite.
22. Perbarui implementation report.
23. Perbarui changelog.
24. Perbarui FRONTEND_STATUS.md.
25. Lanjutkan milestone berikutnya.

Gunakan siklus:

PLAN → DESIGN → TEST → IMPLEMENT → REVIEW → IMPROVE → VERIFY → REPORT.

Jangan berhenti di tengah milestone hanya untuk melaporkan progress.

Jika sesi terputus, simpan task terakhir agar dapat dilanjutkan.

---

# 42. MANDATORY QUALITY GATES

Gunakan gate berikut:

- G1: Scope isolation.
- G2: Architecture.
- G3: Design system alignment.
- G4: Functional completeness.
- G5: Contract compliance.
- G6: Authentication and RBAC.
- G7: Unit/component/layer tests.
- G8: Integration and N2N.
- G9: Browser E2E.
- G10: Security.
- G11: Accessibility.
- G12: Responsive behavior.
- G13: Performance.
- G14: Visual regression.
- G15: Real API integration.
- G16: UI/UX improvement.
- G17: Final regression and production build.
- G18: Documentation and handoff.

Setiap gate harus menggunakan:

- PASS.
- FAIL.
- BLOCKED.
- NOT_VERIFIED.
- NOT_APPLICABLE dengan justifikasi.

Jangan menganggap BLOCKED atau NOT_VERIFIED sebagai PASS.

---

# 43. FINAL COMMAND VERIFICATION

Gunakan package manager aktual.

Contoh jika menggunakan npm:

```powershell
npm run typecheck
npm run lint
npm run format:check
npm run test
npm run test:coverage
npm run build
npm run test:e2e
```

Gunakan command aktual yang sesuai package.json.

Jika script pengujian belum tersedia, implementasikan script yang diperlukan.

Jalankan dependency vulnerability audit.

Jangan menjalankan automatic major breaking upgrades.

Untuk setiap command, catat:

- Command.
- Exit code.
- Collected.
- Passed.
- Failed.
- Skipped.
- Execution duration.
- Browser.
- Coverage.
- Environment.
- Backend integration mode.

Jangan menuliskan command sebagai bukti jika belum dijalankan.

---

# 44. DOCUMENTATION POLICY — ONLY TWO MASTER OUTPUT FILES

Gunakan hanya dua laporan utama:

1. `frontend/FRONTEND_IMPLEMENTATION_REPORT.md`
2. `frontend/FRONTEND_CHANGELOG.md`

Jika execution plan menetapkan lokasi resmi berbeda, gunakan lokasi tersebut tanpa duplikasi.

Perbarui kedua file secara kumulatif dari FE-M0 sampai FE-M10.

Pertahankan:

- `frontend/AGENTS.md`
- `coordination/FRONTEND_STATUS.md`

FRONTEND_STATUS.md adalah coordination state, bukan laporan tambahan.

Diperbolehkan membuat:

- Source code.
- Test code.
- Generated types.
- Configuration.
- Dependency lockfiles.
- Screenshots.
- Playwright traces.
- Coverage artifacts.
- Machine-readable benchmark outputs.

Jangan membuat file Markdown laporan terpisah untuk setiap milestone.

Jangan membuat:

- FE_M0_REPORT.md.
- FE_M1_REPORT.md.
- UIUX_IMPROVEMENT_REPORT.md.
- SECURITY_REPORT.md.
- PERFORMANCE_REPORT.md.
- ACCESSIBILITY_REPORT.md.
- FINAL_AUDIT.md.

Gabungkan seluruh informasi ke dua laporan utama.

---

# 45. FRONTEND_IMPLEMENTATION_REPORT.md

Gunakan struktur:

1. Metadata.
2. Executive Summary.
3. FE-M0 Preflight Results.
4. Milestone Completion Matrix.
5. Architecture.
6. Technology and Environment.
7. Design System.
8. Pencil Design-to-Code Matrix.
9. Screen Inventory.
10. 25 UI/UX Principles Implementation.
11. Role-Based Feature Matrix.
12. API Integration Matrix.
13. Authentication and Session Security.
14. Functional Verification.
15. Automated Test Results.
16. Coverage.
17. N2N and Cross-Feature Tests.
18. Browser E2E Results.
19. Security Audit.
20. Accessibility Audit.
21. Responsive Audit.
22. Performance Benchmark.
23. UI/UX Improvement Matrix.
24. Before/After Visual Evidence.
25. CodeGraph Utilization.
26. Trail-Code Utilization.
27. Skills Utilization.
28. Backend Integration Evidence.
29. Quality Gates.
30. Known Limitations and Blockers.
31. Final Readiness Decision.

Implementation report harus menggambarkan kondisi terkini.

Jangan mempertahankan spesifikasi lama yang bertentangan dengan implementasi terbaru.

---

# 46. FRONTEND_CHANGELOG.md

Gunakan format kronologis per milestone.

Contoh:

```text
## FE-M9 — UI/UX Improvement & Design Refinement

### Added
### Changed
### Fixed
### UI/UX Improvements
### Accessibility
### Security
### Performance
### Testing
### Contract Alignment
### Files Changed
### Known Issues
```

Untuk perubahan penting, catat:

- Task ID.
- File path.
- Description.
- Reason.
- Affected feature.
- Before/after jika relevan.
- Contract revision.
- Test evidence.
- Regression impact.

Untuk bug:

- Bug ID.
- Root cause.
- Affected files.
- Fix.
- Regression test.
- Final status.

Jangan menyalin seluruh source code ke changelog.

Jangan menduplikasi seluruh implementation report.

Pertahankan histori FE-M0 sampai FE-M10.

---

# 47. FINAL ACCEPTANCE CRITERIA

Frontend hanya boleh dinyatakan selesai apabila:

## Functional

- Seluruh FE-M0 sampai FE-M10 telah dikerjakan sesuai kebutuhan.
- Seluruh 18 screen groups tersedia.
- Seluruh enam dashboard tersedia.
- Seluruh workflow yang disetujui berfungsi.
- Tidak ada placeholder yang diklaim selesai.
- Tidak ada hardcoded operational data.
- Tidak ada fake success.

## Design

- Design tokens konsisten.
- Pencil baseline telah diperiksa.
- Improvement UI/UX telah dilakukan jika diperlukan.
- Anti AI slop diterapkan.
- Responsive behavior terverifikasi.
- Visual hierarchy konsisten.
- Copywriting natural.
- Before/after evidence tersedia untuk perubahan signifikan.

## Contract

- Approved OpenAPI digunakan.
- Generated types valid.
- Seluruh workflow memiliki API consumer.
- Tidak ada field atau endpoint fiktif.

## Security

- Token handling teruji.
- Refresh coordination teruji.
- Permission-aware UI teruji.
- Sensitive cache isolation teruji.
- Private download teruji.
- Tidak ada unresolved critical/high security findings pada frontend scope.

## Accessibility

- Automated checks dijalankan.
- Keyboard navigation diperiksa.
- Focus management benar.
- Contrast diperiksa.
- Reflow diperiksa.
- Keterbatasan manual verification tercatat.

## Testing

- Unit tests.
- Component tests.
- Every-layer tests.
- Feature tests.
- Integration tests.
- N2N tests.
- Contract tests.
- Browser E2E.
- Security tests.
- Accessibility tests.
- Responsive tests.
- Visual regression.
- Performance tests.
- Regression tests.

## Documentation

- Dua laporan master diperbarui.
- FRONTEND_STATUS.md diperbarui.
- Integration handoff tersedia.
- Remaining blockers tercatat.

---

# 48. FINAL READINESS DECISION

Gunakan:

`READY — COMPLETE_FRONTEND_IMPLEMENTED_TESTED_AND_UX_REFINED`

Hanya apabila seluruh mandatory frontend quality gates, termasuk real integration yang diwajibkan, terpenuhi.

Jika frontend telah selesai diimplementasikan tetapi terdapat integration blocker:

`CONDITIONALLY_READY — FRONTEND_COMPLETE_WITH_INTEGRATION_BLOCKERS`

Jika terdapat masalah kritis:

`BLOCKED — CRITICAL_FRONTEND_OR_INTEGRATION_ISSUES`

Jangan mengklaim frontend READY apabila masih terdapat fitur wajib yang belum dibuat atau mandatory test yang belum dijalankan.

Frontend READY tidak otomatis berarti:

- Sistem production-ready.
- Seluruh backend infrastructure lulus.
- UAT telah dilakukan.
- SUS telah dilakukan.
- Efisiensi administrasi terbukti secara empiris.
- Sekolah telah menyetujui sistem.
- WCAG compliance telah disertifikasi.

Integration Track dan Research Evaluation tetap merupakan tahapan terpisah.

---

# 49. FINAL EXECUTION INSTRUCTION

Mulai sekarang.

Kerjakan seluruh Frontend Development Track dari FE-M0 sampai FE-M10.

Jangan berhenti setelah membuat scaffold.

Jangan berhenti setelah membuat dashboard.

Jangan berhenti setelah implementasi fitur utama.

Gunakan:

- Seluruh dokumen proyek.
- Approved OpenAPI.
- DBML.
- RBAC.
- Coordination.
- Pencil MCP.
- Design tokens.
- AI Agent Skills.
- CodeGraph.
- Trail-Code.

Implementasikan frontend React TypeScript yang benar-benar fungsional.

Pertahankan Atomic Design dan arsitektur yang solo developer friendly.

Gunakan desain Pencil sebagai baseline.

Jika hasil Pencil kurang sesuai, Anda diizinkan melakukan improvement UI/UX berdasarkan browser review, prinsip UX, accessibility dan bukti masalah nyata.

Jangan membatasi diri pada desain Pencil apabila desain tersebut menghasilkan usability yang buruk.

Namun, jangan mengubah workflow, hak akses, kontrak, atau design system utama secara sepihak.

Lakukan seluruh pengujian penting pada setiap layer dan setiap feature.

Jika test gagal:

- Investigasi.
- Identifikasi root cause.
- Perbaiki code logic atau test code yang salah.
- Jalankan ulang.
- Lakukan regression verification.

Lanjutkan seluruh pekerjaan independen sampai milestone akhir.

Jika terdapat blocker eksternal, catat secara akurat dan jangan menyembunyikannya.

Gunakan hanya:

- `frontend/FRONTEND_IMPLEMENTATION_REPORT.md`
- `frontend/FRONTEND_CHANGELOG.md`

Untuk seluruh laporan hasil pekerjaan.

Perbarui coordination/FRONTEND_STATUS.md secara berkala.

Tujuan akhir bukan sekadar frontend yang terlihat cantik, melainkan frontend yang profesional, fungsional, mudah digunakan, aman, responsif, performant, teruji, dan siap diintegrasikan.

Kerjakan sampai selesai berdasarkan bukti aktual.
