# UI/UX Design Execution Plan (Pencil MCP Track)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | APPROVED EXECUTION BASELINE |
| Terakhir Diperbarui | 12 November 2026 |
| Target Alat | Pencil MCP (`pen.dev`), Kanvas Desain Terenkripsi, Visual Design Tokens |
| Acuan | UID §1-15, PRD §1-11, AFD §1-10, contracts/openapi.v1.yaml |
| Pengelola | UI/UX Design Agent / Integration Lead |

---

## 1. Prinsip Eksekusi Jalur Desain (Pencil Design Track)

1. **Jalur Produksi Independen:** UI/UX Design Track beroperasi penuh secara mandiri tanpa menunggu ketersediaan kode backend maupun implementasi frontend.
2. **Pencil MCP sebagai Single Source of Truth:** Seluruh wireframe, screen layout, mock visual, dan interaksi dirancang serta dikelola menggunakan **Pencil MCP** (`pen.dev`). Berkas desain disimpan pada direktori `design/**`.
3. **Kepatuhan Desain Anti-AI Slop:**
   - Palet warna wajib mematuhi tema **Institutional Navy & Teal** (Permukaan `#FFFFFF`, Latar `#F5F7FA`, Primary `#173B63`, Accent `#12665C`).
   - Menerapkan 25 hukum dan prinsip UX (Hick's Law, Fitts's Law, Golden Ratio 62%:38%, Jakob's Law, Peak-End Rule, dll.).
   - Bebas dari dekorasi berlebih, tombol palsu/mati, nesting cards tak bermakna, dan grafik 3D generik.
4. **Kelengkapan State Desain:** Setiap screen wajib memvisualisasikan 5 kondisi:
   - *Default / Success*: Tampilan data normal dan interaksi berhasil.
   - *Loading / Skeleton*: Placeholder saat data sedang dijemput.
   - *Empty State*: Informasi ramah saat data belum tersedia disertai aksi jelas.
   - *Refreshing State*: Indikator pembaruan data tanpa memblokir seluruh layar.
   - *Error State*: Pesan kendala yang aman, mudah dimengerti, dan memuat referensi ID.
5. **Protokol Handoff ke Frontend:**
   - Handoff diekspor dalam bentuk spesifikasi token terstruktur (`tokens.json`), visual layout guide, dan kriteria penerimaan desain (*design sign-off criteria*).
   - Frontend Agent memulai scaffolding fungsional dari kontrak API, namun finalisasi visual antarmuka wajib merujuk pada hasil sign-off desain dari Pencil.

---

## 2. Rincian Milestone Desain (UX-M1 s/d UX-M8)

### UX-M1: Design System Foundations & System Tokens
- **Tujuan:** Menetapkan fondasi desain visual, token CSS variable, skala tipografi Inter, sistem grid responsif (Golden Ratio), dan blueprint komponen atomik pada Pencil.
- **Task ID:** `UX-TASK-01`
- **Dependency:** Inisialisasi M0 selesai.
- **Prasyarat Kontrak:** `contracts/openapi.v1.yaml` (ErrorEnvelope & Base Types).
- **Alat:** Pencil MCP (`get_app_state`, `get_style`, `save`, `execute`).
- **Allowed Paths:** `design/tokens/**`, `design/foundations/**`, `coordination/DESIGN_STATUS.md`.
- **Forbidden Paths:** `backend/**`, `frontend/**`, `contracts/**`.
- **Deliverables:**
  - Definisi token warna Institutional Navy & Teal (Primary, Accent, Surfaces, Borders, Text, Feedback).
  - Skala tipografi teks reguler dan angka tabular (Inter font).
  - Skala spasi (4px, 8px, 12px, 16px, 24px, 32px) dan elevation shadow.
  - Komponen atomik Pencil: Button, TextInput, Select, Badge, Checkbox, Toast, Skeleton Loader.
- **Definition of Done:** Token visual tervalidasi pada kanvas Pencil; kontras warna memenuhi rasio WCAG 2.2 AA (minimal 4.5:1 untuk teks normal).

---

### UX-M2: Authentication & Core Application Shell Experience
- **Tujuan:** Merancang pengalaman masuk sistem yang aman dan jelas (S01), halaman profil pengguna (S03), navigasi sidebar desktop, mobile drawer, dan header aplikasi adaptif.
- **Task ID:** `UX-TASK-02`
- **Dependency:** `UX-M1`.
- **Target Layar:** `S01 Login`, `S03 Profil Pengguna & Ganti Password`, Shell Aplikasi Induk.
- **Alat:** Pencil MCP.
- **Allowed Paths:** `design/screens/auth/**`, `design/screens/shell/**`.
- **UX Highlights:**
  - Form login satu kolom terpusat yang ramah password manager dan autofill.
  - Tampilan visual rate-limiting (peringatan sisa percobaan dan pesan jeda).
  - Sidebar navigasi desktop terstruktur per domain (Dashboard, Akademik, Kehadiran, Kesiswaan, Persuratan, Laporan, Pengaturan).
  - Indikator konteks peran aktif pada header tanpa membingungkan hierarki izin.
- **Definition of Done:** Rancangan layar S01, S03, dan Shell tersedia pada kanvas Pencil dengan 5 state lengkap dan responsivitas desktop/mobile.

---

### UX-M3: Master Data Administrative Workflows
- **Tujuan:** Merancang antarmuka penelusuran, penyaringan, dan pengelolaan data master: Pengguna & Peran (S04), Siswa (S05), Pegawai/Kelas/Tahun Ajaran (S06), serta Penempatan & Penugasan (S07).
- **Task ID:** `UX-TASK-03`
- **Dependency:** `UX-M2`.
- **Target Layar:** `S04 Pengguna & Peran`, `S05 Master Siswa`, `S06 Master Referensi`, `S07 Penempatan & Penugasan`.
- **Alat:** Pencil MCP.
- **Allowed Paths:** `design/screens/master_data/**`.
- **UX Highlights:**
  - Pola tabel data enterprise dengan pencarian cepat (*debounced*), filter badge, dan paginasi yang efisien.
  - Modal detail siswa dengan visualisasi tab identitas, penempatan kelas aktif, dan kontak darurat.
  - Dialog penugasan guru dan penempatan siswa massal yang bebas ambigu.
- **Definition of Done:** Wireframe dan visual design S04, S05, S06, S07 selesai dan tersimpan di Pencil.

---

### UX-M4: Attendance Operations & Correction Experience
- **Tujuan:** Merancang pengalaman pengisian presensi kelas harian yang sangat cepat dan minim kesalahan (S08) serta rekapitulasi kehadiran berkala (S09).
- **Task ID:** `UX-TASK-04`
- **Dependency:** `UX-M3`.
- **Target Layar:** `S08 Input Kehadiran Siswa Harian`, `S09 Rekapitulasi Kehadiran Siswa`.
- **Alat:** Pencil MCP.
- **UX Highlights:**
  - Layout baris siswa dengan tombol saklar cepat satu sentuh: Hadir (H), Sakit (S), Izin (I), Alpa (A).
  - Tombol aksi cepat: "Tandai Semua Hadir" untuk efisiensi waktu guru.
  - Kolom catatan yang langsung muncul saat status Sakit atau Izin dipilih.
  - Dialog koreksi kehadiran dengan penanda jelas batas waktu koreksi 24 jam dan kolom alasan koreksi audit.
  - Indikator visual saat terjadi konflik konkurensi (data telah diperbarui oleh pengguna lain).
- **Definition of Done:** Rancangan interaksi S08 dan S09 selesai, diuji kemudahan alurnya, dan siap diserahterimakan ke frontend.

---

### UX-M5: Student Affairs & Confidential BK Counseling Experience
- **Tujuan:** Merancang antarmuka penanganan kasus tata tertib kesiswaan (S10) dan catatan konseling privat bimbingan konseling (S11) dengan batas privasi yang sangat ketat.
- **Task ID:** `UX-TASK-05`
- **Dependency:** `UX-M3`.
- **Target Layar:** `S10 Daftar Kasus Kesiswaan`, `S11 Detail Kasus & Catatan Konseling`.
- **Alat:** Pencil MCP.
- **UX Highlights:**
  - Banner konfidensialitas yang jelas: "Data Rahasia Bimbingan Konseling - Hanya Terlihat oleh Konselor dan Wali Kelas Terkait".
  - Timeline kronologis tindakan (`CaseEvent`) yang menyajikan histori penanganan secara runtut.
  - Tombol aksi transisi status kasus yang dinamis sesuai wewenang peran aktor.
  - State penanganan optimistik: peringatan saat versi kasus telah berubah di server.
- **Definition of Done:** Rancangan layar S10 dan S11 dengan pemisahan visual jelas antara kasus umum dan konseling privat selesai di Pencil.

---

### UX-M6: Administration & Document Services Workflow
- **Tujuan:** Merancang alur layanan persuratan tata usaha (Skenario B): katalog jenis layanan (S12), formulir permohonan surat (S13), verifikasi & persetujuan pimpinan (S14), serta arsip dokumen privat (S15).
- **Task ID:** `UX-TASK-06`
- **Dependency:** `UX-M3`.
- **Target Layar:** `S12 Katalog Layanan Persuratan`, `S13 Form Pengajuan Surat`, `S14 Verifikasi & Disposisi TU`, `S15 Arsip & Unduhan Dokumen`.
- **Alat:** Pencil MCP.
- **UX Highlights:**
  - Tampilan kartu katalog layanan yang ringkas disertai informasi persyaratan berkas.
  - Zona seret-dan-lepas (*drag-and-drop*) berkas lampiran dengan validasi visual tipe berkas (.pdf, .jpg, .png) dan ukuran (maks 5MB).
  - Panel persetujuan Kepala Sekolah dengan tombol aksi jelas: "Setujui Permohonan" dan "Tolak Permohonan" (wajib catatan penolakan).
  - Penanda keamanan pada daftar arsip dokumen privat: tombol unduh terproteksi.
- **Definition of Done:** Seluruh screen alur Skenario B (S12, S13, S14, S15) dirancang lengkap dengan state persetujuan dan penolakan.

---

### UX-M7: Dashboards & Strategic Analytics Experience
- **Tujuan:** Merancang dashboard operasional terpersonalisasi per peran (S02), laporan analitik tren kehadiran dan layanan (S16), serta visualisasi audit trail sistem (S17).
- **Task ID:** `UX-TASK-07`
- **Dependency:** `UX-M4`, `UX-M5`, `UX-M6`.
- **Target Layar:** `S02 Dashboard Beranda Peran`, `S16 Laporan Rekapitulasi Eksekutif`, `S17 Audit Trail Viewer`.
- **Alat:** Pencil MCP.
- **UX Highlights:**
  - Komposisi Golden Ratio: 62% matriks statistik utama & tren grafis batang/garis bersih, 38% daftar tugas tertunda (*action items*) yang memerlukan disposisi cepat.
  - Filter rentang tanggal dan semester yang intuitif untuk laporan eksekutif.
  - Log audit aktivitas yang tersaji rapi dengan filter aktor, rentang waktu, dan tingkat aksi.
- **Definition of Done:** Rancangan S02, S16, dan S17 tervalidasi pada kanvas Pencil.

---

### UX-M8: Accessibility Review & Design System Handoff Package
- **Tujuan:** Melakukan audit aksesibilitas komprehensif pada seluruh kanvas desain di Pencil (WCAG 2.2 AA) dan menerbitkan paket handoff lengkap untuk Frontend Agent.
- **Task ID:** `UX-TASK-08`
- **Dependency:** `UX-M1` s/d `UX-M7`.
- **Target:** Seluruh screen S01 s/d S18.
- **Alat:** Pencil MCP.
- **Deliverables:**
  - Laporan audit kontras warna dan target sentuh seluruh komponen.
  - Berkas handoff spesifikasi desain: tata letak responsif, token CSS, dan panduan micro-interaction.
  - Formulir Design Sign-off per modul untuk acuan verifikasi integrasi visual frontend.
- **Definition of Done:** 18 screen terinspeksi dan berstatus DESIGN APPROVED; paket handoff siap dikonsumsi penuh oleh Frontend Agent.

---

## 3. Matriks Keterlacakan Desain ke Screen & Kontrak

| Screen ID | Nama Layar di UID | Milestone Desain | Endpoint Kontrak Terkait |
|---|---|---|---|
| `S01` | Form Login & Autentikasi | `UX-M2` | `POST /auth/login` |
| `S02` | Dashboard Operasional Peran | `UX-M7` | `GET /reports/dashboard`, `GET /auth/me` |
| `S03` | Profil Pengguna & Ganti Password | `UX-M2` | `GET /auth/me`, `POST /auth/logout` |
| `S04` | Manajemen Pengguna & Peran | `UX-M3` | `GET /accounts/users`, `POST /accounts/users` |
| `S05` | Master Data Siswa | `UX-M3` | `GET /master/students`, `POST /master/students` |
| `S06` | Master Pegawai, Kelas, Tahun Ajaran | `UX-M3` | `GET /master/employees`, `GET /master/classes`, `GET /master/academic-years` |
| `S07` | Penempatan Siswa & Penugasan Guru | `UX-M3` | `GET /master/enrollments`, `GET /master/assignments` |
| `S08` | Input Kehadiran Siswa Harian | `UX-M4` | `GET /attendance/roster`, `POST /attendance/bulk` |
| `S09` | Rekapitulasi Kehadiran Siswa | `UX-M4` | `GET /attendance`, `GET /reports/attendance.xlsx` |
| `S10` | Daftar Kasus Kesiswaan | `UX-M5` | `GET /student-affairs/cases`, `POST /student-affairs/cases` |
| `S11` | Detail Kasus & Catatan Konseling | `UX-M5` | `GET /student-affairs/cases/{id}`, `POST /student-affairs/cases/{id}/transitions` |
| `S12` | Katalog Layanan Persuratan | `UX-M6` | `GET /administration/service-types` |
| `S13` | Formulir Pengajuan Surat | `UX-M6` | `POST /administration/requests`, `POST /administration/requests/{id}/documents` |
| `S14` | Verifikasi & Disposisi Surat TU | `UX-M6` | `GET /administration/requests`, `POST /administration/requests/{id}/transitions` |
| `S15` | Arsip Dokumen & Unduhan Privat | `UX-M6` | `GET /administration/documents`, `GET /administration/documents/{id}/download` |
| `S16` | Laporan Rekapitulasi Eksekutif | `UX-M7` | `GET /reports/attendance.xlsx`, `GET /reports/administration.pdf` |
| `S17` | Riwayat Audit Trail Sistem | `UX-M7` | `GET /audit-logs` |
| `S18` | Halaman Status Sistem & Error | `UX-M2` / `UX-M8` | Response Envelope Error (401, 403, 404, 409, 429, 500) |
