# Master Project Status & Multi-Agent Tracking

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Tahap Proyek Saat Ini | **INT-M0 - SYSTEM INTEGRATION PREFLIGHT & BASELINE VERIFICATION** |
| Status Keseluruhan | **CONDITIONALLY_READY — INTEGRATION_PREFLIGHT_WITH_OPEN_BLOCKERS** |
| Terakhir Diperbarui | 14 November 2026 |
| Pengelola | Coordinator / Integration Agent |
| Status Kontrak Bersama | **APPROVED BASELINE v1.1.0** (OpenAPI: 49 ops, 71 schemas; DBML: 18 tables) |
| SHA-256 OpenAPI | `D3871BA834C17FC6DC49BB92F63391EB3EC63571E784A6623CE8E2A65CB52B9E` |
| Status UI/UX Design | **COMPLETED & FROZEN** (UX-M1 s/d UX-M9.3, 32 visual frames, master canvas 864 KB) |

---

## 1. Ringkasan Status Jalur Kerja (Track Overview)

| Jalur Kerja | Status Saat Ini | Milestone Aktif | Agent Penanggung Jawab | Catatan Kesiapan & Hasil Verifikasi |
|---|---|---|---|---|
| **Kontrak & Koordinasi** | **APPROVED / FINALIZED** | `v1.1.0` | Coordinator Agent | OpenAPI v1.1.0 (49 ops), DBML v1.0.0 (18 tables), RBAC v1.1.0 selaras 100% |
| **UI/UX Design Track** | **COMPLETED** | `UX-M9.3: Handoff Freeze` | UI/UX Design Agent | Kanvas master terpadu 864 KB, 32 evidensi visual PNG, dua master docs |
| **Jalur Backend** | **READY / COMPLETED** | `BE-M9.1: Closure` | Backend Agent | 93 automated tests PASS, 84% code coverage, 49 operasi API, Ruff check clean |
| **Jalur Frontend** | **READY / COMPLETED** | `FE-M10.1: Closure` | Frontend Agent | 71 Vitest tests PASS, 6 Playwright E2E tests PASS, typecheck & build clean |
| **Jalur Integrasi** | **READY FOR INT-M1** | `INT-M0: Preflight` | Integration Agent | INT-M0 selesai; preflight live HTTP lolos; siap eksekusi INT-M1 s/d INT-M8 |

---

## 2. Matriks Pelacakan Milestone Terpadu Tiga Jalur

| Milestone Desain (Pencil) | Milestone Frontend (React) | Milestone Backend (Django) | Gerbang Integrasi | Status Integrasi | Prasyarat Masuk |
|---|---|---|---|:---:|---|
| `UX-M1` (COMPLETED) | `FE-M1` (COMPLETED) | `BE-M1` (COMPLETED) | `INT-M1: Foundation Gate` | **READY** | INT-M0 Lolos Verifikasi Pra-Terbang |
| `UX-M2` (COMPLETED) | `FE-M2` (COMPLETED) | `BE-M2` (COMPLETED) | `INT-M2: Auth Gate` | QUEUED | INT-M1 Selesai |
| `UX-M3` (COMPLETED) | `FE-M3` (COMPLETED) | `BE-M3` (COMPLETED) | `INT-M3: Master Gate` | QUEUED | INT-M2 Selesai |
| `UX-M4` (COMPLETED) | `FE-M4` (COMPLETED) | `BE-M4` (COMPLETED) | `INT-M4: Attendance Gate` | QUEUED | INT-M3 Selesai |
| `UX-M5` (COMPLETED) | `FE-M5` (COMPLETED) | `BE-M5` (COMPLETED) | `INT-M5: Affairs Gate` | QUEUED | INT-M4 Selesai |
| `UX-M6` (COMPLETED) | `FE-M6` (COMPLETED) | `BE-M6` (COMPLETED) | `INT-M6: Admin Gate` | QUEUED | INT-M3 Selesai |
| `UX-M7` (COMPLETED) | `FE-M7` (COMPLETED) | `BE-M7` (COMPLETED) | `INT-M7: Reports Gate` | QUEUED | INT-M4/5/6 Selesai |
| `UX-M8` (COMPLETED) | `FE-M8` (COMPLETED) | `BE-M8` (COMPLETED) | `INT-M8: Full System E2E` | QUEUED | INT-M7 Selesai |

---

## 3. Resolusi Contract Gaps pada M0.2 (CCR-20261112-04)

1. **Master Data PATCH Endpoints:** Menambahkan 6 endpoint mutasi sebagian (`/master/academic-years/{id}`, `/master/classes/{id}`, `/master/employees/{id}`, `/administration/service-types/{id}`, `/master/enrollments/{id}`, `/master/assignments/{id}`) untuk menutup kesenjangan wewenang UPDATE pada RBAC dan menjamin siklus penempatan/penugasan tanpa hard delete.
2. **Attendance Concurrency:** Menambahkan respon resmi HTTP 409 Conflict pada `POST /attendance/bulk` untuk penanganan benturan konkurensi input presensi massal serentak.
3. **Penyaringan Sisi Server (Server-Side Query Parameters):** Menambahkan 10 parameter kueri filter opsional pada seluruh endpoint daftar data (list) untuk mendukung kebutuhan operasional sekolah tanpa melanggar backward-compatibility.
4. **Response Filtering Catatan Konseling BK:** Menegaskan aturan penyaringan sisi server untuk catatan sensitif konseling pada `GET /student-affairs/cases/{id}` agar tidak bocor ke peran non-kesiswaan (DEC-TECH-18).
5. **Wewenang Penugasan Guru:** Menegaskan hak peran Guru membaca daftar penugasan kelas sendiri via `GET /auth/me` dan `GET /master/assignments?employee_id={id}`.

---

## 4. Daftar Usulan Bisnis Terbuka (Open Business Proposals)

Seluruh usulan kebijakan sekolah yang belum divalidasi lapangan ditegakkan dengan aturan **Deny-by-Default** pada tingkat runtime:
- `DEC-BIZ-01`: Alur persetujuan surat pimpinan vs kepala TU (didukung oleh flag `requires_approval: true/false`).
- `DEC-BIZ-02`: Format resmi tata naskah dinas penomoran surat sekolah (format fleksibel disiapkan di database).
- `DEC-BIZ-03`: Ambang batas pasti akumulasi alpa untuk notifikasi kesiswaan (diisolasi di konfigurasi service layer).
- `DEC-BIZ-04`: Batas waktu koreksi absensi guru mandiri dan wali kelas (ditegakkan Deny-by-Default untuk > 24 jam).
- `DEC-BIZ-05`: Penanganan siswa pindahan/mutasi di tengah semester (diakomodasi rentang tanggal tabel `Enrollment` via kolom `end_date`).
