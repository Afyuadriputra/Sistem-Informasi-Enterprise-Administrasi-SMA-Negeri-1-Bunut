# Master Project Status & Multi-Agent Tracking

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Tahap Proyek Saat Ini | **M0.2 - SHARED CONTRACT FINALIZATION & DEVELOPMENT RELEASE** |
| Status Keseluruhan | **READY: THREE_TRACK_PARALLEL_FOUNDATION_READY** |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Coordinator / Integration Agent |
| Status Kontrak Bersama | **APPROVED BASELINE v1.1.0** (OpenAPI: 49 ops, 71 schemas; DBML: 18 tables) |
| Status UI/UX Design | **COMPLETED & FROZEN** (UX-M1 s/d UX-M9.3, 32 visual frames, master canvas 864 KB) |

---

## 1. Ringkasan Status Jalur Kerja (Track Overview)

| Jalur Kerja | Status Saat Ini | Milestone Aktif | Agent Penanggung Jawab | Catatan Kesiapan & Hasil Verifikasi |
|---|---|---|---|---|
| **Kontrak & Integrasi** | **APPROVED / FINALIZED** | `M0.2` | Coordinator Agent | OpenAPI v1.1.0 (49 ops), DBML v1.0.0 (18 tables), RBAC v1.1.0 selaras 100% |
| **UI/UX Design Track** | **COMPLETED** | `UX-M9.3: Handoff Freeze` | UI/UX Design Agent | Kanvas master terpadu 864 KB, 32 evidensi visual PNG, dua master docs |
| **Jalur Backend** | **READY** | `BE-M1: Foundation` | Backend Agent | Siap inisiasi arsitektur Django Ninja, PostgreSQL, Redis, dan test suite |
| **Jalur Frontend** | **READY** | `FE-M1: Foundation` | Frontend Agent | Siap inisiasi React Vite TypeScript, Tailwind CSS, Atomic Design, TanStack Query |
| **Jalur Integrasi** | **STANDBY** | `INT-M1: Gate` | Integration Agent | Menunggu penyelesaian fondasi BE-M1 dan FE-M1 untuk uji kontrak awal |

---

## 2. Matriks Pelacakan Milestone Terpadu Tiga Jalur

| Milestone Desain (Pencil) | Milestone Frontend (React) | Milestone Backend (Django) | Gerbang Integrasi | Status Integrasi | Prasyarat Masuk |
|---|---|---|---|---|---|
| `UX-M1` (COMPLETED) | `FE-M1` (**READY**) | `BE-M1` (**READY**) | `INT-M1: Foundation Gate` | STANDBY | M0.2 Selesai & Kontrak Disetujui |
| `UX-M2` (COMPLETED) | `FE-M2` (QUEUED) | `BE-M2` (QUEUED) | `INT-M2: Auth Gate` | NOT_STARTED | M1 Selesai |
| `UX-M3` (COMPLETED) | `FE-M3` (QUEUED) | `BE-M3` (QUEUED) | `INT-M3: Master Gate` | NOT_STARTED | M2 Selesai |
| `UX-M4` (COMPLETED) | `FE-M4` (QUEUED) | `BE-M4` (QUEUED) | `INT-M4: Attendance Gate` | NOT_STARTED | M3 Selesai |
| `UX-M5` (COMPLETED) | `FE-M5` (QUEUED) | `BE-M5` (QUEUED) | `INT-M5: Affairs Gate` | NOT_STARTED | M3 Selesai |
| `UX-M6` (COMPLETED) | `FE-M6` (QUEUED) | `BE-M6` (QUEUED) | `INT-M6: Admin Gate` | NOT_STARTED | M3 Selesai |
| `UX-M7` (COMPLETED) | `FE-M7` (QUEUED) | `BE-M7` (QUEUED) | `INT-M7: Reports Gate` | NOT_STARTED | M4/5/6 Selesai |
| `UX-M8` (COMPLETED) | `FE-M8` (QUEUED) | `BE-M8` (QUEUED) | `INT-M8: Full System E2E` | NOT_STARTED | M7 Selesai |

---

## 3. Resolusi Contract Gaps pada M0.2 (CCR-20261112-04)

1. **Master Data PATCH Endpoints:** Menambahkan 6 endpoint mutasi sebagian (`/master/academic-years/{id}`, `/master/classes/{id}`, `/master/employees/{id}`, `/administration/service-types/{id}`, `/master/enrollments/{id}`, `/master/assignments/{id}`) untuk menutup kesenjangan wewenang UPDATE pada RBAC dan menjamin siklus penempatan/penugasan tanpa hard delete.
2. **Attendance Concurrency:** Menambahkan respon resmi HTTP 409 Conflict pada `POST /attendance/bulk` untuk penanganan benturan konkurensi input presensi massal serentak.
3. **Penyaringan Sisi Server (Server-Side Query Parameters):** Menambahkan 10 parameter kueri filter opsional pada seluruh endpoint daftar data (list) untuk mendukung kebutuhan operasional sekolah tanpa melanggar backward-compatibility.
4. **Response Filtering Catatan Konseling BK:** Menegaskan aturan penyaringan sisi server untuk catatan sensitif konseling pada `GET /student-affairs/cases/{id}` agar tidak bocor ke peran non-kesiswaan.
5. **Wewenang Penugasan Guru:** Menegaskan hak peran Guru membaca daftar penugasan kelas sendiri via `GET /auth/me` dan `GET /master/assignments?employee_id={id}`.

---

## 4. Daftar Usulan Bisnis Terbuka (Open Business Proposals)

Seluruh usulan kebijakan sekolah yang belum divalidasi lapangan ditegakkan dengan aturan **Deny-by-Default** pada tingkat runtime:
- `DEC-BIZ-01`: Alur persetujuan surat pimpinan vs kepala TU (didukung oleh flag `requires_approval: true/false`).
- `DEC-BIZ-02`: Format resmi tata naskah dinas penomoran surat sekolah (format fleksibel disiapkan di database).
- `DEC-BIZ-03`: Ambang batas pasti akumulasi alpa untuk notifikasi kesiswaan (diisolasi di konfigurasi service layer).
- `DEC-BIZ-04`: Batas waktu koreksi absensi guru mandiri dan wali kelas (ditegakkan Deny-by-Default untuk > 24 jam).
- `DEC-BIZ-05`: Penanganan siswa pindahan/mutasi di tengah semester (diakomodasi rentang tanggal tabel `Enrollment` via kolom `end_date`).
