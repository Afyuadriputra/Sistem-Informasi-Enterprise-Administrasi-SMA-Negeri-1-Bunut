# Contract Change Requests (CCR) Log

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Log | ACTIVE & MANAGED |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Coordinator / Integration Agent |

---

## 1. Prosedur Pengajuan Perubahan Kontrak

Setiap perubahan terhadap `contracts/openapi.v1.yaml` atau `contracts/database.dbml` wajib dicatat pada log ini sebelum dilakukan perubahan kode pada frontend maupun backend:

1. **CCR ID:** Format unik `CCR-YYYYMMDD-XX`
2. **Pengusul:** Backend Agent / Frontend Agent / UI/UX Design Agent / Coordinator
3. **Komponen Kontrak:** Nama endpoint, schema, atau tabel yang terdampak
4. **Alasan Kebutuhan:** Mengapa perubahan mutlak diperlukan
5. **Dampak Teknis:** Dampak pada backend models/services, frontend components/queries, dan desain Pencil
6. **Status:** `PROPOSED` -> `UNDER_REVIEW` -> `APPROVED` / `REJECTED` -> `IMPLEMENTED`

---

## 2. Riwayat Usulan Perubahan Kontrak

| CCR ID | Tanggal | Pengusul | Komponen | Ringkasan Perubahan | Status | Tanggal Persetujuan |
|---|---|---|---|---|---|---|
| `CCR-20261112-01` | 12 Nov 2026 | Coordinator | OpenAPI & DBML | Inisialisasi kontrak baseline v1.0.0 untuk seluruh modul | **APPROVED** | 12 Nov 2026 |
| `CCR-20261112-02` | 12 Nov 2026 | Coordinator | OpenAPI v1.0.0 | Penambahan endpoint kelengkapan S01-S18 (`/accounts/users`, `/master/employees`, dll.) dan 13 skema baru | **APPROVED** | 12 Nov 2026 |
| `CCR-20261112-03` | 12 Nov 2026 | Coordinator | contracts/README | Penerapan siklus kesiapan modular (Modular Readiness Gates) per modul dan per agen | **APPROVED** | 12 Nov 2026 |

---

### Detail CCR-20261112-01 (Baseline Contract Initialization)
- **Komponen:** Seluruh skema di `contracts/openapi.v1.yaml` dan `contracts/database.dbml`.
- **Alasan Kebutuhan:** Menetapkan kontrak antarmuka API dan skema database awal yang sinkron lintas dokumen untuk memulai pengerjaan paralel tahap M1.
- **Dampak Teknis:** Menjadi sumber kebenaran tunggal (*single source of truth*) bagi Backend Agent dan Frontend Agent.
- **Status:** APPROVED.

---

### Detail CCR-20261112-02 (OpenAPI S01-S18 Operational Completeness)
- **Komponen:** `contracts/openapi.v1.yaml` (Paths & Components Schemas).
- **Alasan Kebutuhan:** Audit M0.1 menemukan bahwa beberapa endpoint operasional untuk screen S04 (Manajemen Pengguna), S06 (Master Pegawai), S07 (Penempatan/Penugasan), dan S12 (Jenis Layanan) belum tercantum di paths OpenAPI meskipun sudah ada di RBAC Matrix dan UID.
- **Perubahan Rinci:**
  - Menambahkan path `/accounts/users` (GET list, POST create) dan `/accounts/users/{id}` (GET detail, PATCH update).
  - Menambahkan path `/accounts/roles` (GET list roles).
  - Menambahkan path `/master/employees` (GET list, POST create).
  - Menambahkan method PATCH pada `/master/students/{id}`.
  - Menambahkan method GET pada `/master/enrollments` dan `/master/assignments`.
  - Menambahkan method POST pada `/administration/service-types`.
  - Menambahkan 13 skema komponen Pydantic/OpenAPI: `UserItem`, `UserListResponse`, `UserCreateRequest`, `UserUpdateRequest`, `RoleItem`, `RoleListResponse`, `EmployeeItem`, `EmployeeListResponse`, `EmployeeCreateRequest`, `StudentUpdateRequest`, `EnrollmentListResponse`, `ClassAssignmentListResponse`, `ServiceTypeCreateRequest`.
- **Dampak Teknis:** Total operasi meningkat dari 32 menjadi 43 operasi; total skema meningkat dari 52 menjadi 65 skema; 0 broken references; coverage screen S01-S18 terpenuhi 100%.
- **Status:** APPROVED & IMPLEMENTED.

---

### Detail CCR-20261112-03 (Modular Contract Readiness Gates)
- **Komponen:** `contracts/README.md`, `docs/IPD.md`.
- **Alasan Kebutuhan:** Mengoreksi asumsi keliru bahwa seluruh kontrak sistem wajib berstatus FROZEN sebelum fondasi dimulai. Memisahkan kesiapan kontrak per modul agar fondasi M1 dapat dimulai mandiri.
- **Perubahan Rinci:** Modul Base Error Envelope dan Accounts/Auth berstatus `FROZEN`; Modul Master Data, Attendance, Student Affairs, Administration, dan Reports berstatus `APPROVED` dengan penegakan runtime Deny-by-Default untuk item `PENDING_APPROVAL`.
- **Status:** APPROVED & IMPLEMENTED.
