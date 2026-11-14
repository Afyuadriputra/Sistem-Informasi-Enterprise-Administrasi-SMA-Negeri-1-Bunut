# Frontend Changelog

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

All notable changes to the frontend codebase are documented chronologically in this file.

---

## FE-M0 — Preflight, Design Audit & Verification
*Completed: 13 November 2026*

### Added
- Dependency packages setup in `frontend/package.json` (React 18, Vite 5, Tailwind CSS, TanStack Query, Zustand, Radix UI, Vitest).
- TypeScript strict configuration `tsconfig.json` with path alias `@/*` mapped to `src/*`.
- PostCSS configuration `postcss.config.js` and Tailwind configuration `tailwind.config.ts`.
- Script `generate:api` using `openapi-typescript` pointing to `contracts/openapi.v1.yaml`.
- Generated type definitions file `frontend/src/types/api.generated.ts` containing 2,772 lines strictly derived from OpenAPI v1.1.0.

### Verified
- Validated SHA-256 checksums of `contracts/openapi.v1.yaml`, `contracts/database.dbml`, and `design/tokens.json`.
- Verified 32 visual PNG evidence files in `design/evidence/` across screens S01–S18 and 6 role dashboards.

---

## FE-M1 — Foundation, Tokens & Atomic Components
*Completed: 13 November 2026*

### Added
- CSS Variables in `src/index.css` implementing Institutional Navy (`#173B63`), Teal Accent (`#12665C`), and accessible borders (`#64748B`).
- Utility functions in `src/lib/utils.ts` (`cn`) and `src/lib/formatters.ts` (dates, currencies, numbers, percentages in Indonesian locale).
- Atomic Design Atoms in `src/components/atoms/`:
  - `Button.tsx` (variants: primary, secondary, accent, danger, ghost; size: sm, md, lg; loading spinner support).
  - `Input.tsx` (accessible text, password, date, search input with error styling).
  - `Label.tsx` (Radix UI Label wrapper with required field indicator).
  - `StatusBadge.tsx` (semantic status badges for attendance, cases, requests, academic years).
  - `Spinner.tsx` and `Skeleton.tsx` for loading state representations.
- Atomic Design Molecules in `src/components/molecules/`:
  - `FormField.tsx` (accessible form field combining Label, Input, and Error alert).
  - `SearchBar.tsx` (search input with debounce and clear button).
  - `EmptyState.tsx` (informative empty data visual representation).
  - `ErrorState.tsx` (system and network error display with retry trigger).
  - `PaginationControl.tsx` (accessible page navigation control).
  - `MetricCard.tsx` (kpi metric presentation card with icons and trends).

---

## FE-M2 — Authentication, Shell & Navigation
*Completed: 13 November 2026*

### Added
- Volatile memory token manager and Axios client in `src/lib/api-client.ts`:
  - Memory-only token state (zero leakage to `localStorage`, `sessionStorage`, `document.cookie`).
  - Single-flight refresh token coordination handling concurrent 401s without triggering refresh reuse detection.
  - Automatic `X-Request-ID` header injection.
  - Standardized `ApiErrorEnvelope` normalization.
- Session and authentication store in `src/stores/auth-store.ts` (Zustand):
  - User login, logout, and token purging.
  - Multi-role additive union and active role context switcher.
- Protected Route component `src/components/ProtectedRoute.tsx` with role checking and 403 Forbidden redirection.
- Organism components:
  - `AppSidebar.tsx` (responsive sidebar, role-aware navigation filtering, mobile drawer).
  - `AppHeader.tsx` (institution branding, active role switcher, user profile dropdown, logout trigger).
  - `ConfirmDialog.tsx` (Radix UI Dialog wrapper for destructive action confirmations).
  - `DataTable.tsx` (accessible data table with sortable columns, loading skeleton, and empty states).
