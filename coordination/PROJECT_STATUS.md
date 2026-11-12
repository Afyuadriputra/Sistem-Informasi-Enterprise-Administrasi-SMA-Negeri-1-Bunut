# Master Project Status & Multi-Agent Tracking

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Tahap Proyek Saat Ini | **M0.1 - DOCUMENTATION ALIGNMENT CORRECTION & PENCIL DESIGN TRACK** |
| Status Keseluruhan | **READY: THREE_TRACK_PARALLEL_FOUNDATION_READY** |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Coordinator / Integration Agent |

---

## 1. Ringkasan Status Jalur Kerja (Track Overview)

| Jalur Kerja | Status Saat Ini | Milestone Aktif | Agent Penanggung Jawab | Catatan Kesiapan |
|---|---|---|---|---|
| **Kontrak & Integrasi** | **APPROVED / MODULAR** | `M0.1` | Coordinator Agent | OpenAPI v1.0.0 (43 ops), DBML v1.0.0 (13 tables) tervalidasi |
| **UI/UX Design Track** | **READY** | `UX-M1: System Tokens` | UI/UX Design Agent | Pencil MCP (`pen.dev`) terhubung dan siap kanvas |
| **Jalur Backend** | **READY** | `BE-M1: Foundation` | Backend Agent | Menunggu inisiasi Django modular monolith |
| **Jalur Frontend** | **READY** | `FE-M1: Foundation` | Frontend Agent | Menunggu inisiasi React Vite TypeScript |
| **Jalur Integrasi** | **STANDBY** | `INT-M1: Gate` | Integration Agent | Aktif setelah UX-M1, BE-M1, & FE-M1 selesai |

---

## 2. Matriks Pelacakan Milestone Terpadu Tiga Jalur

| Milestone Desain (Pencil) | Milestone Frontend (React) | Milestone Backend (Django) | Gerbang Integrasi | Status Integrasi | Prasyarat Masuk |
|---|---|---|---|---|---|
| `UX-M1` (READY) | `FE-M1` (READY) | `BE-M1` (READY) | `INT-M1: Foundation Gate` | NOT_STARTED | M0.1 Selesai |
| `UX-M2` (QUEUED) | `FE-M2` (QUEUED) | `BE-M2` (QUEUED) | `INT-M2: Auth Gate` | NOT_STARTED | M1 Selesai |
| `UX-M3` (QUEUED) | `FE-M3` (QUEUED) | `BE-M3` (QUEUED) | `INT-M3: Master Gate` | NOT_STARTED | M2 Selesai |
| `UX-M4` (QUEUED) | `FE-M4` (QUEUED) | `BE-M4` (QUEUED) | `INT-M4: Attendance Gate` | NOT_STARTED | M3 Selesai |
| `UX-M5` (QUEUED) | `FE-M5` (QUEUED) | `BE-M5` (QUEUED) | `INT-M5: Affairs Gate` | NOT_STARTED | M3 Selesai |
| `UX-M6` (QUEUED) | `FE-M6` (QUEUED) | `BE-M6` (QUEUED) | `INT-M6: Admin Gate` | NOT_STARTED | M3 Selesai |
| `UX-M7` (QUEUED) | `FE-M7` (QUEUED) | `BE-M7` (QUEUED) | `INT-M7: Reports Gate` | NOT_STARTED | M4/5/6 Selesai |
| `UX-M8` (QUEUED) | `FE-M8` (QUEUED) | `BE-M8` (QUEUED) | `INT-M8: Full System E2E` | NOT_STARTED | M7 Selesai |

---

## 3. Protokol Resume Sesi (Session Resume Protocol)

Ketika sesi pengerjaan AI agent baru dimulai:
1. Periksa berkas `coordination/PROJECT_STATUS.md` untuk mengetahui milestone global yang sedang aktif.
2. Jika bertindak sebagai **UI/UX Design Agent**, baca `coordination/DESIGN_STATUS.md` dan gunakan tool Pencil MCP untuk beroperasi pada `design/**`.
3. Jika bertindak sebagai **Backend Agent**, baca `coordination/BACKEND_STATUS.md` untuk melihat task ID yang berstatus `IN_PROGRESS` atau `READY`.
4. Jika bertindak sebagai **Frontend Agent**, baca `coordination/FRONTEND_STATUS.md` untuk melihat task ID yang berstatus `IN_PROGRESS` atau `READY`.
5. Jika bertindak sebagai **Integration Agent**, baca `coordination/INTEGRATION_STATUS.md` untuk memeriksa gerbang integrasi yang siap diuji.
6. Lanjutkan pengerjaan persis dari langkah `Next Action` yang tercatat tanpa mengulang task yang telah berstatus `DONE`.

---

## 4. Daftar Blocker & Usulan Bisnis Terbuka (Open Proposals)

Tidak ada blocker teknis untuk memulai tahap pembangunan fondasi (`BE-M1`, `FE-M1`, dan `UX-M1`).

Usulan bisnis yang menunggu validasi lapangan di SMA Negeri 1 Bunut diatur dengan kebijakan **Deny-by-Default**:
- `DEC-BIZ-01`: Alur persetujuan surat pimpinan vs kepala TU (didukung oleh flag `requires_approval` di database).
- `DEC-BIZ-02`: Format resmi tata naskah dinas penomoran surat sekolah (format fleksibel disiapkan di database).
- `DEC-BIZ-03`: Ambang batas pasti akumulasi alpa untuk notifikasi kesiswaan (diisolasi di konfigurasi service layer).
- `DEC-BIZ-04`: Batas waktu koreksi absensi guru mandiri dan wali kelas (ditegakkan Deny-by-Default untuk > 24 jam).
- `DEC-BIZ-05`: Penanganan siswa pindahan/mutasi di tengah semester (diakomodasi rentang tanggal tabel `Enrollment`).
