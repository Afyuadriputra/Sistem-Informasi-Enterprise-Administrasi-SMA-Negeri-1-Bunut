# Implementation Plan Document (IPD)

**Status:** Rencana implementasi bertahap mengacu metodologi Design Science Research Methodology (DSRM) enam bulan dengan strategi pengembangan independen multi-jalur (*multi-track contract-first development*) dan tata kelola integrasi berkelanjutan.

---

## 1. Tahap Penelitian dan Luaran (DSRM & TOGAF Roadmap)

| Tahap | Perkiraan | Kegiatan Utama | Luaran / Kriteria Selesai |
|---|---|---|---|
| 0. Persiapan | Bulan 1 | Perizinan sekolah, identifikasi stakeholder, telaah literatur | Surat izin riset dan rencana studi lapangan tersedia |
| 1. Penemuan Kebutuhan | Bulan 1-2 | Observasi, wawancara, inventarisasi data/proses, pemetaan as-is | Dokumen kebutuhan tervalidasi dan proses prioritas disepakati |
| 2. Arsitektur Enterprise | Bulan 2-3 | Penerapan TOGAF ADM: visi, arsitektur bisnis, data, aplikasi, teknologi | Blueprint EA dan matriks keterlacakan ditinjau stakeholder |
| 3. Fondasi Teknis & Kontrak | Bulan 3 | Pembekuan kontrak dasar, inisialisasi Django Ninja, React Vite, & Pencil MCP | Baseline kontrak disetujui; 3 jalur produksi siap berjalan mandiri |
| 4. Konstruksi Paralel Multi-Track | Bulan 4-5 | Pengembangan 3 jalur independen (Design, Backend, Frontend) per modul | Skenario A (Presensi & Kasus) dan Skenario B (Layanan TU) selesai |
| 5. Pengujian & Evaluasi DSRM | Bulan 5 | Uji black box, integrasi API, review arsitektur, UAT, SUS, dan efisiensi | Bukti evaluasi tercatat objektif sesuai protokol uji DSRM |
| 6. Analisis & Penyusunan Tesis | Bulan 5-6 | Analisis data uji, pembahasan keterbatasan, perumusan rekomendasi | Laporan tesis lengkap menghubungkan artefak DSRM dan bukti empiris |

---

## 2. Struktur Jalur Produksi Independen (Three-Track + Integration Architecture)

Konstruksi prototype sistem dibagi menjadi **tiga jalur produksi independen** ditambah satu **jalur koordinasi & integrasi** yang dipandu oleh batas kontrak API dan skema basis data:

```text
[Jalur Kontrak]:       OpenAPI v1 & DBML (Module-by-Module Readiness) ─────────────┐
                                  │                     │                          │
                                  ├─────────────────────┼──────────────┐           │
                                  ▼                     ▼              ▼           │
[Jalur Desain UI/UX]:  UX-M1 -> UX-M2 -> UX-M3 -> UX-M4 -> UX-M5 -> UX-M6 -> UX-M7 -> UX-M8
 (Pencil MCP)                     │        │        │        │        │        │   │
                                  │ (Handoff Sign-off)                               │
                                  ▼        ▼        ▼        ▼        ▼        ▼   │
[Jalur Frontend]:      FE-M1 -> FE-M2 -> FE-M3 -> FE-M4 -> FE-M5 -> FE-M6 -> FE-M7 -> FE-M8
 (React TypeScript)               │        │        │        │        │        │   │
                                  ▼        ▼        ▼        ▼        ▼        ▼   │
[Jalur Integrasi]:     INT-M1   INT-M2   INT-M3   INT-M4   INT-M5   INT-M6   INT-M7 -> INT-M8
                                  ▲        ▲        ▲        ▲        ▲        ▲   │
                                  │        │        │        │        │        │   │
[Jalur Backend]:       BE-M1 -> BE-M2 -> BE-M3 -> BE-M4 -> BE-M5 -> BE-M6 -> BE-M7 -> BE-M8
 (Django Ninja & ORM)
```

