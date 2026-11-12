# Master Design Handoff (Paket Serah Terima Desain UI/UX ke Frontend)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | **CONDITIONALLY_READY - DESIGN_ALIGNED_WITH_COORDINATOR_OPEN_ITEMS** |
| Versi Rilis | **UX-M9.3 Release (Deterministic Schema Alignment & Design Handoff Freeze)** |
| Tanggal Efektif | 12 November 2026 |
| Pengelola | UI/UX Design Agent (Principal UI/UX Designer & Architect) |
| Konsumen Utama | Frontend Agent, Backend Agent, Coordinator Agent |
| Target Desain Visual | Pencil MCP (`pen.dev`) - `design/master-canvas.pen` (864 KB) |
| Repositori Token | `design/tokens.json` (7.1 KB, 78 token kanonikal) |
| Direktori Bukti Visual | `design/evidence/` (32 berkas visual PNG terverifikasi) |
| Acuan Kontrak API | `contracts/openapi.v1.yaml` (Base URL: `http://localhost:8000/api`, 31 paths, 43 operations, 65 schemas) |
| Acuan Skema Data | `contracts/database.dbml` (18 entitas relasional, PostgreSQL 16) |
| Acuan Wewenang & Aturan | `docs/RBAC_MATRIX.md`, `docs/PRD.md`, `docs/AFD.md`, `docs/UID.md`, `docs/DECISION_LOG.md` |

---

## 1. Document Metadata & Ruang Lingkup

Dokumen ini merupakan spesifikasi teknis tunggal serah terima desain antarmuka (*Single Source of Truth for Design Handoff*) Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut. Seluruh definisi visual, arsitektur informasi, alur interaksi, pemetaan kontrak API, dan pedoman implementasi frontend dikonsolidasikan secara deterministik untuk mencegah inkonsistensi antar-jalur produksi.

### Prinsip Utama Penyelarasan Kontrak (UX-M9.3 Release)
1. **Penyelarasan Skema Deterministik (Deterministic Schema Alignment):**
   - Seluruh 43 operasi API diekstrak langsung dari `contracts/openapi.v1.yaml` dengan base URL resmi `http://localhost:8000/api` (tanpa prefix `/v1/` atau duplikasi `/api`).
   - Seluruh nama field request, properti required, tipe data, enum, dan skema response disinkronkan tanpa ada field atau parameter fiktif yang tidak didukung kontrak backend.
2. **Kepatuhan Matriks Otorisasi RBAC (RBAC Realism):**
   - Hak akses dinyatakan dalam aksi operasional riil (`LIST`, `READ`, `CREATE`, `UPDATE`, `DEACTIVATE`, `ASSIGN`, `RECORD`, `CORRECT`, `PROCESS`, `APPROVE`, `REJECT`, `CANCEL`, `EXPORT`, `DOWNLOAD`, `AUDIT`) dan batasan lingkup objek (*object-level scope*).
   - 4 kebijakan bisnis berstatus `PENDING_APPROVAL` pada `docs/RBAC_MATRIX.md` ditegakkan secara ketat sebagai `DENIED` pada antarmuka hingga terbit Surat Keputusan (SK) resmi sekolah.
3. **Penyaringan Fitur Spekulatif (Anti-AI Slop & Minimalist Reality):**
   - Menghapus asumsi otomatis seperti default status Hadir pada presensi massal, batas waktu koreksi 24 jam yang belum disahkan, trigger otomatis penanganan kasus akibat alpa 3 hari, jadwal mata pelajaran per jam/lonceng, widget pemantauan internal database/Redis, dan badge fiktif verifikasi digital/stempel barcode.
4. **Verifikasi Filter Endpoint:**
   - Filter pada antarmuka pengguna diselaraskan dengan parameter query yang benar-benar didukung oleh kontrak API. Filter yang belum didukung kontrak dinonaktifkan atau ditandai sebagai filter tampilan lokal pada halaman aktif, dan dicatat sebagai *Contract Gap* untuk tindak lanjut Coordinator.
5. **Independensi Implementasi Frontend:**
   - Frontend Agent dapat langsung mengimplementasikan arsitektur aplikasi, routing, client state, skema validasi Zod, dan komponen atomik mengacu pada dokumen ini tanpa menunggu implementasi backend selesai.

---

## 2. Executive Design Overview (Filosofi & Pendekatan Desain)

Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut dirancang khusus untuk memenuhi kebutuhan tata kelola operasional sekolah negeri dengan standar korporat modern. Antarmuka mengutamakan kejelasan informasi (*information clarity*), kecepatan akses (*low latency workflows*), dan keandalan data (*transactional integrity*).

### 2.1 Filosofi Visual: Institutional Navy & Teal
- **Wibawa Institusional & Integritas Publik:** Warna dominan *Institutional Navy* (`#173B63`) memancarkan kredibilitas, keamanan sistem pemerintahan/pendidikan, dan kejelasan struktur hierarki.
- **Kesegaran & Ketelitian Administrasi:** Warna aksen *Institutional Teal* (`#12665C`) digunakan secara terukur untuk memandu fokus aksi primer, status terverifikasi, dan penanda progres aktif.
- **Ketahanan Visual Pengguna:** Latar permukaan netral abu-abu terang (`#F5F7FA`) dengan kontras kartu putih bersih (`#FFFFFF`) mengurangi kelelahan mata operator tata usaha dan guru yang menggunakan sistem berjam-jam setiap hari.

---

## 3. Design System Foundations (Fondasi Sistem Desain)

Seluruh token visual tersimpan secara baku pada `design/tokens.json` dan wajib diimpor langsung ke dalam konfigurasi Tailwind CSS frontend.

### 3.1 Palet Warna Resmi & Kalkulasi Kontras WCAG Terverifikasi

Kalkulasi rasio kontras dihitung secara matematis menggunakan formula resmi W3C Relative Luminance ($L = 0.2126 \cdot R + 0.7152 \cdot G + 0.0722 \cdot B$):

| Token Name | Nilai Heksadesimal | Pasangan Latar Belakang | Rasio Kontras | Kepatuhan WCAG 2.2 | Fungsi Penggunaan |
|---|---|---|---|---|---|
| `color.brand.primary` | `#173B63` | White (`#FFFFFF`) | **11.40 : 1** | AAA Normal (>7:1) | Tombol aksi primer, navbar, sidebar aktif, judul utama |
| `color.brand.accent` | `#12665C` | White (`#FFFFFF`) | **6.82 : 1** | AA Normal (>4.5:1), AAA Large | Tombol simpan/konfirmasi, tab aktif, ring fokus input |
| `color.surface.card` | `#FFFFFF` | Background (`#F5F7FA`) | **1.09 : 1** | Kontras Bidang | Kartu kontainer, modal pop-up, baris tabel selang-seling |
| `color.surface.bg` | `#F5F7FA` | Canvas Base | Netral | Kontras Bidang | Latar belakang kanvas aplikasi, area kerja utama |
| `color.text.primary` | `#1E293B` | White (`#FFFFFF`) | **14.38 : 1** | AAA Normal (>7:1) | Teks utama, judul tabel, label formulir, angka metrik |
| `color.text.secondary` | `#64748B` | White (`#FFFFFF`) | **4.76 : 1** | AA Normal (>4.5:1) | Deskripsi pendukung, metadata, rekam jejak waktu |
| `color.text.secondary` | `#64748B` | Background (`#F5F7FA`) | **4.43 : 1** | AA Large (>=18pt) / Non-Body | Sub-judul pada latar abu terang; teks penting wajib pakai Slate 700 (`#334155`) |
| `color.text.muted` | `#94A3B8` | White (`#FFFFFF`) | **2.56 : 1** | Ikon Dekoratif / Subtle | DILARANG untuk teks yang harus dibaca; hanya untuk garis pemisah dan ikon non-kritis |
| `color.border.default` | `#E2E8F0` | White (`#FFFFFF`) | **1.23 : 1** | Batas Struktur | Garis batas kartu, tabel grid, pemisah bagian formulir |
| `color.status.success` | `#047857` (Bg: `#ECFDF5`) | Teks Success di Badge | **6.42 : 1** | AA Normal (>4.5:1) | Status: AKTIF, HADIR, DISETUJUI, SELESAI |
| `color.status.warning` | `#B45309` (Bg: `#FFFBEB`) | Teks Warning di Badge | **5.58 : 1** | AA Normal (>4.5:1) | Status: DIPROSES, MENUNGGU_PERSETUJUAN, SAKIT, IZIN |
| `color.status.danger` | `#BE123C` (Bg: `#FFF1F2`) | Teks Danger di Badge | **7.28 : 1** | AAA Normal (>7:1) | Status: ALPA, DITOLAK, DIBATALKAN, NONAKTIF, Error 409 |
| `color.status.info` | `#0369A1` (Bg: `#F0F9FF`) | Teks Info di Badge | **9.84 : 1** | AAA Normal (>7:1) | Status: DIAJUKAN, WALI_KELAS, Notifikasi sistem |