- Template layouts:
  - `AppLayout.tsx` (skip-to-content link, sticky header, responsive sidebar, breadcrumbs, Sonner toasts).
  - `AuthLayout.tsx` (50:50 desktop split layout featuring official school identity and motivational mission statement).
- Pages:
  - `src/pages/auth/LoginPage.tsx` (S01: credential login, Zod validation, error banner).
  - `src/pages/profile/ProfilePage.tsx` (S03: user profile details, employee ID, active role context switcher).
  - `src/pages/error/ErrorPages.tsx` (S18: 403 Forbidden, 404 Not Found, 500 Server Error).

---

## FE-M3 — Master Data Management
*Completed: 13 November 2026*

### Added
- `src/pages/accounts/AccountManagementPage.tsx` (S04):
  - User listing, search, role filter.
  - Create user dialog with password confirmation and role assignment.
  - User activation toggle via PATCH `/accounts/users/{id}`.
- `src/pages/students/StudentListPage.tsx` (S05):
  - Comprehensive student database, status filter (AKTIF, LULUS, MUTASI, KELUAR, DO).
  - Create and edit student modal forms.
  - Student detail drawer with enrollment history.
- `src/pages/academic/AcademicMasterPage.tsx` (S06):
  - Tab 1: Siklus Tahun Ajaran (Academic Years) with single active year guarantee via PATCH.
  - Tab 2: Rombongan Belajar (Classes) with grade level and academic year linking.
  - Tab 3: Data Pegawai Sekolah (Employees) with NIP and phone numbers.
- `src/pages/assignments/AssignmentsPage.tsx` (S07):
  - Tab 1: Penempatan Rombel Siswa (Student Enrollments) with start/end date bounds.
  - Tab 2: Penugasan Guru & Wali Kelas (Teacher Assignments) with role tags (`GURU_MAPEL`, `WALI_KELAS`).

---

## FE-M4 — Attendance Management
*Completed: 13 November 2026*

### Added
- `src/pages/attendance/RecordAttendancePage.tsx` (S08):
  - Class selector restricted to authorized teaching/homeroom assignments.
  - Attendance date picker with bounds up to current date.
  - Daily roster fetch via GET `/attendance/roster`.
  - Color-coded H/S/I/A status radio buttons per student.
  - Real-time live percentage summary counter.
  - "Tandai Semua Hadir" quick-fill action.
  - Atomic bulk save via POST `/attendance/bulk`.
- `src/pages/attendance/AttendanceRecapPage.tsx` (S09):
  - Class and date range filters (defaults to current month).
  - Aggregated attendance table with status counts.
  - Official Excel export trigger via GET `/reports/attendance.xlsx` with authorized blob download.

---

## FE-M5 — Student Affairs & Counseling
*Completed: 13 November 2026*

### Added
- `src/pages/cases/CaseListPage.tsx` (S10):
  - Counseling case listing, status filter (`BARU`, `DIPROSES`, `SELESAI`, `DIBATALKAN`).
  - Search by case number or student name.
  - New case referral modal for Teachers, Homeroom, and Counselors.
- `src/pages/cases/CaseDetailPage.tsx` (S11):
  - 62:38 Golden Ratio adaptive two-column split layout.
  - Chronological action event timeline.
  - State machine workflow transitions: `MULAI_PENANGANAN`, `CATAT_TINDAKAN`, `SELESAIKAN`, `BATALKAN`.
  - Optimistic concurrency control sending `expected_version` with 409 conflict handling.
  - Preservation of DEC-TECH-18 counseling note privacy masking (`[Dirahasiakan oleh Konselor/Kesiswaan]`).

---

## FE-M6 — Administration & Private Documents
*Completed: 13 November 2026*

### Added
- `src/pages/administration/RequestListPage.tsx` (S12):
  - Operational letter service request queue with status filters.
- `src/pages/administration/NewRequestPage.tsx` (S13):
  - Service type selection, student ID, applicant name, purpose.
  - Multipart document attachment uploader with 5 MB size limit and extension checking.