### 2.1. UI/UX Design Track (Pencil MCP Specialist)
- **Lingkup:** Perancangan antarmuka, token sistem, tata letak Golden Ratio, alur interaksi mikro, dan visualisasi 5 state wajib menggunakan **Pencil MCP** (`pen.dev`). Berkas desain disimpan pada `design/**`.
- **Independensi:** Design Agent bekerja tanpa membutuhkan kode frontend maupun backend yang sedang berjalan.
- **Milestone:**
  - `UX-M1`: Design System Foundations & Tokens (Navy & Teal, tipografi Inter, spacing, shadows, atomik).
  - `UX-M2`: Authentication & Core Shell Layout (S01 Login, S03 Profil, navigasi sidebar & header).
  - `UX-M3`: Master Data Administrative Workflows (S04 Pengguna/Peran, S05 Siswa, S06 Pegawai/Kelas, S07 Penempatan).
  - `UX-M4`: Attendance Operations & Correction Flow (S08 Input Massal Cepat, S09 Rekap, modal koreksi 24 jam).
  - `UX-M5`: Student Affairs & Confidential BK Flow (S10 Kasus Tata Tertib, S11 Catatan Privat Konseling BK).
  - `UX-M6`: Administration & Document Services (S12 Katalog, S13 Form Permohonan, S14 Verifikasi/Persetujuan, S15 Arsip Privat).
  - `UX-M7`: Dashboards & Strategic Analytics (S02 Dashboard Peran, S16 Rekap Eksekutif, S17 Audit Trail).
  - `UX-M8`: Accessibility Review & Design System Handoff (WCAG 2.2 AA audit, token export, design sign-off per modul).

### 2.2. Frontend Development Track (React TypeScript)
- **Lingkup:** Pembangunan Single Page Application (SPA) berbasis React 18+, TypeScript (Strict), Vite, Tailwind CSS, shadcn/ui, TanStack Query, dan Zustand.
- **Independensi:** Frontend Agent dapat memulai fondasi aplikasi, routing, client state, dan form validasi Zod secara mandiri berdasarkan skema kontrak OpenAPI tanpa menunggu backend selesai. Finalisasi styling visual diselaraskan dengan hasil sign-off desain dari Pencil Track.
- **Milestone:**
  - `FE-M1`: Project Foundation, Design Tokens Scaffolding, & Atomic Primitives.
  - `FE-M2`: Authentication UI & Application Shell Layout (S01, S03, S18).
  - `FE-M3`: Master Data Management UI (S04, S05, S06, S07).
  - `FE-M4`: Attendance Recording & Class Recap UI (S08, S09).
  - `FE-M5`: Student Affairs & Case Timeline UI (S10, S11).
  - `FE-M6`: Administration, Approval Workflow, & Document UI (S12-S15).
  - `FE-M7`: Dashboards, Executive Reports, & Audit UI (S02, S16, S17).
  - `FE-M8`: Accessibility Audit, Frontend Hardening, & Polish (WCAG 2.2 AA).

### 2.3. Backend Development Track (Django Modular Monolith)
- **Lingkup:** Pembangunan arsitektur modular monolith menggunakan Django 5.x, Django Ninja, Granian (ASGI), PostgreSQL / SQLite WAL, Redis, dan pengujian independen via pytest.
- **Independensi:** Backend Agent dapat membangun dan menguji seluruh router API, logika bisnis, transaksi atomik, dan keamanan data tanpa bergantung pada penyelesaian desain maupun implementasi frontend.
- **Milestone:**
  - `BE-M1`: Project Foundation, Core Settings, & Exception Envelope.
  - `BE-M2`: Authentication, Custom User Model, & RBAC (`/auth/*`, `/accounts/*`).
  - `BE-M3`: Master Data & Academic Placements (`/master/*`).
  - `BE-M4`: Attendance Module, Bulk Atomic Write, & Simple-History (`/attendance/*`).
  - `BE-M5`: Student Affairs, Case Timeline, & Optimistic Locking (`/student-affairs/*`).
  - `BE-M6`: Administration, Approval Workflow, & Private Documents (`/administration/*`).
  - `BE-M7`: Dashboard Aggregations, Redis Caching, & Reporting (`/reports/*`, `/audit-logs`).
  - `BE-M8`: Backend Hardening, Security IDOR Audit, & Performance Review.

### 2.4. Coordinator / Integration Track
- **Lingkup:** Manajemen repositori, penegakan protokol kontrak, pengujian sambungan HTTP riil (*real API integration*), validasi lintas peran, dan evaluasi kepatuhan DSRM.
- **Milestone:** `INT-M1` s/d `INT-M8`.

---

## 3. Matriks Pengerjaan Paralel Multi-Jalur (Multi-Track Matrix)

