# Master AI Agent Guidelines & Architecture Rules

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | ACTIVE & ENFORCED |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Coordinator / Integration Agent |
| Acuan | task/task1.md, PRD, TRD, DBD, BSD, AFD, IPD, UID |

---

## 1. Ikhtisar Proyek & Filosofi

Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut adalah aplikasi web enterprise berbasis arsitektur **Modular Monolith Django Ninja** di backend dan **SPA React TypeScript Atomic Design** di frontend, serta didukung oleh **Pencil MCP UI/UX Design Track** (`pen.dev`). Proyek ini dikembangkan menggunakan pendekatan **Contract-First Parallel Development**, di mana kontrak API (`contracts/openapi.v1.yaml`) dan skema basis data (`contracts/database.dbml`) menjadi batas pemisah dan acuan bersama antara pengerjaan desain, backend, dan frontend.

---

## 2. Hierarki Sumber Kebenaran (Source of Truth)

Jika terjadi perbedaan tafsir antar dokumen atau spesifikasi, selesaikan melalui hierarki keputusan berikut:
1. **PRD.md:** Kebutuhan fungsional, ruang lingkup, dan batasan wewenang bisnis.
2. **AFD.md:** Alur kerja pengguna, proses bisnis, dan transisi status.
3. **DBD.md & database.dbml:** Desain data, integritas tabel, relasi, dan audit trail.
4. **BSD.md & openapi.v1.yaml:** Spesifikasi teknis backend, endpoint API, dan kontrak data.
5. **TRD.md:** Standar teknologi, dependensi, arsitektur modul, dan infrastruktur.
6. **UID.md & design/** (Pencil MCP): Desain visual, pengalaman pengguna, 25 hukum UX, dan aksesibilitas.
7. **IPD.md:** Roadmap tahapan penelitian DSRM dan dependensi pengerjaan paralel multi-jalur.

Dilarang menyelesaikan perbedaan secara sepihak. Catat temuan pada `coordination/PROJECT_STATUS.md` untuk direview Coordinator.

---

## 3. Peran AI Agent & Batas Kepemilikan File (File Ownership)

Produksi dibagi ke dalam empat peran agent dengan batas kepemilikan berkas (*file ownership boundaries*) yang ketat:

| Peran Agent | Tanggung Jawab Utama | Primary Writable Scope | Read-Only Scope |
|---|---|---|---|
| **UI/UX Design Agent** | Wireframe, screen layout, token sistem, WCAG audit di Pencil MCP (`pen.dev`) | `design/**`, `coordination/DESIGN_STATUS.md` | `docs/**`, `contracts/**` |
| **Backend Agent** | Django Ninja, Models, Migrations, Services, Selectors, Redis, Pytest | `backend/**`, `coordination/BACKEND_STATUS.md` | `frontend/**`, `design/**`, `contracts/**`, `docs/**` |
| **Frontend Agent** | React Vite, TypeScript, Tailwind, shadcn/ui, TanStack Query, Vitest | `frontend/**`, `coordination/FRONTEND_STATUS.md` | `backend/**`, `design/**`, `contracts/**`, `docs/**` |
| **Coordinator / Integration Agent** | Penyelarasan kontrak, status integrasi, E2E test, mitigasi konflik | `contracts/**`, `coordination/PROJECT_STATUS.md`, `coordination/INTEGRATION_STATUS.md`, `coordination/CONTRACT_CHANGE_REQUESTS.md`, root `AGENTS.md` | Seluruh repositori |

### Aturan Ketat Isolasi Berkas:
1. Backend Agent **DILARANG KERAS** mengubah berkas di `frontend/**` atau `design/**`.
2. Frontend Agent **DILARANG KERAS** mengubah berkas di `backend/**` atau `design/**`.
3. Design Agent **DILARANG KERAS** mengubah berkas kode aplikasi di `backend/**` atau `frontend/**`.
4. Berkas desain `.pen` adalah terenkripsi dan **wajib** dikelola secara eksklusif menggunakan tool Pencil MCP (`get_app_state`, `save`, `execute`, dll.), tidak boleh diedit sebagai berkas teks biasa.
5. Jika ditemukan masalah integrasi pada sisi lain, **DILARANG** memperbaiki langsung. Buat catatan isu pada `coordination/PROJECT_STATUS.md` dan delegasikan ke pemilik cakupan.

---

## 4. Independensi Jalur Produksi & Kesiapan Kontrak (Decoupled Readiness)

1. **Independensi Backend:** Backend Agent dapat memulai pekerjaan logika bisnis, ORM, dan router API segera setelah kontrak endpoint dan DBML modul terkait berstatus `APPROVED` atau `FROZEN`. Backend **tidak bergantung** pada selesainya desain UI maupun implementasi frontend.
2. **Independensi Frontend:** Frontend Agent dapat memulai fondasi aplikasi, routing, client state, dan form validasi Zod berdasarkan kontrak OpenAPI tanpa menunggu backend selesai. Mocking hanya dilakukan pada lingkungan dev/test terisolasi dan dilarang masuk ke build produksi. Finalisasi visual antarmuka mengikuti design sign-off dari Pencil Track.
3. **Independensi Desain:** Design Agent dapat menyelesaikan rancangan antarmuka dan interaksi pada Pencil MCP murni berdasarkan PRD, AFD, dan UID, tanpa memerlukan frontend atau backend yang berjalan.

---

## 5. Tata Kelola Perubahan Kontrak (Contract Protocol)

- File `contracts/openapi.v1.yaml` dan `contracts/database.dbml` adalah baseline yang mengikat.
- Jika implementasi memerlukan penyesuaian endpoint, parameter, atau field:
  1. Buat usulan pada `coordination/CONTRACT_CHANGE_REQUESTS.md`.
  2. Integration Agent melakukan analisis dampak dan memberikan persetujuan.
  3. File kontrak diperbarui oleh Integration Agent dengan nomor revisi eksplisit.
  4. Backend, Frontend, dan Design Agent memperbarui artefak masing-masing.

---

## 6. Standar Kualitas & Keamanan (Non-Negotiable)

1. **Deny-by-Default & Object-Level Authorization:**
   - Seluruh endpoint memvalidasi hak akses objek riil. Guru hanya dapat mengakses kelas penugasannya; kesiswaan hanya mengakses kasus dalam kewenangannya.
2. **Pencegahan Kebocoran Data Sensitif:**
   - Dilarang menyimpan kata sandi, token, atau NIK siswa ke dalam berkas log sistem.
   - Dokumen permohonan persuratan wajib disimpan di direktori privat (`PRIVATE_MEDIA_ROOT`) dan diunduh melalui endpoint terproteksi.
3. **Kontrol Konkurensi Optimistik:**
   - Mutasi status kasus dan permohonan wajib menyertakan `expected_version` (Optimistic Locking) untuk mendeteksi konflik dan mengembalikan HTTP 409 Conflict.
4. **Transaksi Atomik Absensi:**
   - Simpan absensi kelas massal wajib atomik (*all-or-nothing*) dan mencatat riwayat audit menggunakan `bulk_create_with_history`.
5. **Kebijakan Keamanan Kegagalan Redis (Failure Policy):**
   - *Fail-Closed:* Pemeriksaan blacklist pembatalan sesi token dan rate limiting pencegahan brute-force wajib menolak akses atau beralih ke verifikasi basis data jika Redis terputus.
   - *Fail-Open:* Cache respon kueri non-kritis dapat dilewati (*bypass*) langsung ke basis data.
6. **Standar Desain Anti-AI Slop:**
   - Antarmuka web wajib mengikuti tema *Institutional Navy & Teal* di UID.md. Dilarang menambahkan animasi dekoratif berlebih, tombol mati, teks template generik, atau card bertumpuk tanpa fungsi nyata.

---

## 7. Routing AI Agent Skills

Gunakan skill yang relevan sesuai jenis tugas yang sedang dikerjakan:

| Domain Tugas | Rekomendasi Skills yang Relevan |
|---|---|
| **UI/UX Design Track (Pencil)** | `antislop`, `antislop-ui`, `antislop-copywriting`, `antislop-layoutmobile`, `ui-taste` |
| **Frontend UI/UX Implementation** | `antislop`, `antislop-ui`, `antislop-copywriting`, `antislop-layoutmobile`, `ui-taste`, `tdd` |
| **Backend Logic & Security** | `security-audit`, `tdd`, `antislop-code`, `python-performance-optimization` |
| **Backend & Architecture Review**| `ponytail-review`, `ponytail-audit`, `ponytail` |
| **Cross-System Review & Integration**| `security-audit`, `ponytail-review`, `ponytail-audit` |

*Catatan:* Jangan menggunakan skill native mobile (`ios-design`, `design-mobile-apps`) karena proyek ini adalah aplikasi web desktop & responsif.

---

## 8. Protokol Handoff & Resume Sesi

Sebelum mengakhiri sesi pengerjaan:
1. Agent wajib mencatat progress, langkah terakhir yang diselesaikan, dan langkah berikutnya pada berkas status masing-masing di `coordination/` (`BACKEND_STATUS.md`, `FRONTEND_STATUS.md`, `DESIGN_STATUS.md`, `PROJECT_STATUS.md`).
2. Agent berikutnya wajib membaca berkas status terkait sebelum melanjutkan pengerjaan untuk menghindari pengerjaan ulang (*duplicate work*).