- `src/pages/administration/RequestDetailPage.tsx` (S14):
  - Detailed request review, document attachments list with authorized blob download.
  - Transition workflow: `PROSES`, `AJUKAN_PERSETUJUAN`, `SELESAIKAN`.
  - Optimistic locking via `expected_version`.
- `src/pages/administration/ApprovalsQueuePage.tsx` (S14-P):
  - Pimpinan approval queue for Principal disposition (`SETUJUI`, `TOLAK`).
- `src/pages/administration/DocumentArchivePage.tsx` (S15):
  - Digital document archive catalog with search, metadata, and secure download.

---

## FE-M7 — Dashboards, Reports & Audit
*Completed: 13 November 2026*

### Added
- `src/pages/dashboard/DashboardPage.tsx` (S02):
  - Adaptive role metrics for Administrator, Guru, Wali Kelas, Kesiswaan, Tata Usaha, Pimpinan.
  - 4 primary metric cards consuming GET `/reports/dashboard`.
  - Quick action shortcuts mapped to role duties.
- `src/pages/reports/ReportsPage.tsx` (S16):
  - Attendance spreadsheet report export trigger (Excel `.xlsx`).
  - Administration document report export trigger (PDF `.pdf`).
- `src/pages/audit/AuditLogsPage.tsx` (S17):
  - Administrator audit trail table displaying timestamp, actor, action, resource, IP address, and Request ID.

---

## FE-M8 — Security, Accessibility & Testing
*Completed: 13 November 2026*

### Testing
- Created 13 test files with 58 automated tests in `frontend/tests/`:
  - `tests/unit/formatters.test.ts` (5 tests)
  - `tests/unit/api-client.test.ts` (3 tests)
  - `tests/unit/auth-store.test.ts` (3 tests)
  - `tests/components/atoms.test.tsx` (8 tests)
  - `tests/components/molecules.test.tsx` (6 tests)
  - `tests/components/organisms.test.tsx` (6 tests)
  - `tests/security/token-storage.test.ts` (3 tests)
  - `tests/accessibility/wcag.test.tsx` (4 tests)
  - `tests/features/auth.test.tsx` (3 tests)
  - `tests/features/attendance.test.tsx` (2 tests)
  - `tests/features/cases.test.tsx` (2 tests)
  - `tests/features/administration.test.tsx` (4 tests)
  - `tests/features/pages-coverage.test.tsx` (9 tests)
- **Result:** 100% tests passing (58 PASS, 0 FAIL).

### Security
- Verified zero token exposure across `localStorage`, `sessionStorage`, and `document.cookie`.
- Validated memory-only token wipe on logout.

### Accessibility
- Ran automated WCAG 2.1 AA audits with `axe-core`, reporting 0 accessibility violations.
- Implemented visible 2px blue focus rings on interactive elements.

---

## FE-M9 — UI/UX Improvement & Design Refinement
*Completed: 13 November 2026*

### UI/UX Improvements
- Upgraded border color contrast to `#64748B` across card panels and tables for enhanced readability.
- Added live percentage counter badges to daily class attendance recording.
- Implemented human-readable optimistic concurrency conflict banners (HTTP 409) with one-click data reload.
- Styled DEC-TECH-18 privacy notes with subtle amber containers and italic typography to signify confidential records.
- Configured Rollup `manualChunks` in `vite.config.ts` splitting vendors (`vendor-react`, `vendor-query`, `vendor-ui`), eliminating bundle size warnings.

---

## FE-M10 — Final Regression & Integration Readiness
*Completed: 13 November 2026*

