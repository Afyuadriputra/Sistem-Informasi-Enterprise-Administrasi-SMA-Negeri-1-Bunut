# Frontend Execution Plan

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | APPROVED EXECUTION BASELINE |
| Terakhir Diperbarui | 12 November 2026 |
| Target Arsitektur | React 18+, TypeScript (Strict), Vite, Tailwind CSS, shadcn/ui, Radix Primitives, TanStack Query, Zustand |
| Acuan | UID §1-15, PRD §1-11, AFD §1-10, contracts/openapi.v1.yaml |

---

## 1. Prinsip Eksekusi Frontend

1. **Pengembangan Mandiri Berbasis Kontrak (Contract-Bound):** Frontend Agent dapat membangun seluruh tampilan antarmuka dan interaksi pengguna tanpa menunggu backend selesai, dipandu oleh kontrak `contracts/openapi.v1.yaml`.
2. **Kepatuhan Mutlak terhadap UID.md:**
   - Desain visual mengikuti tema **Institutional Navy & Teal** (Permukaan `#FFFFFF`, Latar `#F5F7FA`, Primary `#173B63`, Accent `#12665C`).
   - Menerapkan 25 hukum dan prinsip UX (Hick's Law, Fitts's Law, Doherty Threshold, Peak-End Rule, dll.).
   - Menerapkan pembagian komposisi Golden Ratio adaptif (62% panel utama : 38% panel pendukung pada layar desktop).
   - Tipografi menggunakan font Inter dengan tabular numerals pada kolom angka dan tabel.
   - Menghormati standar anti-AI slop: tidak ada tombol ornamen tanpa fungsi, tidak ada card di dalam card, tidak ada grafik 3D yang tidak informatif, tidak ada bahasa jargon mesin.
3. **Standar Aksesibilitas WCAG 2.2 Level AA:**
   - Target sentuh kontrol utama minimal 44x44 px pada mode sentuh.
   - Rasio kontras teks minimal 4,5:1 (teks biasa) dan 3:1 (non-teks/fokus).
   - Navigasi keyboard penuh (`Tab`, `Shift+Tab`, `Enter`, `Escape`) dengan fokus visual yang jelas.
4. **Kelengkapan State Tampilan:** Setiap komponen data wajib memiliki 5 penanganan state: *Loading (Skeleton)*, *Refreshing*, *Empty*, *Success*, dan *Error (Safe message + request ID)*.
5. **Kebijakan Mocking:** Mocking hanya diperbolehkan pada lingkungan development/testing terisolasi berbasis kontrak OpenAPI. **Dilarang keras menyertakan kode mock API pada build produksi operasional.**

---

## 2. Rincian Milestone Pengerjaan Frontend (FE-M1 s/d FE-M8)

