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
| `CCR-20261112-04` | 12 Nov 2026 | Coordinator | OpenAPI & DBML | Shared Contract Finalization, 6 PATCH endpoints, 49 ops, HTTP 409 | **APPROVED** | 12 Nov 2026 |
| `CCR-20261114-01` | 14 Nov 2026 | Coordinator | OpenAPI v1.1.0 | Roster Optimistic Concurrency Precondition (`expected_roster_version` / HTTP 409) | **APPROVED** | 14 Nov 2026 |

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
- **Status:** APPROVED & IMPLEMENTED.\n---

### Detail CCR-20261112-04 (Shared Contract Finalization & Master Data Lifecycle)
- **Komponen:** contracts/openapi.v1.yaml (v1.1.0), docs/RBAC_MATRIX.md, contracts/README.md, docs/DECISION_LOG.md.
- **Alasan Kebutuhan:**
  1. Penyelarasan wewenang UPDATE pada RBAC yang belum didukung operasi PATCH di OpenAPI (Tahun Ajaran, Kelas Rombel, Pegawai, Jenis Layanan).
  2. Siklus hidup penempatan siswa dan penugasan guru (pengakhiran status penugasan via end_date tanpa penghapusan fisik/hard delete).
  3. Penanganan konkurensi presensi massal via respon HTTP 409 Conflict pada POST /attendance/bulk.
  4. Penyediaan parameter kueri filter opsional di sisi server yang dibutuhkan operasional sekolah dan UI/UX Design Track.
  5. Penegasan aturan response filtering untuk catatan konseling rahasia BK pada backend.
- **Perubahan Rinci:**
  - Menambahkan 6 endpoint mutasi PATCH:
    - PATCH /master/academic-years/{id} (updateAcademicYear)
    - PATCH /master/classes/{id} (updateClass)
    - PATCH /master/employees/{id} (updateEmployee)
    - PATCH /administration/service-types/{id} (updateServiceType)
    - PATCH /master/enrollments/{id} (updateEnrollment)
    - PATCH /master/assignments/{id} (updateClassAssignment)
  - Menambahkan 6 skema Pydantic/OpenAPI: AcademicYearUpdateRequest, ClassUpdateRequest, EmployeeUpdateRequest, ServiceTypeUpdateRequest, EnrollmentUpdateRequest, ClassAssignmentUpdateRequest.
  - Menambahkan respon HTTP 409 Conflict pada POST /attendance/bulk.
  - Menambahkan 10 parameter kueri filter opsional: is_active pada academic-years, class_id pada students, 
ole pada assignments, student_id & search pada cases, service_type_id & search pada requests, service_type_id pada documents & pdf reports, search, 
ole, is_active pada users, serta user_id, start_date, end_date pada audit-logs.
  - Memperbarui versi OpenAPI menjadi 1.1.0 (37 paths, 49 operations, 71 schemas, 0 broken references).
- **Dampak Teknis:**
  - Backend: Django Ninja mengimplementasikan router PATCH dan filter parameter opsional.
  - Frontend: openapi-typescript menggenerasi antarmuka TypeScript v1.1.0 dengan 49 operasi.
  - Desain: Seluruh frame antarmuka Pencil MCP pada master-canvas.pen tetap valid dan kini didukung penuh oleh kontrak server.
- **Status:** APPROVED & IMPLEMENTED.

---

### Detail CCR-20261114-01 (Attendance Roster Optimistic Concurrency Resolution)
- **Komponen:** `contracts/openapi.v1.yaml` (`AttendanceRosterResponse`, `AttendanceBulkRequest`, `POST /attendance/bulk`).
- **Alasan Kebutuhan:** Menutup kesenjangan P0 konkurensi presensi massal di mana `POST /attendance/bulk` telah memiliki respon HTTP 409 Conflict namun request payload belum memuat field precondition revision untuk mendeteksi submit dari data roster yang sudah kedaluwarsa (*stale roster edits*).
- **Perubahan Rinci:**
  1. Pada `AttendanceRosterResponse`, disediakan field `roster_version` (integer bertahap yang mencerminkan timestamp atau jumlah mutasi pada rombel/tanggal terkait).
  2. Pada `AttendanceBulkRequest`, disediakan field opsional `expected_roster_version` (integer).
  3. Logika Backend: Server memvalidasi bahwa `expected_roster_version` cocok dengan status saat ini. Jika data telah diubah oleh guru lain atau wali kelas setelah roster dimuat, kembalikan respon HTTP 409 Conflict (`CONCURRENCY_CONFLICT`).
  4. Backward Compatibility: Field bersifat opsional sehingga input awal atau klien tanpa versi tetap didukung tanpa breaking change.
- **Status:** APPROVED & IMPLEMENTED.
\n