| Modul / Domain | Prasyarat Kontrak | Status Desain (Pencil) | Status Frontend | Status Backend | Gerbang Integrasi Nyata |
|---|---|---|---|---|---|
| Fondasi & Konfigurasi | Base OpenAPI Schema & Envelope | `UX-M1` (Mandiri) | `FE-M1` (Mandiri) | `BE-M1` (Mandiri) | `INT-M1: Foundation Gate` |
| Autentikasi & Akun | `/auth/*`, `/accounts/*` (Rev 1.0) | `UX-M2` (Pencil S01/S03) | `FE-M2` (Form/Shell) | `BE-M2` (JWT/RBAC) | `INT-M2: Auth Gate` |
| Master Data Sekolah | `/master/*` (Rev 1.0) | `UX-M3` (Pencil S04-S07) | `FE-M3` (Tabel/Form) | `BE-M3` (ORM/Placement) | `INT-M3: Master Gate` |
| Presensi Kelas (Skenario A) | `/attendance/*` (Rev 1.0) | `UX-M4` (Pencil S08/S09) | `FE-M4` (Grid/Koreksi) | `BE-M4` (Bulk Atomic) | `INT-M4: Attendance Gate` |
| Kasus Kesiswaan | `/student-affairs/*` (Rev 1.0) | `UX-M5` (Pencil S10/S11) | `FE-M5` (Timeline/Privat) | `BE-M5` (State Machine) | `INT-M5: Affairs Gate` |
| Persuratan TU (Skenario B) | `/administration/*` (Rev 1.0) | `UX-M6` (Pencil S12-S15) | `FE-M6` (Katalog/Alur) | `BE-M6` (Workflow/Doc) | `INT-M6: Admin Gate` |
| Laporan & Dashboard | `/reports/*`, `/audit-logs` (Rev 1.0) | `UX-M7` (Pencil S02/S16/S17) | `FE-M7` (Visual Agregat) | `BE-M7` (Redis/Ekspor) | `INT-M7: Reports Gate` |
| Verifikasi Sistem Akhir | Seluruh Kontrak (v1.0.0) | `UX-M8` (Handoff Audit) | `FE-M8` (Hardening) | `BE-M8` (Hardening) | `INT-M8: Full System E2E` |

---

## 4. Gerbang Kesiapan Kontrak Modular (Modular Contract Readiness Gates)

Pekerjaan fondasi dan modul tidak memerlukan seluruh sistem berstatus `FROZEN` secara serempak. Kesiapan kontrak dinilai per modul dan per agen secara terisolasi:

```text
Per-Module Contract Lifecycle:
[DRAFT] -> [IN_REVIEW] -> [APPROVED] -> [FROZEN]
```

### 4.1. Kriteria Kesiapan per Agen
1. **Untuk UI/UX Design Agent:**
   - Prasyarat: Memerlukan kebutuhan fungsional (PRD), alur proses bisnis (AFD), dan tata letak layar (UID).
   - **Bebas Dependensi:** Tidak bergantung pada kode frontend, tipe TypeScript, skema DBML, maupun implementasi backend.
2. **Untuk Backend Agent:**
   - Prasyarat: Endpoint modul, skema request/response payload, tipe data, dan skema database DBML modul bersangkutan telah mencapai status `APPROVED` atau `FROZEN` dengan nomor revisi eksplisit (misal `rev-1.0.0`).
   - **Bebas Dependensi:** Backend sama sekali tidak membutuhkan generated TypeScript frontend, mock fixture, maupun selesainya desain antarmuka.
3. **Untuk Frontend Agent:**
   - Prasyarat: Spesifikasi OpenAPI modul bersangkutan telah mencapai status `APPROVED` atau `FROZEN` untuk keperluan generasi tipe TypeScript dan mocking lokal terisolasi.
   - **Bebas Dependensi Backend:** Frontend tidak memerlukan backend yang sudah diimplementasikan untuk membangun antarmuka dan form validasi.
   - **Finalisasi Visual:** Membutuhkan design sign-off dari Pencil Design Track sebelum status modul dinyatakan siap integrasi akhir.

---

## 5. Protokol Evaluasi Penelitian DSRM & Pengukuran Ilmiah

Sebagai penelitian tesis yang menerapkan metodologi DSRM, evaluasi artefak prototype wajib memiliki bukti empiris yang objektif, terukur, dan bebas bias.

### 5.1. Matriks Pengukuran Konsistensi Data (Data Consistency Metrics)
Konsistensi data antar modul diukur menggunakan tiga formula matematis:

1. **Rasio Keutuhan Referensial Data (Referential Integrity Ratio - RIR):**
   $$\text{RIR} = \left( 1 - \frac{N_{\text{orphaned}}}{N_{\text{total\_foreign\_keys}}} \right) \times 100\%$$
   - Target evaluasi: $\text{RIR} = 100\%$ (Zero orphaned records pada relasi siswa, penempatan, kehadiran, dan surat).
2. **Indeks Duplikasi Entri Data (Data Duplication Index - DDI):**
   $$\text{DDI} = \frac{N_{\text{redundant\_inputs}}}{N_{\text{total\_inputs}}}$$
   - Target evaluasi: $\text{DDI} = 0$ (Informasi siswa dan rombel yang telah dicatat di master data tidak perlu dimasukkan ulang secara manual pada modul presensi maupun persuratan).
3. **Tingkat Keberhasilan Konkurensi Optimistik (Optimistic Concurrency Success Rate - OCSR):**
   $$\text{OCSR} = \frac{N_{\text{valid\_transitions}} + N_{\text{detected\_conflicts}}}{N_{\text{total\_mutations}}} \times 100\%$$
   - Target evaluasi: $\text{OCSR} = 100\%$ (Setiap konflik tabrakan versi menghasilkan status HTTP 409 Conflict dan mencegah *lost update*).

### 5.2. Pengendalian Bias Evaluasi (Evaluation Bias Control)
Untuk menjamin validitas internal dan eksternal penelitian:
1. **Pemilihan Responden Independen:** Evaluasi melibatkan pengguna riil sekolah (minimal 2 guru, 1 wali kelas, 1 staf kesiswaan, 2 staf TU, dan 1 pimpinan) yang tidak terlibat dalam perancangan kode.
2. **Protokol Fasilitator Terstandar (*Standardized Facilitator Script*):** Fasilitator pengujian dilarang memberikan panduan atau petunjuk subjektif selama responden menjalankan tugas evaluasi.
3. **Pengujian Skenario Berpasangan (*Paired Task Testing*):** Mengukur efisiensi waktu penyelesaian tugas antara cara kerja konvensional (baseline manual) dan sistem prototype menggunakan uji statistik inferensial (Paired t-test atau Wilcoxon Signed-Rank Test untuk data non-normal) dengan tingkat signifikansi $\alpha = 0.05$.
4. **Isolasi Evaluator:** Pengisian kuesioner System Usability Scale (SUS) dilakukan secara anonim dan mandiri oleh responden tanpa kehadiran pengembang secara langsung.

### 5.3. Matriks Keterlacakan Kebutuhan (Requirements Traceability Matrix - RTM)
Setiap kebutuhan bisnis ditelusuri secara ketat dari dokumen perencanaan hingga pengujian:

$$\text{PRD (FR-xxx)} \longrightarrow \text{AFD (Flow-xxx)} \longrightarrow \text{DBD/DBML (Table-xxx)} \longrightarrow \text{BSD/OpenAPI (Endpoint-xxx)} \longrightarrow \text{Screen (Sxx)} \longrightarrow \text{Test Suite (TST-xxx)}$$

| Kebutuhan Fungsional (PRD) | Alur Bisnis (AFD) | Tabel Basis Data (DBML) | Kontrak API (OpenAPI) | Screen (UID/Pencil) | Skenario Uji (Test ID) |
|---|---|---|---|---|---|
| `FR-01` Autentikasi & Akun | §1 Login & Logout | `users`, `roles`, `user_roles` | `POST /auth/login`, `POST /auth/refresh` | `S01`, `S03` | `BE-01`, `BE-02`, `FE-01` |
| `FR-02` Data Master & Rombel | §2 Penempatan Rombel | `academic_years`, `school_classes`, `students`, `enrollments` | `GET/POST /master/*` | `S04`, `S05`, `S06`, `S07` | `BE-03`, `FE-03`, `INT-M3` |
| `FR-03` Presensi Harian Siswa | §3 Skenario A Presensi | `attendances`, `historical_attendances` | `GET /attendance/roster`, `POST /attendance/bulk` | `S08`, `S09` | `BE-04`, `BE-05`, `E2E-A1` |
| `FR-04` Kasus & Konseling BK | §3 Skenario A Kasus | `student_cases`, `case_events` | `GET/POST /student-affairs/cases/*` | `S10`, `S11` | `BE-06`, `FE-05`, `E2E-A2` |
| `FR-05` Layanan Persuratan | §4 Skenario B Layanan | `service_types`, `service_requests`, `service_events` | `GET/POST /administration/requests/*` | `S12`, `S13`, `S14` | `BE-07`, `FE-06`, `E2E-B1` |
| `FR-06` Dokumen Privat Aman | §4 Skenario B Berkas | `documents` | `POST .../documents`, `GET .../download` | `S13`, `S14`, `S15` | `BE-08`, `FE-06`, `E2E-B2` |
| `FR-07` Dashboard Operasional | §5 Dashboard Ringkasan | View Agregat / Redis Cache | `GET /reports/dashboard` | `S02` | `BE-09`, `FE-07`, `E2E-R1` |
| `FR-08` Rekapitulasi Eksekutif | §5 Laporan Berkala | Kueri Teragregasi | `GET /reports/attendance.xlsx`, `GET /reports/administration.pdf` | `S16` | `BE-10`, `FE-07`, `E2E-R1` |
| `FR-09` Audit Trail Aktivitas | §5 Audit Keamanan | `activity_logs`, `historical_*` | `GET /audit-logs` | `S17` | `BE-05`, `FE-07`, `INT-M7` |