### FE-M1: Project Foundation, Design Tokens & Atomic Primitives
- **Tujuan:** Menginisialisasi proyek React Vite TypeScript, konfigurasi Tailwind CSS dengan token Institutional Navy & Teal, pemasangan primitive shadcn/Radix, dan setup generator tipe OpenAPI.
- **Task ID:** `FE-TASK-01`
- **Dependency:** Inisialisasi M0 selesai.
- **OpenAPI Dependency:** `contracts/openapi.v1.yaml`.
- **Allowed Paths:** `frontend/src/{app,components/atoms,lib,styles,types}/**`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tailwind.config.js`.
- **Forbidden Paths:** `frontend/src/features/**`, `backend/**`.
- **Screen ID:** S01-S18 (Komponen Fondasi).
- **Atomic Design Inventory:**
  - Atoms: `Button`, `Input`, `Label`, `Badge`, `Checkbox`, `Radio`, `Spinner`, `Icon` (Lucide Icons).
- **States:** Hover, Active, Focus-visible ring (`#1D4ED8`), Disabled (`cursor: not-allowed`).
- **Responsive & A11y:** Viewport meta dikonfigurasi; skip link terpasang; target ukuran tombol minimal 40 px desktop / 44 px mobile.
- **Testing:** Vitest pengujian rendering button varian; pemeriksaan lint ESLint bersih; typecheck `tsc --noEmit` lulus.
- **Definition of Done:** Project Vite berjalan; palet token CSS variable terdaftar; generasi tipe dari OpenAPI berhasil (`npm run generate:types`).

---

### FE-M2: Authentication UI & Application Shell Layout
- **Tujuan:** Membangun halaman login (S01), penanganan token sesi di memory/storage, layout shell aplikasi (Sidebar navigasi desktop, Drawer mobile, Header profil), dan rute terproteksi.
- **Task ID:** `FE-TASK-02`
- **Dependency:** `FE-M1`.
- **OpenAPI Dependency:** `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`.
- **Allowed Paths:** `frontend/src/pages/auth/**`, `frontend/src/features/accounts/**`, `frontend/src/components/{molecules,organisms,templates}/**`, `frontend/src/stores/**`.
- **Forbidden Paths:** `frontend/src/features/{master_data,attendance,student_affairs,administration,reports}/**`, `backend/**`.
- **Screen ID:** `S01 Login`, `S03 Profil / Ganti Konteks`, `S18 Error State`.
- **User Role:** Seluruh peran (Administrator, Guru, Wali Kelas, Kesiswaan, TU, Pimpinan).
- **User Journey:** Pengguna memasukkan username & kata sandi -> Sistem menampilkan spinner loading -> Berhasil login mengarahkan ke dashboard -> Header menampilkan nama & penugasan peran -> Tombol logout mengakhiri sesi.
- **Atomic Design Inventory:**
  - Molecules: `FormField`, `PasswordInput`, `UserMenuDropdown`, `NotificationToast`.
  - Organisms: `AppSidebar`, `AppHeader`, `MobileNavDrawer`.
  - Templates: `AuthLayout` (split panel bersih), `AppLayout` (sidebar responsif).
- **States:**
  - S01: Form login normal, validasi lokal, loading saat submit, pesan error generik saat kredensial salah, pesan 429 saat rate limit terlampaui.
- **Responsive & A11y:**
  - Layar >= 1280 px: Sidebar tetap (240 px).
  - Layar < 768 px: Drawer navigasi hamburger; form login satu kolom terpusat.
  - Dukungan penuh password manager dan autofill.
- **Testing:** Uji form login validasi submit; pengujian route guard (pengguna belum login diarahkan ke `/login`).
- **Definition of Done:** Halaman login S01 dan shell navigasi responsif selesai; logout membersihkan seluruh cache sesi.

---

### FE-M3: Master Data Management UI
- **Tujuan:** Membangun antarmuka pengelolaan data master siswa (S05), referensi tahun ajaran/kelas/pegawai (S06), dan penempatan/penugasan (S07).
- **Task ID:** `FE-TASK-03`
- **Dependency:** `FE-M2`.
- **OpenAPI Dependency:** `GET/POST/PATCH /api/master/*`.
- **Allowed Paths:** `frontend/src/features/master_data/**`, `frontend/src/pages/master/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** `S04 Pengguna & Peran`, `S05 Master Siswa`, `S06 Master Referensi`, `S07 Penempatan & Penugasan`.
- **User Role:** Administrator, Tata Usaha (sesuai kewenangan).
- **Atomic Design Inventory:**
  - Molecules: `SearchField`, `FilterChipGroup`, `PaginationControl`, `StatusBadge`.
  - Organisms: `DataTable` (server-side sorting/pagination), `StudentDetailModal`, `EnrollmentFormDialog`.
  - Templates: `ListPageLayout`.
- **States:**
  - Loading: Skeleton table baris berkedip lembut.
  - Empty: Tampilan "Belum ada data siswa" disertai tombol aksi buat jika berwenang.
  - Error: Pesan aman dan tombol "Muat Ulang".
- **Responsive & A11y:** Tabel mendukung scroll horizontal lokal tanpa merusak layout induk; kolom nama dan NIS tetap terlihat (*sticky* bila diperlukan).
- **Testing:** Pengujian filter pencarian siswa; validasi form tambah siswa via Zod schema.
- **Definition of Done:** Layar S04, S05, S06, dan S07 selesai; paginasi dan filter pencarian berfungsi mulus.

---

### FE-M4: Attendance Recording & Class Recap UI
- **Tujuan:** Membangun antarmuka pencatatan kehadiran kelas harian massal (S08) dan rekapitulasi kehadiran kelas/siswa (S09).
- **Task ID:** `FE-TASK-04`
- **Dependency:** `FE-M2`.
- **OpenAPI Dependency:** `GET /api/attendance/roster`, `POST /api/attendance/bulk`, `GET /api/attendance`.
- **Allowed Paths:** `frontend/src/features/attendance/**`, `frontend/src/pages/attendance/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** `S08 Catat Kehadiran`, `S09 Rekap Kehadiran`.
- **User Role:** Guru Mata Pelajaran, Wali Kelas, Kesiswaan, Pimpinan.
- **User Journey:** Guru memilih kelas dan tanggal -> Roster siswa termuat -> Guru mengisi radio button status (Hadir, Sakit, Izin, Alpa) per siswa -> Tombol Simpan Kehadiran divalidasi -> Konfirmasi sukses muncul tanpa refresh penuh.
- **Atomic Design Inventory:**
  - Molecules: `AttendanceStatusSelector` (H/S/I/A radio group yang aksesibel), `AttendanceCounterBar` (menghitung jumlah siswa terisi secara real-time).
  - Organisms: `AttendanceEditorTable`, `RecapSummaryCard`, `ClassRecapTable`.
- **States:**
  - S08: Indikator progress pengisian (Goal-Gradient Effect), penandaan baris error jika ada catatan yang belum lengkap, konfirmasi saat ingin berpindah halaman sebelum simpan (*dirty form warning*).
  - S09: Rekapitulasi persentase kehadiran dan penandaan siswa yang memerlukan perhatian.
- **Responsive & A11y:** Tombol status kehadiran memiliki target sentuh nyaman (44x44 px); navigasi naik/turun baris siswa dapat menggunakan tombol keyboard.
- **Testing:** Test pengisian form absensi massal; penolakan submit saat ada baris yang belum dipilih; kalkulasi rekap angka.
- **Definition of Done:** Form absensi massal S08 dan rekap S09 berfungsi intuitif, cepat (<100 ms feedback interaksi), dan tervalidasi.

---

### FE-M5: Student Affairs & Case Timeline UI
- **Tujuan:** Membangun antarmuka antrean kasus kesiswaan (S10), detail kronologis tindakan (S11), dan form transisi status penanganan.
- **Task ID:** `FE-TASK-05`
- **Dependency:** `FE-M2`.
- **OpenAPI Dependency:** `GET/POST /api/student-affairs/cases*`.
- **Allowed Paths:** `frontend/src/features/student_affairs/**`, `frontend/src/pages/student_affairs/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** `S10 Daftar Kasus`, `S11 Detail Kasus & Timeline`.
- **User Role:** Petugas Kesiswaan, Wali Kelas.
- **Atomic Design Inventory:**
  - Molecules: `CaseStatusBadge`, `ActionTransitionDialog`.
  - Organisms: `CaseTimeline` (urutan peristiwa kronologis dengan nama aktor dan waktu), `CaseFormModal`.
  - Templates: `DetailPageLayout` (pembagian Golden Ratio 62% detail kasus : 38% timeline tindakan).
- **States:**
  - S11: Status BARU, DIPROSES, SELESAI. Penanganan konflik HTTP 409 jika versi data telah berubah oleh staf lain.
- **Responsive & A11y:** Timeline menggunakan konektor visual dan teks deskriptif; tidak bergantung hanya pada warna status.
- **Testing:** Pengujian dialog transisi status; validasi catatan wajib penanganan kasus.
- **Definition of Done:** S10 dan S11 selesai; riwayat tindakan tampil berurutan; penanganan HTTP 409 teruji.

---

### FE-M6: Administration, Approval & Private Archive UI
- **Tujuan:** Membangun antarmuka antrean permohonan persuratan (S12), form permohonan dengan upload berkas (S13), detail dan tindakan persetujuan pimpinan (S14), serta arsip dokumen privat (S15).
- **Task ID:** `FE-TASK-06`
- **Dependency:** `FE-M2`.
- **OpenAPI Dependency:** `GET/POST /api/administration/*`.
- **Allowed Paths:** `frontend/src/features/administration/**`, `frontend/src/pages/administration/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** `S12 Daftar Layanan`, `S13 Buat Permohonan`, `S14 Detail Layanan & Persetujuan`, `S15 Arsip Dokumen`.
- **User Role:** Tata Usaha, Pimpinan.
- **Atomic Design Inventory:**
  - Molecules: `FileUploadDropzone`, `ApprovalActionBar`, `DocumentPreviewRow`.
  - Organisms: `ServiceRequestTable`, `ServiceTimeline`, `DocumentArchiveTable`.
- **States:**
  - S13: Progress upload berkas, error validasi format/ukuran (>5MB), tombol batal.
  - S14: Tombol Setujui dan Tolak (dengan alasan wajib) khusus bagi peran Pimpinan.
- **Responsive & A11y:** Input file dapat diakses keyboard; error validasi berkas diumumkan pembaca layar.
- **Testing:** Pengujian alur pengajuan surat; validasi unggah berkas; dialog persetujuan pimpinan.
- **Definition of Done:** S12, S13, S14, dan S15 selesai; unduh berkas privat melalui endpoint terproteksi berfungsi.

---

### FE-M7: Dashboard, Visualizations & Reporting UI
- **Tujuan:** Membangun dashboard utama teragregasi per peran (S02), filter laporan terpadu, dan pemicu ekspor berkas Excel/PDF (S16).
- **Task ID:** `FE-TASK-07`
- **Dependency:** `FE-M4`, `FE-M5`, `FE-M6`.
- **OpenAPI Dependency:** `GET /api/reports/*`, `GET /api/audit-logs`.
- **Allowed Paths:** `frontend/src/features/reports/**`, `frontend/src/pages/reports/**`, `frontend/src/pages/dashboard/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** `S02 Dashboard Multi-Peran`, `S16 Laporan & Ekspor`, `S17 Audit Trail`.
- **User Role:** Seluruh peran (tampilan widget disesuaikan secara dinamis).
- **Atomic Design Inventory:**
  - Molecules: `MetricCard`, `DateRangeFilterPicker`, `ExportButtonDropdown`.
  - Organisms: `AttendanceBarChart` (Recharts sederhana tanpa dekorasi berlebih), `RecentActivityList`.
  - Templates: `DashboardLayout` (Desktop 62% metrik rekap : 38% antrean tugas).
- **States:**
  - S02: Loading skeleton widget; grafik dengan legenda jelas dan alternatif tabel angka.
- **Responsive & A11y:** Layout dashboard beralih menjadi satu kolom pada layar sempit; grafik memiliki atribut aksesibel dan ringkasan tekstual.
- **Testing:** Pengujian filter rentang tanggal; pengujian pemicuan unduh berkas ekspor.
- **Definition of Done:** S02 dan S16 berfungsi responsif; widget metrik terfilter tepat sesuai peran pengguna login.

---

### FE-M8: Accessibility, Usability Audit & Visual Hardening
- **Tujuan:** Audit aksesibilitas WCAG 2.2 AA (menggunakan axe-core), peninjauan anti-AI slop menyeluruh, verifikasi responsivitas pada 8 breakpoint layar, dan audit performa client bundle.
- **Task ID:** `FE-TASK-08`
- **Dependency:** `FE-M7`.
- **OpenAPI Dependency:** Seluruh kontrak OpenAPI v1.
- **Allowed Paths:** `frontend/**`.
- **Forbidden Paths:** `backend/**`.
- **Screen ID:** S01-S18 (Seluruh Layar).
- **Quality Checks:**
  - Uji kontras warna seluruh elemen teks dan kontrol pada permukaan putih dan abu-abu.
  - Uji navigasi keyboard murni dari awal hingga akhir tanpa menyentuh mouse.
  - Verifikasi breakpoint: 320px, 375px, 390px, 768px, 1024px, 1280px, 1440px, 1920px.
  - Tidak ada teks yang terpotong atau horizontal overflow.
  - Produksi build bersih (`npm run build`), tidak menyisakan mock atau variabel debug.
- **Testing:** Pengujian a11y otomatis; verifikasi visual manual.
- **Definition of Done:** Seluruh screen S01-S18 lulus Quality Gate Frontend; build produksi sukses.