### Verification
- Executed `npm run typecheck` (`tsc --noEmit`): **Exit Code 0 (0 errors)**.
- Executed `npm run build`: **Exit Code 0 in 9.19s**.
- Executed `npm run format:check`: **Exit Code 0 (All files conform to Prettier standard)**.
- Executed `npm run test`: **58 tests PASS (100%)**.
- Completed Master Implementation Report `frontend/FRONTEND_IMPLEMENTATION_REPORT.md` and updated `coordination/FRONTEND_STATUS.md`.
- Final status declared: `CONDITIONALLY_READY — FRONTEND_COMPLETE_WITH_INTEGRATION_BLOCKERS`.

---

## FE-M10.1 — Independent Frontend Verification, Contract Alignment, Browser Testing & UI/UX Closure
*Completed: 14 November 2026*

### Added & Updated
- **OpenAPI v1.1.0 Full Contract Alignment:**
  - Audited all 49 operations in `contracts/openapi.v1.yaml` with consistent camelCase `operationId`.
  - Added modal detail akun pengguna pada `AccountManagementPage.tsx` yang mengonsumsi `getUserDetail` (`GET /accounts/users/{id}`).
  - Added alur end-dating penempatan rombel pada `AssignmentsPage.tsx` yang mengonsumsi `updateEnrollment` (`PATCH /master/enrollments/{id}`).
  - Added alur end-dating penugasan guru pada `AssignmentsPage.tsx` yang mengonsumsi `updateClassAssignment` (`PATCH /master/assignments/{id}`).
  - Added tab katalog jenis layanan administrasi pada `AcademicMasterPage.tsx` untuk Administrator mengonsumsi `listServiceTypes` (`GET /administration/service-types`), `createServiceType` (`POST /administration/service-types`), dan `updateServiceType` (`PATCH /administration/service-types/{id}`).
  - Corrected enum status siswa pada `StudentListPage.tsx` dan `StatusBadge.tsx` menjadi `['AKTIF', 'MUTASI_KELUAR', 'LULUS', 'NONAKTIF']`.
  - Verified operasi pembaruan data siswa menggunakan metode HTTP `PATCH /master/students/{id}` (`updateStudent`).
- **Partial Failure Handling:**
  - Added penanganan kegagalan parsial pada `NewRequestPage.tsx` di mana jika berkas lampiran gagal diunggah setelah permohonan surat berhasil dibuat, sistem mencegah pembuatan surat ganda dan menyediakan tombol coba unggah ulang pada ID permohonan yang sama.
- **Session Security & Safe Retry Policy:**
  - Added fungsi `isIdempotentRequest` pada `src/lib/api-client.ts`. Permintaan idempoten (GET, HEAD, OPTIONS, PUT, DELETE) diulang otomatis setelah refresh token; permintaan mutasi non-idempoten (POST) diblokir dari replay otomatis dengan kode `NON_IDEMPOTENT_MUTATION_ABORTED`.
  - Added pembersihan antrean request (`failedQueue`) pada `clearAuthTokens()` saat logout untuk mencegah race conditions.
- **Contract & Security Automated Tests:**
  - Created `tests/contract/contract-alignment.test.ts` (7 tests) memverifikasi 49 operasi, penamaan camelCase, enum status siswa, dan skema request/response.
  - Created `tests/security/safe-retry.test.ts` (5 tests) memverifikasi safe retry policy, penolakan otomatis mutasi non-idempoten, dan isolasi memori token.
  - Added pengujian aksesibilitas `axe-core` pada `LoginPage` di `tests/accessibility/wcag.test.tsx` (5 tests, 0 pelanggaran).
- **Playwright E2E Browser Testing:**
  - Installed `@playwright/test` dan browser Chromium headless.
  - Configured proxy Vite dev server (`http://localhost:3000/api` -> `http://127.0.0.1:8000/api`).
  - Created `tests/e2e/auth-and-roles.spec.ts` menguji login dan navigasi 6 peran pengguna nyata: Administrator, Guru, Wali Kelas, Kesiswaan, Tata Usaha, Pimpinan.
  - Generated 8 tangkapan layar bukti visual di `frontend/evidence/` (`e2e-01-admin-dashboard.png` s/d `e2e-08-kepsek-approvals.png`).