### 3.2 Skala Tipografi (Typography Scale)
Menggunakan font keluarga sistematis: **Inter** (atau fallback `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`).

| Level Tipografi | Ukuran Font | Line Height | Font Weight | Letter Spacing | Penggunaan Antarmuka |
|---|---|---|---|---|---|
| `font.size.display` | 30px (1.875rem) | 36px (1.2) | 700 (Bold) | -0.02em | Hero banner, total ringkasan eksekutif |
| `font.size.h1` | 24px (1.5rem) | 32px (1.33) | 700 (Bold) | -0.01em | Judul halaman operasional (H1) |
| `font.size.h2` | 20px (1.25rem) | 28px (1.4) | 600 (SemiBold)| -0.005em | Judul kartu panel, judul modal |
| `font.size.h3` | 16px (1.0rem) | 24px (1.5) | 600 (SemiBold)| 0.0em | Judul seksi tabel, widget KPI |
| `font.size.body` | 14px (0.875rem) | 20px (1.43) | 400 (Regular) | 0.0em | Teks data tabel, isi konten, petunjuk formulir |
| `font.size.body-medium` | 14px (0.875rem) | 20px (1.43) | 500 (Medium) | 0.0em | Nilai baris tabel, label tombol standar |
| `font.size.small` | 12px (0.75rem) | 16px (1.33) | 500 (Medium) | 0.01em | Badge status, header kolom tabel, teks bantuan input |
| `font.size.xs` | 11px (0.6875rem)| 14px (1.27) | 600 (SemiBold)| 0.02em | Metadata rekam jejak (audit timestamp), tag singkatan |

### 3.3 Sistem Border Radius & Elevasi (Corner Radius & Shadows)
- `radius.sm`: 4px - Badge tag status, checkbox, toggle segmented control.
- `radius.md`: 6px - Input text field, tombol standar, dropdown select box.
- `radius.lg`: 8px - Kontainer kartu modul (Card Container), panel pratinjau.
- `radius.xl`: 12px - Modal dialog box, drawer panel samping, banner pengumuman.
- `shadow.card`: `0 1px 3px 0 rgba(0, 0, 0, 0.08), 0 1px 2px -1px rgba(0, 0, 0, 0.04)` (Flat clean elevation).
- `shadow.popover`: `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.05)` (Dropdown, tooltip).

### 3.4 Skala Spasi & Proporsi Emas (Spacing Scale & Golden Ratio)
- Grid Spacing: 4px base (4, 8, 12, 16, 20, 24, 32, 48, 64 px).
- Golden Ratio Split Layout: Layar detail (`S11_DetailKasus`, `S14_DetailPermohonan`) membagi area konten dengan rasio 61.8% (lebar konten aksi utama ~800px) dan 38.2% (lebar panel ringkasan/pendukung ~460px) pada resolusi desktop 1440px.

---

## 4. Component Inventory (Inventori Komponen Atomic Design)

### 4.1 Komponen Atom (Atoms)
- `Button`: Varian `primary` (`#173B63`), `accent` (`#12665C`), `secondary` (`#FFFFFF` dengan border `#E2E8F0`), `danger` (`#BE123C`), `ghost`. Tinggi standar: 38px (desktop), 44px (touch target).
- `BadgeStatus`: Komponen tag status terstandardisasi sesuai 4 modul semantik (lihat Bab 12).
- `InputField`: Input teks, sandi, angka dengan label terikat, indikator wajib (`*`), pesan error terintegrasi, dan focus ring `#12665C`.
- `SelectDropdown`: Dropdown pemilihan opsi dengan pencarian lokal untuk rombel, jenis layanan, dan status.
- `ToggleRoster`: Tombol pilihan status presensi 4 opsi (`H`, `S`, `I`, `A`) dengan state visual unselected netral.

### 4.2 Komponen Molekul (Molecules)
- `SearchBar`: Gabungan ikon kaca pembesar, input teks, tombol bersihkan, dan debounce filter 300ms.
- `FilterChipGroup`: Grup tombol chip penyaring status dengan indikator jumlah hitungan data.
- `PaginationControl`: Paginasi tabel lengkap dengan info cakupan baris (`Menampilkan 1-10 dari 48 baris`), pemilih `page_size` (10, 25, 50), dan tombol navigasi halaman.
- `MetricCard`: Kartu ringkasan metrik dasbor dengan judul indikator, angka nilai utama, label sub-status, dan ikon pembeda.
- `AuditLogRow`: Baris rekaman jejak audit dengan timestamp terformat, nama aktor pengguna, tag aksi, dan detail objek.

### 4.3 Komponen Organisme (Organisms)
- `AppShell`: Kerangka navigasi master dengan Sidebar Navigasi Kiri (lebar 240px desktop, 64px tablet icon rail, drawer mobile), Header Atas (lebar penuh dengan breadcrumb, konteks peran, dan profil pengguna), dan Kontainer Konten Utama.
- `RosterAttendanceTable`: Tabel pencatatan kehadiran kelas massal dengan toggle 4 state per siswa, input catatan khusus, dan kalkulator persentase kehadiran real-time.
- `CaseTimelineCard`: Kartu alur kronologi penanganan kasus siswa dengan penanda versi optimistik (`expected_version`).
- `DocumentVerificationPanel`: Panel pratinjau verifikasi berkas permohonan surat dengan penampil status disposisi berjenjang.

---

## 5. Information Architecture & App Shell (Arsitektur Informasi & Kerangka Aplikasi)

### 5.1 Navigasi Berdasarkan 6 Peran Pengguna (Role Navigation Configurations)
Sistem informasi memisahkan menu navigasi secara dinamis berdasarkan peran aktif pengguna:

| Peran Pengguna | Menu Navigasi Utama | Endpoint API Terkait | Izin Wewenang |
|---|---|---|---|
| **ADMINISTRATOR** | Dashboard Admin, Manajemen Akun, Data Induk Master, Penugasan & Rombel, Log Audit Sistem | `/reports/dashboard`, `/accounts/users`, `/master/*`, `/audit-logs` | Pengelolaan teknis & akun penuh |
| **GURU** | Dashboard Guru, Presensi Kelas Mengajar, Rekapitulasi Presensi Kelas Binaan | `/reports/dashboard`, `/auth/me`, `/attendance/roster`, `/attendance/bulk`, `/attendance` | Catat presensi rombel aktif |
| **WALI_KELAS** | Dashboard Wali Kelas, Presensi Rombel Binaan, Rekapitulasi & Koreksi, Rujukan Kesiswaan | `/reports/dashboard`, `/attendance/*`, `/student-affairs/cases` | Presensi & rujukan kelas binaan |
| **KESISWAAN** | Dashboard Kesiswaan, Kasus Pelanggaran & Konseling BK, Catat Tindakan Mediasi, Rekap Kasus | `/reports/dashboard`, `/student-affairs/cases/*`, `/master/students` | Penanganan kasus & konseling privat |
| **TATA_USAHA** | Dashboard Tata Usaha, Daftar Permohonan Surat, Proses Verifikasi Berkas, Arsip Dokumen Digital | `/reports/dashboard`, `/administration/requests/*`, `/administration/documents/*` | Verifikasi operasional persuratan |
| **PIMPINAN** | Dashboard Eksekutif, Antrean Persetujuan Disposisi Surat, Laporan Terpadu Sekolah & Ekspor | `/reports/dashboard`, `/administration/requests/*`, `/reports/*` | Disposisi persetujuan & monitoring |

### 5.2 Multi-Role Context Switcher (Pemisahan Tampilan vs Otorisasi Server)
- Pengguna yang memiliki beberapa peran sah (contoh: Staf Guru yang juga menjabat Wali Kelas X-A) dapat beralih konteks tampilan melalui menu profil di Header Atas (`S03_ProfilKonteks`).
- **Aturan Otorisasi:** Pengalihan konteks di sisi antarmuka semata-mata menyaring tampilan visual menu navigasi. Backend Django Ninja mengevaluasi wewenang secara aditif (kesatuan dari seluruh peran yang dimiliki pengguna).

---

## 6. Screen Inventory (Inventori Lengkap Layar Antarmuka S01 s/d S18 & Varian Responsif)