---

## 6. Gerbang Evaluasi Penelitian (Research Evaluation Gates)

| Gerbang Evaluasi | Fokus Pengujian | Indikator Keberhasilan | Target Evaluasi |
|---|---|---|---|
| **Gate E1: Technical Gate** | Fungsionalitas API, keamanan IDOR, transaksi atomik, dan build frontend | 100% test suite backend dan frontend lulus | Zero critical defect, 100% kontrak patuh |
| **Gate E2: Usability Gate** | Pengukuran kemudahan antarmuka dan kepuasan peran pengguna | Kuesioner System Usability Scale (SUS) | Skor rata-rata SUS >= 68 (Kategori Good) |
| **Gate E3: Acceptance Gate** | Kesesuaian alur kerja Skenario A & B dengan tugas nyata sekolah | User Acceptance Testing (UAT) per peran | Persentase penerimaan UAT >= 85% |
| **Gate E4: Efficiency Gate** | Pengukuran waktu tugas berpasangan dan penurunan entri berulang | Waktu tugas (menit), nilai signifikansi $p < 0.05$ | Penurunan durasi signifikan & DDI = 0 |

---

## 7. Matriks Risiko dan Mitigasi

| Risiko Teknis / Operasional | Tindakan Mitigasi |
|---|---|
| Keterlambatan perizinan akses data sekolah | Siapkan dan gunakan data sintetis terstruktur untuk pembangunan dan pengujian awal |
| Ruang lingkup membengkak | Batasi dan bekukan lingkup prototype pada dua skenario utama (Skenario A dan Skenario B) |
| Kendala dependensi C di Windows (`libmagic`, `WeasyPrint`) | Gunakan `python-magic-bin` atau inspeksi bytes murni; siapkan `ReportLab` sebagai alternatif PDF |
| Perbedaan konkurensi SQLite vs PostgreSQL | Terapkan transaksi atomik eksplisit dan verifikasi migrasi pada kedua basis data |
| Riwayat bulk attendance tidak tercatat otomatis | Wajib gunakan utilitas `bulk_create_with_history` di blok transaksi yang sama |
| Angka dashboard usang karena cache | Gunakan `transaction.on_commit` untuk pembersihan cache Redis pasca mutasi |
| Risiko kebocoran berkas permohonan | Simpan berkas di luar folder publik; wajibkan verifikasi peran dan objek pada endpoint unduh |
| Ketidaksesuaian visual antara desain dan kode | Terapkan gerbang review desain (Design Sign-off Gate) sebelum pengujian integrasi modul |

---

## 8. Definition of Done (DoD) Integrasi Penuh

- Seluruh artefak arsitektur TOGAF (bisnis, data, aplikasi, teknologi) terdokumentasi dan konsisten.
- Seluruh spesifikasi desain pada Pencil MCP telah diverifikasi dan memiliki paket handoff visual lengkap.
- Seluruh endpoint API kritis memiliki pengujian otomatis (pytest) yang lulus 100%.
- Kedua skenario demonstrasi utama (Kehadiran dan Layanan TU) dapat dijalankan lancar melalui antarmuka peramban.
- Seluruh aturan otorisasi peran dan proteksi data per objek terverifikasi tanpa celah IDOR.
- Tidak ada rahasia, kredensial, atau data pribadi siswa yang masuk ke repositori kode.
- Panduan deployment, backup, restore basis data, dan seed data sintetis tersedia lengkap.