### Verification Results
- Vitest Automated Tests: **15 Test Files, 71 Tests PASS (100% Lulus, 0 Gagal)**.
- Playwright E2E Browser Tests: **6 Tests PASS (8.1s)**.
- TypeScript Compilation (`tsc --noEmit`): **Exit Code 0 (0 errors)**.
- Production Build (`vite build`): **Exit Code 0 dalam 7.71s**.
- Prettier Code Standard (`prettier --check`): **Exit Code 0 (Clean)**.
- Final Status Declared: **`READY — FRONTEND_VERIFIED_UX_REFINED_AND_READY_FOR_INTEGRATION`**.

---

## FE-M10.2 - Centralized API Configuration & Environment Hardening (INT-M8.1 Addendum)
*Completed: 14 November 2026*

### Added & Updated
- **Pemusatan Konfigurasi Environment & Sanitasi URL API:**
  - Exported fungsi sentral `resolveApiBaseUrl(raw?: string)` pada `frontend/src/lib/api-client.ts`:
    - Normalisasi trailing slash (menghapus tanda slash di akhir URL).
    - Memastikan path `/api` tersemat secara otomatis pada URL origin root absolut (misal `http://localhost:8000` menjadi `http://localhost:8000/api`).
    - Fallback aman ke `/api` default saat variabel environment tidak didefinisikan atau kosong.
  - Ditambahkan interceptor request pada `api-client.ts` yang mendeteksi dan memangkas prefix duplikat `/api` (jika `config.url` berawalan `/api/` dan `baseURL` berakhiran `/api`), mencegah timbulnya kesalahan HTTP 404 `/api/api/...`.
  - Diperbarui `frontend/vite.config.ts` untuk memuat variabel `BACKEND_PROXY_TARGET` melalui `loadEnv(mode, process.cwd(), '')` hanya pada level dev server Node.js, menjaga isolasi kredensial server-side dari JavaScript bundle browser.
  - Diperbarui `frontend/playwright.config.ts` agar mendukung variabel lingkungan dinamis `PLAYWRIGHT_BASE_URL` dengan fallback default ke `http://localhost:3000`.
  - Dibuat template konfigurasi environment:
    - `frontend/.env`: Konfigurasi pengembang lokal default (`VITE_API_BASE_URL=/api`, `BACKEND_PROXY_TARGET=http://127.0.0.1:8000`).
    - `frontend/.env.example`: Template publik dengan panduan konfigurasi dev dan reverse proxy.
    - `frontend/.env.production.example`: Template publik untuk deployment produksi.

- **Penguatan Pengujian Otomatis & Proteksi Secret (3 pengujian baru, total 74 pengujian Vitest):**
  - Ekspansi berkas uji `frontend/tests/unit/api-client.test.ts` dari 3 menjadi 6 pengujian:
    - Pengujian resolusi dan normalisasi `resolveApiBaseUrl` dengan input undefined, kosong, relative path, dan absolute URL.
    - Pengujian pencegahan prefix duplikat `/api` pada request interceptor Axios.
    - Pengujian pencegahan kebocoran secret backend: memverifikasi bahwa tidak ada variabel sensitif backend (`DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, atau kredensial proxy) yang bocor ke dalam `import.meta.env` client bundle.

### Verification Results
- Vitest Automated Tests: **15 Test Files, 74 Tests PASS (100% Lulus, 0 Gagal)**.
- Playwright E2E Browser Tests: **6 Tests PASS (13.9s)**.
- TypeScript Compilation (`tsc --noEmit`): **Exit Code 0 (0 errors)**.
- Production Build (`vite build`): **Exit Code 0 dalam 9.00s**.
- Final Status Declared: **`READY — FRONTEND_VERIFIED_UX_REFINED_AND_READY_FOR_INTEGRATION`**.