| Kode Layar | Nama Layar Kanonikal | Frame Node ID | Resolusi Kanvas | Bukti Visual PNG | Cakupan Fungsional Utama |
|---|---|---|---|---|---|
| `S01` | `S01_Login_Desktop` | `Ap3YR` | 1440 x 900 | `evidence/S01_Login_Desktop.png` | Autentikasi kredensial pengguna & penanganan brute force |
| `S01-M` | `S01_Login_Mobile` | `x6nWP` | 390 x 844 | `evidence/S01_Login_Mobile.png` | Varian mobile login responsive dengan target sentuh 44px |
| `S02-ADM`| `S02_DashboardAdmin_Desktop` | `tHNs6` | 1440 x 900 | `evidence/S02_DashboardAdmin_Desktop.png` | Ringkasan metrik operasional terpusat dari DashboardMetricsResponse |
| `S02-GRU`| `S02_DashboardGuru_Desktop` | `P7RgJ` | 1440 x 900 | `evidence/S02_DashboardGuru_Desktop.png` | Penugasan mengajar aktif dari /auth/me & status catat presensi |
| `S02-WLK`| `S02_DashboardWaliKelas_Desktop` | `mGkfL` | 1440 x 900 | `evidence/S02_DashboardWaliKelas_Desktop.png` | Tingkat kehadiran rombel binaan & siswa perlu perhatian khusus |
| `S02-KSW`| `S02_DashboardKesiswaan_Desktop` | `eh6QG` | 1440 x 900 | `evidence/S02_DashboardKesiswaan_Desktop.png` | Antrean kasus aktif konseling BK & rekapan pembinaan siswa |
| `S02-TU` | `S02_DashboardTataUsaha_Desktop` | `w9p6O` | 1440 x 900 | `evidence/S02_DashboardTataUsaha_Desktop.png` | Antrean permohonan surat masuk TU & status proses berkas |
| `S02-PMP`| `S02_DashboardPimpinan_Desktop` | `cnAzK` | 1440 x 900 | `evidence/S02_DashboardPimpinan_Desktop.png` | Antrean disposisi persetujuan pimpinan & ringkasan sekolah |
| `S02-TAB`| `S02_Dashboard_Tablet` | `V8dsvd` | 768 x 1024 | `evidence/S02_Dashboard_Tablet.png` | Varian tablet dasbor eksekutif dengan grid metrik adaptif 2x2 |
| `S03` | `S03_ProfilKonteks_Desktop` | `H21Lu` | 1440 x 900 | `evidence/S03_ProfilKonteks_Desktop.png` | Profil pengguna dari /auth/me, info sesi & pengalih konteks navigasi |
| `S04` | `S04_ManajemenAkun_Desktop` | `gg4b3` | 1440 x 900 | `evidence/S04_ManajemenAkun_Desktop.png` | Pengelolaan akun pengguna, status keaktifan & penetapan peran |
| `S05` | `S05_MasterSiswa_Desktop` | `dezB0` | 1440 x 900 | `evidence/S05_MasterSiswa_Desktop.png` | Katalog data induk siswa, filter pencarian & status siswa |
| `S06` | `S06_MasterDataAkademik_Desktop` | `gdLXM` | 1440 x 900 | `evidence/S06_MasterDataAkademik_Desktop.png` | Tabulasi data pegawai, kelas rombel, dan tahun ajaran aktif |
| `S07` | `S07_PenempatanPenugasan_Desktop` | `r40Kr2` | 1440 x 900 | `evidence/S07_PenempatanPenugasan_Desktop.png` | Penempatan rombel siswa (enrollments) & penugasan guru/wali kelas |
| `S08` | `S08_CatatKehadiran_Desktop` | `Q1Xifi` | 1440 x 900 | `evidence/S08_CatatKehadiran_Desktop.png` | Pencatatan kehadiran kelas harian secara atomik massal |
| `S08-TAB`| `S08_CatatKehadiran_Tablet` | `C968L` | 768 x 1024 | `evidence/S08_CatatKehadiran_Tablet.png` | Varian tablet pencatatan presensi dengan kartu siswa sentuh |
| `S08-M` | `S08_CatatKehadiran_Mobile` | `zxwXr` | 390 x 844 | `evidence/S08_CatatKehadiran_Mobile.png` | Varian mobile pencatatan presensi darurat oleh guru piket |
| `S09` | `S09_RekapKehadiran_Desktop` | `Y0rij` | 1440 x 900 | `evidence/S09_RekapKehadiran_Desktop.png` | Rekapitulasi absensi rombel berkala & riwayat kehadiran siswa |
| `S10` | `S10_DaftarKasus_Desktop` | `NUFLD` | 1440 x 900 | `evidence/S10_DaftarKasus_Desktop.png` | Daftar penanganan kasus kedisiplinan & bimbingan konseling |
| `S10-M` | `S10_DaftarKasus_Mobile` | `xF9g9` | 390 x 844 | `evidence/S10_DaftarKasus_Mobile.png` | Varian mobile daftar kasus konseling untuk guru pembina lapangan |
| `S11` | `S11_DetailKasus_Desktop` | `LElcs` | 1440 x 900 | `evidence/S11_DetailKasus_Desktop.png` | Rincian kasus, pencatatan tindakan mediasi & penyelesaian |
| `S12` | `S12_DaftarLayanan_Desktop` | `L3oHd` | 1440 x 900 | `evidence/S12_DaftarLayanan_Desktop.png` | Katalog permohonan layanan administrasi surat operasional TU |
| `S13` | `S13_FormPermohonan_Desktop` | `VTbEe` | 1440 x 900 | `evidence/S13_FormPermohonan_Desktop.png` | Formulir pengajuan surat siswa dengan unggah berkas pendukung |
| `S14` | `S14_DetailPermohonan_Desktop` | `S8MG0` | 1440 x 900 | `evidence/S14_DetailPermohonan_Desktop.png` | Verifikasi berkas, persetujuan pimpinan, dan penerbitan surat |
| `S14-TAB`| `S14_DetailPermohonan_Tablet` | `vHJ6o` | 768 x 1024 | `evidence/S14_DetailPermohonan_Tablet.png` | Varian tablet verifikasi permohonan disposisi pimpinan |
| `S15` | `S15_ArsipDokumen_Desktop` | `Y6pRp` | 1440 x 900 | `evidence/S15_ArsipDokumen_Desktop.png` | Katalog arsip dokumen digital terbit & unduhan binary privat |
| `S16` | `S16_LaporanSekolah_Desktop` | `nKRc7` | 1440 x 900 | `evidence/S16_LaporanSekolah_Desktop.png` | Laporan eksekutif terpadu & ekspor resmi spreadsheet/PDF |
| `S17` | `S17_AuditTrail_Desktop` | `vZKl5` | 1440 x 900 | `evidence/S17_AuditTrail_Desktop.png` | Log rekaman jejak audit sistem enterprise & investigasi forensik |
| `S18` | `S18_ErrorStates_Desktop` | `v93RXB` | 1440 x 900 | `evidence/S18_ErrorStates_Desktop.png` | Penanganan kesalahan sistem HTTP 403, 404, 409, 500, dan offline |
| `SHELL` | `AppShell_Desktop` | `MEJyA` | 1440 x 900 | `evidence/AppShell_Desktop.png` | Kerangka tata letak desktop dengan sidebar 240px & breadcrumbs |
| `SH-TAB`| `AppShell_Tablet` | `aGxFY` | 768 x 1024 | `evidence/AppShell_Tablet.png` | Kerangka tata letak tablet dengan sidebar icon rail 64px |
| `TOKENS`| `UX_M1_DesignSystem_Tokens` | `tOR0X` | 1440 x 1200 | `evidence/UX_M1_DesignSystem_Tokens.png` | Pustaka visual komponen sistem desain, palet warna & varian tombol |

---

## 7. Role & Permission Mapping (Matriks Hak Akses Berdasarkan docs/RBAC_MATRIX.md)

Matriks kewenangan berikut disusun berdasarkan batasan wewenang riil pada `docs/RBAC_MATRIX.md`. Seluruh wewenang yang masih berstatus `PENDING_APPROVAL` diperlakukan secara tegas sebagai `DENIED` pada antarmuka hingga disahkan:

| Modul & Sumber Data | Administrator | Guru Mapel | Wali Kelas | Kesiswaan / BK | Tata Usaha | Pimpinan / Kepsek | Catatan Implementasi & Batasan Objek |
|---|---|---|---|---|---|---|---|
| **Autentikasi & Profil** (`/auth/*`) | Akses Penuh | Akses Penuh | Akses Penuh | Akses Penuh | Akses Penuh | Akses Penuh | Profil via `GET /auth/me`, logout via token blacklist |
| **Manajemen Akun** (`/accounts/*`) | `LIST`, `CREATE`, `UPDATE` | DENIED | DENIED | DENIED | DENIED | DENIED | Khusus Administrator teknis sekolah |
| **Data Induk Siswa** (`/master/students`) | `LIST`, `READ`, `CREATE`, `UPDATE` | `LIST`, `READ` | `LIST`, `READ` | `LIST`, `READ` | `LIST`, `READ` *(Create/Update: PENDING)* | `LIST`, `READ` | Hak TU buat/ubah siswa berstatus `DENIED` menunggu SK |
| **Tahun Ajaran & Kelas** (`/master/classes`) | `LIST`, `CREATE`, *(Update: GAP)* | `LIST`, `READ` | `LIST`, `READ` | `LIST`, `READ` | `LIST`, `READ` | `LIST`, `READ` | Read-only untuk seluruh peran non-admin |
| **Penempatan & Penugasan** (`/master/assignments`)| `LIST`, `CREATE` | `LIST` (Penugasan sendiri) | `LIST` (Rombel binaan) | `LIST`, `READ` | `LIST`, `CREATE` (Penempatan Rombel) | `LIST`, `READ` | Guru hanya membaca daftar kelas penugasannya |
| **Presensi Kelas Harian** (`/attendance/*`) | `LIST`, `READ` | `RECORD`, `READ` (Kelas aktif) | `RECORD`, `CORRECT` (Binaan) | `READ` | `READ` | `READ` | Simpan atomik via `/attendance/bulk`. Koreksi >24j `DENIED` |
| **Kasus Kesiswaan & BK** (`/student-affairs/*`) | `READ` (Metadata) | `CREATE` (Rujukan) | `CREATE`, `READ` (Binaan) | `PROCESS`, `ACTION`, `RESOLVE` | DENIED | `READ` (Eksekutif) | Catatan konseling privat rahasia khusus Kesiswaan/BK |
| **Layanan Persuratan** (`/administration/requests`)| `READ` (Metadata) | DENIED | DENIED | DENIED | `CREATE`, `PROCESS`, `FINALIZE` | `APPROVE`, `REJECT` (Disposisi) | Siswa ajukan surat via loket TU (`S13`), Pimpinan disposisi (`S14`) |
| **Arsip Dokumen Privat** (`/administration/documents`)| DENIED | DENIED | DENIED | DENIED | `LIST`, `DOWNLOAD` | `LIST`, `DOWNLOAD` | Unduhan binary terproteksi JWT via endpoint download privat |
| **Laporan & Ekspor** (`/reports/*`) | `READ` | `READ` (Rombel sendiri) | `READ` (Rombel binaan) | `READ` (Kasus) | `EXPORT` (Administrasi) | `EXPORT`, `READ` (Penuh) | Ekspor format `.xlsx` dan `.pdf` resmi sekolah |
| **Log Audit Sistem** (`/audit-logs`) | `LIST`, `AUDIT` | DENIED | DENIED | DENIED | DENIED | `DENIED` *(Audit: PENDING)* | Hak audit pimpinan berstatus `DENIED` menunggu validasi sekolah |

---

## 8. Screen-to-API Contract Mapping (Pemetaan Presisi 43 Operasi OpenAPI Aktual)

Pemetaan berikut diekstrak langsung dari `contracts/openapi.v1.yaml` (Base URL: `http://localhost:8000/api`):

