# Frontend Agent Guidelines & UI/UX Standards

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Peran Agent | Frontend Agent |
| Cakupan Writable | `frontend/**`, `coordination/FRONTEND_STATUS.md` |
| Cakupan Read-Only | `backend/**`, `design/**`, `contracts/**`, `docs/**` |
| Acuan Utama | UID.md, PRD.md, AFD.md, contracts/openapi.v1.yaml |

---

## 1. Tanggung Jawab Utama Frontend Agent

1. Membangun antarmuka web SPA responsif menggunakan React 18+, TypeScript (strict mode), Vite, Tailwind CSS, dan shadcn/ui.
2. Memulai fondasi aplikasi, routing, client state, dan form validasi Zod secara mandiri berdasarkan kontrak OpenAPI tanpa menunggu backend selesai. Finalisasi visual antarmuka diselaraskan dengan hasil sign-off desain dari Pencil Track (`design/**`).
3. Mengimplementasikan 18 rancangan screen (S01 s/d S18) sesuai spesifikasi persis pada UID.md dan artefak desain Pencil.
4. Menghasilkan dan memelihara tipe TypeScript otomatis dari kontrak API melalui `openapi-typescript`.
5. Mengelola server state menggunakan TanStack Query (caching, deduplication, invalidasi pasca mutasi) dan client state lokal menggunakan Zustand.
6. Menerapkan validasi form yang ketat menggunakan React Hook Form dan Zod schemas.
7. Memastikan antarmuka memenuhi standar aksesibilitas WCAG 2.2 Level AA.
8. Menulis pengujian komponen menggunakan Vitest dan React Testing Library.

---

## 2. Standar Desain Visual & Anti-AI Slop (Mandatory)

1. **Palet Warna Institusional (Institutional Navy & Teal):**
   - Latar workspace lembut: `#F5F7FA` (`--background`)
   - Permukaan kartu/tabel: `#FFFFFF` (`--surface`)
   - Teks utama: `#172B42` (`--foreground`)
   - Teks sekunder/label: `#475569` (`--muted-foreground`)
   - Brand utama/tombol primer: `#173B63` (`--primary`), Hover: `#102D4D`
   - Aksen data/penekanan: `#12665C` (`--accent`)
   - Batas kontrol input: `#64748B` (`--input-border`)
   - Fokus keyboard aksesibel: `#1D4ED8` (`--focus-ring`)
2. **Prinsip Golden Ratio Adaptif:**
   - Pada layar desktop, gunakan proporsi ~62% panel konten utama dan ~38% panel pendukung (misal pada dashboard pimpinan S02 dan detail kasus S11).
3. **Standar Anti-AI Slop:**
   - Dilarang membuat tombol atau tautan yang tidak berfungsi (*no dead controls*).
   - Dilarang membuat card di dalam card atau membuat seluruh panel melayang (*no excessive floating cards*).
   - Dilarang menggunakan gradien neon, efek kaca (*glassmorphism*) berlebihan, atau grafik 3D dekoratif yang tidak menjawab kebutuhan data pengguna.
   - Microcopy antarmuka menggunakan Bahasa Indonesia yang ringkas, formal, dan familiar bagi guru/staf sekolah (misal: "Simpan Kehadiran", "Tahun Ajaran", "Permohonan Layanan").
   - Dilarang memasukkan jargon teknis mesin seperti "CRUD", "endpoint", "payload", "UUID", "mock", atau "simulasi" ke antarmuka operasional pengguna.

---

## 3. Standar Aksesibilitas (WCAG 2.2 AA) & Responsivitas

1. **Ukuran Target Sentuh (Target Size Minimum):**
   - Tombol utama dan kontrol form wajib memiliki ukuran target sentuh minimal 44x44 px pada mode mobile/touch.
2. **Navigasi Keyboard Penuh:**
   - Seluruh interaksi form, tabel absensi, dialog konfirmasi, dan menu dropdown wajib dapat dioperasikan penuh menggunakan keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`).
   - Indikator fokus (`focus-visible`) wajib terlihat jelas dan tidak boleh dihilangkan dengan `outline: none` tanpa pengganti.
3. **Lima State Tampilan Data (Five UI States):**
   - Setiap halaman dan tabel wajib menangani:
     - `Initial Loading`: Skeleton table / layout yang berkedip lembut.
     - `Refreshing`: Indikator pembaruan data tanpa merusak tata letak.
     - `Empty State`: Ilustrasi/pesan deskriptif saat data belum tersedia.
     - `Success Feedback`: Notifikasi toast singkat (Sonner) atau pesan inline.
     - `Error State`: Pesan aman berbahasa Indonesia disertai tombol coba lagi dan request ID jika disediakan backend.
4. **Kebijakan Mocking:**
   - Penggunaan mock service/fixture hanya diperbolehkan pada lingkungan development/testing terisolasi.
   - **Dilarang keras membiarkan mock API aktif pada build produksi operasional.**

---

## 4. Struktur Arsitektur Atomic Design

Letakkan komponen sesuai tingkatannya:
```text
frontend/src/
  components/
    atoms/       # Button, Input, Label, Badge, Checkbox, Spinner, Icon
    molecules/   # FormField, SearchField, FilterChip, StatusBadge, Pagination
    organisms/   # DataTable, AttendanceEditorTable, CaseTimeline, AppSidebar
    templates/   # AuthLayout, AppLayout, ListPageLayout, DetailPageLayout
  features/      # Slice per domain (api hooks TanStack Query, Zod schemas, state)
  pages/         # Komposisi rute halaman S01 s/d S18
```

---

## 5. Protokol Pelaporan Status

Setelah menyelesaikan pekerjaan atau sebelum sesi berakhir:
- Perbarui progress pada berkas `coordination/FRONTEND_STATUS.md`.
- Cantumkan: Milestone yang dikerjakan, langkah terakhir yang tuntas, bukti pengujian (Vitest output/build check), dan langkah berikutnya.
- **Dilarang memodifikasi file di luar `frontend/**` dan `coordination/FRONTEND_STATUS.md`.**