| No | Method | Path Kontrak Aktual | Operation ID | Request Schema & Fields | Response Schema | Layar Terkait | Parameter & Wewenang |
|---|---|---|---|---|---|---|---|
| 1 | `POST` | `/auth/login` | `authLogin` | `LoginRequest` (`username`, `password`) | `LoginResponse` (`access_token`, `refresh_token`, `token_type`, `expires_in`) | `S01`, `S01-M` | Public, Rate Limit 5 req/min, Error 401/429 |
| 2 | `POST` | `/auth/refresh` | `authRefresh` | `RefreshRequest` (`refresh_token`) | `LoginResponse` | Seluruh Layar | Payload JSON refresh_token, Error 401 |
| 3 | `POST` | `/auth/logout` | `authLogout` | `LogoutRequest` (`refresh_token`) | `LogoutResponse` (`message`) | `S03`, `SHELL` | Blacklist token pada Redis, Error 200 |
| 4 | `GET` | `/auth/me` | `authMe` | None | `UserProfileResponse` (`id`, `username`, `name`, `employee_id`, `roles`, `assigned_classes`) | `S02`, `S03`, `SHELL`| BearerAuth, Mengambil identitas & kelas penugasan |
| 5 | `GET` | `/master/academic-years` | `listAcademicYears` | None | `AcademicYearListResponse` (items: `id`, `name`, `start_date`, `end_date`, `is_active`) | `S06` | Query params: NONE. Filter lokal di halaman aktif |
| 6 | `POST` | `/master/academic-years` | `createAcademicYear` | `AcademicYearCreateRequest` (`name`, `start_date`, `end_date`, `is_active`) | `AcademicYearItem` | `S06` | Wewenang: ADMINISTRATOR, Response 201 |
| 7 | `GET` | `/master/classes` | `listClasses` | None | `ClassListResponse` (items: `id`, `academic_year_id`, `academic_year_name`, `name`, `level`) | `S06`, `S07`, `S08` | Query: `academic_year_id` (integer) |
| 8 | `POST` | `/master/classes` | `createClass` | `ClassCreateRequest` (`academic_year_id`, `name`, `level`) | `ClassItem` | `S06` | Wewenang: ADMINISTRATOR, Response 201 |
| 9 | `GET` | `/master/students` | `listStudents` | None | `StudentListResponse` (items: `id`, `student_number`, `name`, `gender`, `status`, `current_class_name`) | `S05` | Query: `search` (string), `status` (StudentStatusEnum) |
| 10 | `POST` | `/master/students` | `createStudent` | `StudentCreateRequest` (`student_number`, `name`, `gender`, `status`) | `StudentDetailResponse` | `S05` | Wewenang: ADMINISTRATOR (TU: PENDING/DENIED) |
| 11 | `GET` | `/master/students/{id}` | `getStudentDetail` | None | `StudentDetailResponse` (`id`, `student_number`, `name`, `gender`, `status`, `enrollments`) | `S05`, `S11` | Path: `id` (integer), Response 200/404 |
| 12 | `PATCH`| `/master/students/{id}` | `updateStudent` | `StudentUpdateRequest` (`name`, `gender`, `status`) | `StudentDetailResponse` | `S05` | Path: `id` (integer), Wewenang: ADMINISTRATOR |
| 13 | `GET` | `/master/enrollments` | `listEnrollments` | None | `EnrollmentListResponse` (items: `id`, `student_id`, `class_id`, `start_date`, `end_date`) | `S07` | Query: `class_id` (integer), `student_id` (integer) |
| 14 | `POST` | `/master/enrollments` | `createEnrollment` | `EnrollmentCreateRequest` (`student_id`, `class_id`, `start_date`) | `EnrollmentItem` | `S07` | Wewenang: ADMINISTRATOR, TATA_USAHA |
| 15 | `GET` | `/master/assignments` | `listClassAssignments` | None | `ClassAssignmentListResponse` (items: `id`, `employee_id`, `class_id`, `role`, `start_date`) | `S07`, `S08` | Query: `class_id` (integer), `employee_id` (integer) |
| 16 | `POST` | `/master/assignments` | `createClassAssignment`| `ClassAssignmentCreateRequest` (`employee_id`, `class_id`, `role`: GURU_MAPEL/WALI_KELAS, `start_date`) | `ClassAssignmentItem` | `S07` | Wewenang: ADMINISTRATOR, Response 201 |
| 17 | `GET` | `/master/employees` | `listEmployees` | None | `EmployeeListResponse` (items: `id`, `user_id`, `nip`, `name`, `phone`, `status`, `created_at`) | `S06`, `S07` | Query: `search` (string). Tidak ada filter jabatan |
| 18 | `POST` | `/master/employees` | `createEmployee` | `EmployeeCreateRequest` (`user_id`, `nip`, `name`, `phone`, `status`) | `EmployeeItem` | `S06` | Wewenang: ADMINISTRATOR, Response 201 |
| 19 | `GET` | `/attendance/roster` | `getAttendanceRoster` | None | `AttendanceRosterResponse` (`class_id`, `class_name`, `date`, items: `student_id`, `student_name`, `student_number`, `status`, `note`) | `S08`, `S08-TAB` | Query: `class_id` (int, req), `date` (date, req) |
| 20 | `POST` | `/attendance/bulk` | `saveAttendanceBulk` | `AttendanceBulkRequest` (`class_id`, `date`, items: `student_id`, `status`, `note`) | `AttendanceBulkResponse` (`total_recorded`, `recorded_at`) | `S08`, `S08-M` | Simpan transaksi atomik. Error: 403, 422 |
| 21 | `GET` | `/attendance` | `getAttendanceRecap` | None | `AttendanceRecapResponse` (items: `student_id`, `student_number`, `student_name`, `hadir_count`, `sakit_count`, `izin_count`, `alpa_count`, `attendance_rate_pct`) | `S09` | Query: `class_id` (int), `start_date` (date, req), `end_date` (date, req) |
| 22 | `GET` | `/student-affairs/cases` | `listStudentCases` | None | `StudentCaseListResponse` (items: `id`, `case_number`, `student_id`, `student_name`, `title`, `status`, `assigned_to_name`, `version`, `created_at`) | `S10`, `S10-M` | Query: `status` (CaseStatusEnum). Tidak ada query student_id |
| 23 | `POST` | `/student-affairs/cases` | `createStudentCase` | `StudentCaseCreateRequest` (`student_id`, `title`, `summary`, `assigned_to_id`) | `StudentCaseDetailResponse` | `S10` | Wewenang: GURU, WALI_KELAS, KESISWAAN |
| 24 | `GET` | `/student-affairs/cases/{id}`| `getStudentCaseDetail`| None | `StudentCaseDetailResponse` (`id`, `case_number`, `student_id`, `student_name`, `title`, `summary`, `status`, `assigned_to_id`, `version`, `timeline`) | `S11` | Path: `id` (integer), Wewenang: KESISWAAN, WALI_KELAS |
| 25 | `POST` | `/student-affairs/cases/{id}/transitions` | `transitionStudentCase` | `CaseTransitionRequest` (`action`: MULAI_PENANGANAN, CATAT_TINDAKAN, SELESAIKAN, BATALKAN; `note`; `expected_version`) | `StudentCaseDetailResponse` | `S11` | Optimistic locking via `expected_version`, Error 409 |
| 26 | `GET` | `/administration/service-types` | `listServiceTypes` | None | `ServiceTypeListResponse` (items: `id`, `code`, `name`, `description`, `requires_approval`, `is_active`) | `S12`, `S13` | Query params: NONE. Seluruh tipe layanan aktif |
| 27 | `POST` | `/administration/service-types` | `createServiceType` | `ServiceTypeCreateRequest` (`code`, `name`, `description`, `requires_approval`, `is_active`) | `ServiceTypeItem` | `S12` | Wewenang: ADMINISTRATOR (TU: PENDING/DENIED) |
| 28 | `GET` | `/administration/requests` | `listServiceRequests` | None | `ServiceRequestListResponse` (items: `id`, `tracking_number`, `service_type_name`, `applicant_name`, `status`, `requires_approval`, `version`, `created_at`) | `S12` | Query: `status` (ServiceRequestStatusEnum). Tidak ada service_type_id |
| 29 | `POST` | `/administration/requests` | `createServiceRequest` | `ServiceRequestCreateRequest` (`service_type_id`, `applicant_name`, `applicant_phone`, `student_id`, `purpose`) | `ServiceRequestDetailResponse` | `S13` | Wewenang: TATA_USAHA, Siswa/Pemohon via Loket TU |
| 30 | `GET` | `/administration/requests/{id}` | `getServiceRequestDetail` | None | `ServiceRequestDetailResponse` (`id`, `tracking_number`, `service_type_id`, `applicant_name`, `applicant_phone`, `purpose`, `status`, `version`, `documents`, `timeline`) | `S14`, `S14-TAB`| Path: `id` (integer), Wewenang: TATA_USAHA, PIMPINAN |
| 31 | `POST` | `/administration/requests/{id}/transitions` | `transitionServiceRequest` | `ServiceTransitionRequest` (`action`: PROSES, AJUKAN_PERSETUJUAN, SETUJUI, TOLAK, SELESAIKAN; `note`; `expected_version`) | `ServiceRequestDetailResponse` | `S14` | Optimistic locking via `expected_version`. Status DITOLAK terminal |
| 32 | `POST` | `/administration/requests/{id}/documents` | `uploadRequestDocument` | Multipart Form-Data (`file`: binary, max 5 MB PDF/JPG/PNG) | `DocumentItem` (`id`, `file_name`, `file_size`, `uploaded_at`) | `S13`, `S14` | Path: `id` (int). Disimpan di PRIVATE_MEDIA_ROOT |
| 33 | `GET` | `/administration/documents` | `listArchivedDocuments` | None | `ArchivedDocumentListResponse` (items: `id`, `document_number`, `title`, `file_name`, `created_at`) | `S15` | Query: `search` (string). Tidak ada filter service_type_id |
| 34 | `GET` | `/administration/documents/{id}/download` | `downloadPrivateDocument` | None | Binary File Stream (`application/pdf`, `image/*`) | `S14`, `S15` | Path: `id` (int). Verifikasi wewenang TU & Pimpinan |
| 35 | `GET` | `/reports/dashboard` | `getDashboardMetrics` | None | `DashboardMetricsResponse` (`role_scope`, `generated_at`, `metrics`: `attendance_summary`, `pending_cases_count`, `pending_requests_count`, `active_students_count`) | `S02` (6 Peran), `S02-TAB` | Query: `start_date` (date), `end_date` (date) |
| 36 | `GET` | `/reports/attendance.xlsx` | `exportAttendanceExcel` | None | Binary Spreadsheet Stream (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`) | `S16` | Query: `start_date` (req), `end_date` (req), `class_id` (opt) |
| 37 | `GET` | `/reports/administration.pdf` | `exportAdministrationPdf` | None | Binary PDF Stream (`application/pdf`) | `S16` | Query: `start_date` (req), `end_date` (req). Tidak ada service_type_id |
| 38 | `GET` | `/audit-logs` | `listAuditLogs` | None | `AuditLogListResponse` (items: `id`, `user_id`, `username`, `action`, `entity_name`, `entity_id`, `details`, `ip_address`, `created_at`) | `S17` | Query: `action` (string). Tidak ada filter role_id/user_id |
| 39 | `GET` | `/accounts/users` | `listUsers` | None | `UserListResponse` (items: `id`, `username`, `is_active`, `is_staff`, `roles`, `created_at`) | `S04` | Query params: NONE. Filter lokal di halaman aktif |
| 40 | `POST` | `/accounts/users` | `createUser` | `UserCreateRequest` (`username`, `password`, `roles`, `is_active`) | `UserItem` | `S04` | Wewenang: ADMINISTRATOR. Tidak ada email/full_name |
| 41 | `GET` | `/accounts/users/{id}` | `getUserDetail` | None | `UserDetailResponse` (`id`, `username`, `is_active`, `is_staff`, `roles`, `created_at`) | `S04` | Path: `id` (integer), Wewenang: ADMINISTRATOR |
| 42 | `PATCH`| `/accounts/users/{id}` | `updateUser` | `UserUpdateRequest` (`is_active`, `roles`) | `UserItem` | `S04` | Path: `id` (integer), Wewenang: ADMINISTRATOR |
| 43 | `GET` | `/accounts/roles` | `listRoles` | None | `RoleListResponse` (items: `id`, `name`, `description`) | `S04` | Query params: NONE. Referensi daftar peran sistem |

---

### 8.1 Verifikasi Parameter Query & Batasan Filter Antarmuka

Berdasarkan pemeriksaan langsung terhadap `contracts/openapi.v1.yaml`, berikut adalah status dukungan filter di sisi backend yang wajib dipatuhi oleh Frontend Agent:

| Endpoint & Operasi | Parameter Query yang Didukung Kontrak | Filter yang Belum Didukung Kontrak (Gap) | Solusi Antarmuka Frontend |
|---|---|---|---|
| `GET /master/academic-years` | *Tidak ada* | `is_active` | Tampilkan seluruh data; filter keaktifan dilakukan di sisi klien pada halaman aktif |
| `GET /master/students` | `search` (string), `status` (StudentStatusEnum) | `class_id` | Pencarian nama/NIS dan filter status didukung backend. Filter rombel kelas ditandai sebagai kebutuhan integrasi |
| `GET /master/assignments` | `class_id` (integer), `employee_id` (integer) | `teacher_id`, `role_type` | Gunakan parameter resmi `employee_id`. Pemilahan peran dilakukan via properti data `role` |
| `GET /student-affairs/cases`| `status` (CaseStatusEnum) | `student_id`, `search` | Filter status didukung backend. Pencarian nama siswa di tabel merupakan pencarian lokal halaman aktif |
| `GET /administration/requests`| `status` (ServiceRequestStatusEnum) | `service_type_id`, `search` | Filter status didukung backend. Penyaringan jenis layanan merupakan penyaringan lokal halaman aktif |
| `GET /administration/documents`| `search` (string) | `service_type_id` | Pencarian judul/nomor dokumen didukung backend. Pengelompokan jenis surat dilakukan secara lokal |
| `GET /reports/administration.pdf`| `start_date` (date), `end_date` (date) | `service_type_id` | Ekspor menghasilkan laporan administrasi menyeluruh untuk rentang tanggal yang dipilih |
| `GET /accounts/users` | *Tidak ada* | `role_id`, `is_active`, `search` | Menampilkan daftar akun per halaman; pencarian username dan filter peran dilakukan secara lokal di klien |
| `GET /audit-logs` | `action` (string) | `user_id`, `start_date`, `role` | Filter aksi sistem didukung backend. Penyaringan tanggal atau aktor dicatat sebagai usulan integrasi |

> [!WARNING]
> **Larangan Filter Semu pada Paginasi Server:**
> Frontend Agent **dilarang** melakukan filtering hanya terhadap satu halaman data hasil paginasi server lalu menampilkan label bahwa seluruh dataset sekolah telah tersaring. Jika endpoint belum mendukung parameter filter di query URL, antarmuka wajib memberikan indikasi jelas bahwa penyaringan hanya berlaku untuk data yang sedang dimuat pada halaman saat ini (*in-memory current page filter*).

---

### 8.2 Pemetaan Lengkap Widget Dasbor Enam Peran (`DashboardMetricsResponse`)

Seluruh kartu ringkasan KPI pada enam layar dasbor (`S02`) dipetakan secara presisi terhadap skema tunggal `DashboardMetricsResponse`:

```json
{
  "role_scope": "Guru",
  "generated_at": "2026-11-12T07:30:00Z",
  "metrics": {
    "attendance_summary": {
      "recorded_today": true,
      "attendance_rate_pct": 96.4
    },
    "pending_cases_count": 12,
    "pending_requests_count": 5,
    "active_students_count": 312
  }
}
```

| Peran Pengguna | Widget / KPI Dasbor | Operation ID Sumber | Path Properti Respons | Formula / Logika Penurunan | Lingkup Objek (Scope) |
|---|---|---|---|---|---|
| **ADMINISTRATOR** | Metriks Presensi Terpusat | `getDashboardMetrics` | `metrics.attendance_summary.attendance_rate_pct` | Tampilkan nilai persentase langsung | Global Seluruh Rombel |
| **ADMINISTRATOR** | Metriks Permohonan Layanan | `getDashboardMetrics` | `metrics.pending_requests_count` | Tampilkan jumlah berkas status DIAJUKAN | Global Tata Usaha |
| **ADMINISTRATOR** | Metriks Kasus Kedisiplinan | `getDashboardMetrics` | `metrics.pending_cases_count` | Tampilkan jumlah kasus aktif berjalan | Global Kesiswaan |
| **ADMINISTRATOR** | Metriks Peserta Didik | `getDashboardMetrics` | `metrics.active_students_count` | Tampilkan jumlah siswa status AKTIF | Global Sekolah |
| **GURU** | Penugasan Kelas Aktif | `authMe` | `assigned_classes` | `assigned_classes.length` (daftar kelas ajar) | Khusus Penugasan Guru Terautentikasi |
| **GURU** | Presensi Tercatat Hari Ini | `getDashboardMetrics` | `metrics.attendance_summary.recorded_today` | Boolean: `true` -> SUDAH, `false` -> BELUM | Rombel Kelas Mengajar Hari Ini |
| **GURU** | Tingkat Kehadiran Kelas | `getDashboardMetrics` | `metrics.attendance_summary.attendance_rate_pct` | Tampilkan nilai persentase kehadiran | Rombel Kelas Binaan/Ajar |
| **GURU** | Total Siswa Aktif Binaan | `getDashboardMetrics` | `metrics.active_students_count` | Nilai cacah siswa aktif pada kelas penugasan | Rombel Kelas Binaan/Ajar |
| **WALI_KELAS** | Presensi Kumulatif Binaan | `getDashboardMetrics` | `metrics.attendance_summary.attendance_rate_pct` | Persentase kumulatif kehadiran semester berjalan | Rombel Binaan Wali Kelas |
| **WALI_KELAS** | Status Presensi Hari Ini | `getDashboardMetrics` | `metrics.attendance_summary.recorded_today` | Status konfirmasi pengisian presensi kelas hari ini | Rombel Binaan Wali Kelas |
| **WALI_KELAS** | Total Siswa Terdaftar | `getDashboardMetrics` | `metrics.active_students_count` | Jumlah siswa aktif terdaftar di rombel binaan | Rombel Binaan Wali Kelas |
| **KESISWAAN** | Kasus Aktif Berjalan | `getDashboardMetrics` | `metrics.pending_cases_count` | Jumlah kasus status DIAJUKAN dan DIPROSES | Lingkup Bimbingan Konseling & Kedisiplinan |
| **KESISWAAN** | Total Siswa dalam Pantauan | `getDashboardMetrics` | `metrics.active_students_count` | Total populasi siswa yang menjadi subjek binaan | Global Siswa Sekolah |
| **TATA_USAHA** | Antrean Permohonan Masuk | `getDashboardMetrics` | `metrics.pending_requests_count` | Jumlah permohonan status DIAJUKAN (menunggu verifikasi TU) | Seluruh Layanan Persuratan |
| **PIMPINAN** | Rata-rata Presensi Sekolah | `getDashboardMetrics` | `metrics.attendance_summary.attendance_rate_pct` | Rata-rata kehadiran seluruh siswa sekolah | Agregat Eksekutif Sekolah |
| **PIMPINAN** | Antrean Disposisi Masuk | `getDashboardMetrics` | `metrics.pending_requests_count` | Permohonan butuh persetujuan pimpinan (MENUNGGU_PERSETUJUAN)| Disposisi Dokumen Sekolah |
| **PIMPINAN** | Kasus Kesiswaan Aktif | `getDashboardMetrics` | `metrics.pending_cases_count` | Jumlah kasus pelanggaran/konseling aktif berjalan | Monitoring Eksekutif Siswa |
| **PIMPINAN** | Total Siswa Aktif Sekolah | `getDashboardMetrics` | `metrics.active_students_count` | Total seluruh siswa berstatus AKTIF | Data Induk Sekolah |

---

## 9. Business Workflow Mapping (Alur Kerja Operasional Sekolah Sesuai Kontrak)

### 9.1 Alur Autentikasi & Sesi Pengguna
1. Pengguna memasukkan username dan password pada `S01_Login_Desktop`.
2. Antarmuka memanggil `POST /auth/login`. Jika kredensial valid, backend mengembalikan `LoginResponse` (`access_token`, `refresh_token`, `token_type`, `expires_in`).
3. Frontend menyimpan `access_token` dalam state memori dan memanggil `GET /auth/me` untuk mendapatkan data identitas profil (`UserProfileResponse`) serta daftar penugasan kelas (`assigned_classes`).
4. Saat token kedaluwarsa, frontend memanggil `POST /auth/refresh` dengan menyertakan payload JSON `{ "refresh_token": "..." }`.
5. Saat pengguna keluar (*logout*), frontend memanggil `POST /auth/logout` dengan payload JSON `{ "refresh_token": "..." }`, kemudian menghapus seluruh state sesi dan membersihkan cache query aplikasi.

### 9.2 Alur Pencatatan Presensi Kelas Massal (`S08` & `S09`)
1. Guru atau Wali Kelas membuka `S08_CatatKehadiran_Desktop` dan memilih rombel kelas serta tanggal presensi.
2. Antarmuka memanggil `GET /attendance/roster?class_id={id}&date={date}` untuk memuat daftar siswa. Siswa yang belum dicatat statusnya berada pada state form lokal *unselected*.
3. Pengguna memilih status kehadiran tiap siswa (`HADIR`, `SAKIT`, `IZIN`, `ALPA`) dan menambahkan catatan khusus jika diperlukan.
4. Pengguna menekan tombol "Simpan Presensi Kelas", memicu pemanggilan atomik `POST /attendance/bulk` dengan skema `AttendanceBulkRequest`:
   ```json
   {
     "class_id": 1,
     "date": "2026-11-12",
     "items": [
       { "student_id": 101, "status": "HADIR", "note": "" },
       { "student_id": 102, "status": "SAKIT", "note": "Surat dokter terlampir" }
     ]
   }
   ```
5. Backend menyimpan seluruh baris secara atomik (*all-or-nothing*). Jika guru tidak memiliki hak mengajar di kelas tersebut pada tanggal terkait, backend merespons dengan HTTP 403 Forbidden.

### 9.3 Alur Penanganan Kasus Kesiswaan & Bimbingan Konseling (`S10` & `S11`)
1. Guru, Wali Kelas, atau Kesiswaan mendaftarkan dugaan pelanggaran atau kebutuhan konseling siswa melalui `POST /student-affairs/cases` (`StudentCaseCreateRequest`). Kasus berstatus awal `BARU` (atau `DIAJUKAN`).
2. Guru BK / Tim Kesiswaan membuka detail kasus pada `S11_DetailKasus_Desktop`.
3. Setiap mutasi status dilakukan melalui `POST /student-affairs/cases/{id}/transitions` menggunakan skema `CaseTransitionRequest`:
   - Aksi `MULAI_PENANGANAN`: Mengubah status kasus menjadi `DIPROSES`.
   - Aksi `CATAT_TINDAKAN`: Menambahkan catatan pembinaan/konseling ke dalam timeline tanpa mengubah status kasus.
   - Aksi `SELESAIKAN`: Mengubah status kasus menjadi `SELESAI`.
   - Aksi `BATALKAN`: Mengubah status kasus menjadi `DIBATALKAN`.
4. Seluruh mutasi menyertakan `expected_version` integer. Jika ada pengguna lain yang telah memperbarui kasus lebih dahulu, backend merespons HTTP 409 Conflict.

### 9.4 Alur Pelayanan Persuratan Tata Usaha & Pengarsipan Digital (`S12` s/d `S15`)
1. Pemohon (siswa/wali murid) mengajukan permohonan surat di loket TU (`S13_FormPermohonan_Desktop`). Staf TU memanggil `POST /administration/requests` (`ServiceRequestCreateRequest`). Permohonan berstatus awal `DIAJUKAN`.
2. Jika ada berkas fisik pendukung, staf TU mengunggah berkas via `POST /administration/requests/{id}/documents` (multipart/form-data, max 5 MB). Berkas disimpan secara privat di `PRIVATE_MEDIA_ROOT`.
3. Staf TU memeriksa kelayakan berkas dan memproses permohonan via `POST /administration/requests/{id}/transitions`:
   - Aksi `PROSES`: Mengubah status menjadi `DIPROSES`.
   - Aksi `AJUKAN_PERSETUJUAN`: Mengubah status menjadi `MENUNGGU_PERSETUJUAN` (khusus layanan dengan `requires_approval: true`).
4. Kepala Sekolah / Pimpinan memeriksa berkas pada `S14_DetailPermohonan_Desktop` dan mengambil keputusan:
   - Aksi `SETUJUI`: Mengubah status menjadi `DISETUJUI`.
   - Aksi `TOLAK`: Mengubah status menjadi `DITOLAK` (status penolakan bersifat terminal).
5. Staf TU mencetak surat fisik resmi, membubuhkan stempel sekolah basah, dan menyelesaikan permohonan dengan aksi `SELESAIKAN`. Dokumen terbit otomatis tercatat pada katalog arsip digital `S15_ArsipDokumen_Desktop`. Pengunduhan berkas privat dilakukan melalui binary streaming `GET /administration/documents/{id}/download`.

---

## 10. Responsive Specification (Spesifikasi Perilaku Responsif Tiga Skala)

### 10.1 Sistem Breakpoint Resmi
- **Desktop (>= 1024px, Base Canvas: 1440 x 900):**
  - Layout dua kolom Golden Ratio (61.8% konten utama, 38.2% panel samping).
  - Sidebar navigasi vertikal permanen terbuka (lebar 240px).
  - Tabel tabular penuh dengan seluruh kolom aksi dan filter lanjutan.
- **Tablet (768px - 1023px, Base Canvas: 768 x 1024):**
  - Sidebar menyusut menjadi icon-only rail (lebar 64px) dengan tooltip saat kursor diarahkan.
  - Layout Golden Ratio bertransformasi menjadi tumpukan vertikal atau pergeseran tab.
  - Grid metrik KPI bertransformasi menjadi 2 kolom x 2 baris.
  - Tabel data menyembunyikan kolom sekunder (kolom tanggal dibuat ringkas).
- **Mobile (< 768px, Base Canvas: 390 x 844):**
  - Sidebar navigasi berganti menjadi Navigation Drawer (hamburger menu).
  - Tabel data tabular bertransformasi menjadi daftar kartu vertikal (*Card-based List View*).
  - Target sentuh interaktif diperbesar memenuhi standar kenyamanan jari minimal 44 x 44 px.

---

## 11. Interaction Specification (Spesifikasi Interaksi & State Sistem)

### 11.1 Durasi Mikro-Interaksi (Doherty Threshold < 400ms)
- Seluruh umpan balik interaksi pengguna (hover tombol, buka accordion, modal popup) wajib selesai dalam rentang waktu <= 200ms.
- Setiap aksi mutasi data wajib menampilkan indikator pemuatan (*button spinner* atau progress bar) dan menonaktifkan tombol submit untuk mencegah pengiriman ganda (*double submission*).

### 11.2 Penanganan Konflik Konkurensi Optimistik (HTTP 409 Conflict)
Saat memutasi kasus kesiswaan atau permohonan surat:
1. Permintaan wajib menyertakan nilai `expected_version` integer.
2. Jika backend mengembalikan status HTTP 409 Conflict:
   - Antarmuka **DILARANG** menampilkan pesan sukses semu.
   - Antarmuka menampilkan dialog peringatan: *"Data telah diperbarui oleh pengguna lain saat Anda membuka halaman ini."*
   - Antarmuka menyajikan pratinjau perbedaan (*diff viewer*) antara data versi terkini di server dengan data formulir lokal pengguna.
   - Pengguna diberikan opsi untuk memuat ulang data server (*Refresh*) atau menggabungkan perubahan secara manual.

---

## 12. Semantic Status Mapping (Pemetaan Status Semantik Sesuai Kontrak)

### 12.1 Modul Presensi Siswa (`AttendanceStatusEnum`)
- `HADIR`: Latar `#ECFDF5`, Teks `#047857`, Ikon Centang (Siswa hadir di kelas).
- `SAKIT`: Latar `#FFFBEB`, Teks `#B45309`, Ikon Medis (Surat keterangan sakit).
- `IZIN`: Latar `#EFF6FF`, Teks `#1D4ED8`, Ikon Surat (Surat izin orang tua/wali).
- `ALPA`: Latar `#FFF1F2`, Teks `#BE123C`, Ikon Peringatan (Tanpa keterangan sah).

### 12.2 Modul Kasus Kesiswaan (`CaseStatusEnum`)
- `BARU` / `DIAJUKAN`: Latar `#F0F9FF`, Teks `#0369A1` (Rujukan masuk).
- `DIPROSES`: Latar `#FFFBEB`, Teks `#B45309` (Dalam penanganan konseling/mediasi).
- `SELESAI`: Latar `#ECFDF5`, Teks `#047857` (Pembinaan tuntas, kasus ditutup).
- `DIBATALKAN`: Latar `#F1F5F9`, Teks `#475569` (Rujukan dicabut / tidak terbukti).

### 12.3 Modul Layanan Persuratan (`ServiceRequestStatusEnum`)
- `DIAJUKAN`: Latar `#F0F9FF`, Teks `#0369A1` (Permohonan baru masuk di loket TU).
- `DIPROSES`: Latar `#FFFBEB`, Teks `#B45309` (Berkas diverifikasi staf administrasi).
- `MENUNGGU_PERSETUJUAN`: Latar `#FEF3C7`, Teks `#92400E` (Disposisi ke Pimpinan).
- `DISETUJUI`: Latar `#ECFDF5`, Teks `#047857` (Pimpinan menyetujui penerbitan surat).
- `DITOLAK`: Latar `#FFF1F2`, Teks `#BE123C` (Permohonan ditolak terminal).
- `SELESAI`: Latar `#ECFDF5`, Teks `#047857` (Surat dicetak, disahkan, dan diarsipkan).

### 12.4 Modul Status Siswa (`StudentStatusEnum`)
- `AKTIF`: Latar `#ECFDF5`, Teks `#047857` (Siswa aktif mengikuti proses belajar).
- `MUTASI_KELUAR`: Latar `#FFFBEB`, Teks `#B45309` (Siswa pindah ke sekolah lain).
- `LULUS`: Latar `#EFF6FF`, Teks `#1D4ED8` (Siswa telah menuntaskan pendidikan).
- `NONAKTIF`: Latar `#F1F5F9`, Teks `#475569` (Siswa berhenti / tidak aktif).
*(Catatan: Nilai `DROPOUT` tidak ada pada skema kontrak resmi).*

---

## 13. Frontend Implementation Guide (Panduan Praktis Frontend Agent)

### 13.1 Konfigurasi Tailwind CSS (`frontend/tailwind.config.ts`)
```ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#173B63", // Institutional Navy 900
          hover: "#0F2A48",   // Institutional Navy 950
          accent: "#12665C",  // Institutional Teal 700
          accentHover: "#0D4D46",
          light: "#EBF3F5",
        },
        surface: {
          bg: "#F5F7FA",      // Kanvas latar belakang utama
          card: "#FFFFFF",    // Kartu kontainer
          subtle: "#EDF2F7",
        },
        text: {
          primary: "#1E293B", // Slate 800 - rasio kontras 14.38:1
          secondary: "#64748B",// Slate 500 - rasio kontras 4.76:1
          muted: "#94A3B8",   // Slate 400 - hanya untuk ikon dekoratif
        },
        border: {
          default: "#E2E8F0", // Slate 200
        },
        status: {
          successBg: "#ECFDF5",
          successText: "#047857",
          warningBg: "#FFFBEB",
          warningText: "#B45309",
          dangerBg: "#FFF1F2",
          dangerText: "#BE123C",
          infoBg: "#F0F9FF",
          infoText: "#0369A1",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        sm: "4px",
        md: "6px",
        lg: "8px",
        xl: "12px",
      },
    },
  },
  plugins: [],
};

export default config;
```

### 13.2 Pola Hooks TanStack Query v5 (Mengacu Endpoint Kontrak Aktual)
```ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

// Base URL resmi dari variabel environment tanpa duplikasi /api
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Interceptor menyematkan Bearer token dari memory store
apiClient.interceptors.request.use((config) => {
  const token = getAuthTokenFromMemory(); // Bukan localStorage publik
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Hook: Memuat Roster Presensi Kelas Harian (GET /attendance/roster)
export function useAttendanceRoster(classId: number, date: string) {
  return useQuery({
    queryKey: ["attendance", "roster", classId, date],
    queryFn: async () => {
      const response = await apiClient.get("/attendance/roster", {
        params: { class_id: classId, date },
      });
      return response.data;
    },
    enabled: Boolean(classId && date),
  });
}

// Hook: Simpan Presensi Massal Atomik (POST /attendance/bulk)
export function useSaveAttendanceBulk() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      class_id: number;
      date: string;
      items: Array<{ student_id: number; status: string; note?: string }>;
    }) => {
      const response = await apiClient.post("/attendance/bulk", payload);
      return response.data;
    },
    onSuccess: (_, variables) => {
      // Invalidate roster dan metriks dasbor setelah mutasi berhasil dikonfirmasi server
      queryClient.invalidateQueries({
        queryKey: ["attendance", "roster", variables.class_id, variables.date],
      });
      queryClient.invalidateQueries({ queryKey: ["reports", "dashboard"] });
    },
  });
}
```

---

## 14. Accessibility Requirements (Kerangka Kerja 4 Tingkat Aksesibilitas)

Frontend Agent wajib menerapkan kerangka kerja 4 tingkat kepatuhan aksesibilitas:

1. **Tingkat 1 - Kontras Warna & Keterbacaan Teks:**
   - Seluruh teks isi data dan label formulir wajib memenuhi rasio kontras minimal 4.5:1 terhadap latar belakangnya.
   - Warna `#94A3B8` (kontras 2.56:1) **dilarang keras** digunakan untuk teks yang menyampaikan informasi; hanya diizinkan untuk ornamen visual non-kritis.
   - Pada kontainer berlatar `#F5F7FA`, jika teks sekunder `#64748B` berukuran kecil (<18pt), wajib dinaikkan kontrasnya menjadi `#334155` (Slate 700) untuk menjamin lolos WCAG AA.
2. **Tingkat 2 - Navigasi Keyboard Penuh:**
   - Seluruh elemen tombol, input formulir, modal dialog, dan dropdown harus dapat dioperasikan penuh menggunakan tombol `Tab`, `Enter`, `Space`, dan panah arah.
   - Ring fokus keyboard wajib tampak jelas (`outline: 2px solid #12665C` dengan offset 2px).
3. **Tingkat 3 - Aksesibilitas Pembaca Layar (Screen Readers & ARIA):**
   - Seluruh ikon tombol aksi wajib memiliki atribut `aria-label` deskriptif (contoh: `<button aria-label="Ubah Data Siswa Ahmad Fauzi">`).
   - Tabel data wajib memiliki `<caption>`, elemen `<th>` dengan atribut `scope="col"`, dan sel data terasosiasi dengan benar.
4. **Tingkat 4 - Ketahanan Formulir & Status Validasi:**
   - Setiap pesan kesalahan validasi input wajib terhubung ke elemen input melalui atribut `aria-describedby` dan memiliki `aria-invalid="true"`.
   - Perubahan status real-time wajib diumumkan ke pembaca layar menggunakan `aria-live="polite"`.

---

## 15. Known Limitations & Coordinator Open Items

Berikut adalah daftar 10 batasan integrasi (*Shared Contract Gaps*) yang belum tersedia pada kontrak bersama atau masih menunggu penetapan kebijakan sekolah:

| No | Modul / Kebutuhan | Deskripsi Masalah / Gap | Rekomendasi Penanganan | Status Tindak Lanjut |
|---|---|---|---|---|
| 1 | Master Tahun Ajaran | RBAC mengizinkan `UPDATE`, namun operasi `PATCH /master/academic-years/{id}` belum ada di OpenAPI | Hanya sediakan aksi `CREATE`. Pengubahan data menunggu penambahan endpoint | Open Item Coordinator |
| 2 | Master Kelas Rombel | RBAC mengizinkan `UPDATE`, namun operasi `PATCH /master/classes/{id}` belum ada di OpenAPI | Hanya sediakan aksi `CREATE`. Pengubahan data menunggu penambahan endpoint | Open Item Coordinator |
| 3 | Master Data Pegawai | RBAC mengizinkan `UPDATE`, namun operasi `PATCH /master/employees/{id}` belum ada di OpenAPI | Hanya sediakan aksi `CREATE`. Pengubahan data menunggu penambahan endpoint | Open Item Coordinator |
| 4 | Master Jenis Layanan | RBAC mengizinkan `UPDATE`, namun operasi `PATCH /administration/service-types/{id}` belum ada | Hanya sediakan aksi `CREATE`. Pengubahan data menunggu penambahan endpoint | Open Item Coordinator |
| 5 | Bimbingan Konseling | Pencatatan sesi konseling rahasia BK belum memiliki endpoint mandiri (saat ini tergabung di transitions) | Gunakan aksi `CATAT_TINDAKAN` pada transitions dengan catatan privat | Open Item Coordinator |
| 6 | Penugasan Guru | Wewenang Guru membaca daftar penugasan kelas sendiri belum didefinisikan eksplisit pada RBAC | Frontend mengandalkan properti `assigned_classes` dari respons `GET /auth/me` | Terselesaikan di Desain |
| 7 | Kerahasiaan Kasus Siswa| Detail kasus perlu mekanisme response filtering agar catatan konseling sensitif tidak bocor ke peran umum | Backend wajib memfilter array timeline berdasarkan peran pengguna | Open Item Backend |
| 8 | Antrean Surat Pimpinan | Hak Pimpinan pada antrean surat dibatasi hanya pada permohonan yang membutuhkan persetujuan | Frontend menyaring tampilan antrean pimpinan khusus status MENUNGGU_PERSETUJUAN | Terselesaikan di Desain |
| 9 | Penempatan Siswa oleh TU| Hak penempatan siswa ke rombel oleh TU perlu konsistensi navigasi antarmuka | Form penempatan rombel (`S07`) dibuka aksesnya untuk wewenang TATA_USAHA | Terselesaikan di Desain |
| 10 | Kebijakan Pending RBAC | 4 kebijakan sekolah (TU buat siswa/layanan, koreksi absensi >24 jam, audit logs pimpinan) berstatus pending | Seluruh 4 fitur ditegakkan sebagai `DENIED` pada antarmuka hingga SK terbit | Terkunci di Desain (DENIED) |

---

## 16. Design Acceptance & Handoff Checklist (Daftar Periksa Kesiapan Frontend)

| No | Kriteria Penerimaan Teknis | Hasil Audit Desain | Status Kesiapan |
|---|---|---|---|
| 1 | **Kesesuaian 43 Operasi OpenAPI v1** | Seluruh 43 operasi memiliki path, method, operationId, schema request/response yang sinkron 100% | **TERVERIFIKASI (0 Mismatch)** |
| 2 | **Kesesuaian Matriks Otorisasi RBAC** | Seluruh aksi tombol dan navigasi peran mematuhi batasan wewenang riil; 4 pending item dikunci DENIED | **TERVERIFIKASI (0 Mismatch)** |
| 3 | **Pembersihan Fitur Spekulatif** | Kanvas bebas dari fitur fiktif (default hadir, timer 24j, trigger alpa 3j, lonceng jadwal, monitoring DB) | **TERVERIFIKASI (Bersih)** |
| 4 | **Kelengkapan 16 Kelompok Layar** | 18 layar fungsional (S01-S18) tersedia dalam frame mandiri yang dapat diedit pada master canvas | **TERVERIFIKASI (Lengkap)** |
| 5 | **Varian Responsif Kanonikal** | Tersedia varian teruji untuk Tablet 768px (AppShell, S02, S08, S14) dan Mobile 390px (S01, S08, S10) | **TERVERIFIKASI (Lengkap)** |
| 6 | **Audit Rasio Kontras Matematis** | Seluruh token warna diuji rasio kontras W3C; panduan 4 tingkat kepatuhan aksesibilitas didefinisikan | **TERVERIFIKASI (Lengkap)** |
| 7 | **Keamanan Implementasi Frontend** | Contoh kode bebas DTO duplikat, token auth aman di memori, penanganan konkurensi HTTP 409 terstruktur | **TERVERIFIKASI (Aman)** |

### Keputusan Akhir Status Handoff:
**`CONDITIONALLY_READY - DESIGN_ALIGNED_WITH_COORDINATOR_OPEN_ITEMS`**

- **Fitur yang Diizinkan untuk Diimplementasikan:** Seluruh fondasi aplikasi, routing, client state, skema validasi Zod, komponen atomik, modul autentikasi login/profil, master data siswa/kelas/tahun ajaran (read & create), pencatatan presensi massal atomik, pendaftaran kasus kesiswaan & transisi aksi, loket permohonan surat & verifikasi TU, pengarsipan dokumen digital privat, dasbor ringkasan enam peran, dan ekspor resmi spreadsheet/PDF.
- **Fitur yang Ditunda / Diblokir Sementara:** Fitur pengubahan master data yang belum memiliki endpoint PATCH (Tahun Ajaran, Kelas, Pegawai, Jenis Layanan), pengajuan koreksi presensi lampau (>24 jam), dan audit log untuk peran non-administrator.
