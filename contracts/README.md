# API & Database Contracts Management

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Kontrak Baseline | OpenAPI 3.1.0 & DBML 2.0 |
| Versi Dokumen | v1.1.0 (Finalized Shared Contract Baseline) |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola Kontrak | Coordinator / Integration Agent |
| Checksum OpenAPI | `561415e6195e9921203af3370a621637d00ea1518ada8f735beea5e970594fe5` (71 KB) |
| Checksum DBML | `da7b35dbbfc0df1080dd40a93e4db01d97ceb568edf31ee3a97e1caf723603b8` (13.8 KB) |

---

## 1. Filosofi Modular Contract-First Development

Dalam pendekatan **Modular Contract-First Development**, kontrak antarmuka API (`openapi.v1.yaml`) dan skema basis data (`database.dbml`) disepakati dan dikelola statusnya secara modular.

Prinsip ini memungkinkan:
1. **Pemisahan Kesiapan per Modul (Decoupled Readiness):** Pekerjaan fondasi dan modul inti tidak terhambat oleh kebijakan bisnis modul lain yang masih dalam tahap validasi SOP sekolah.
2. **Independensi Backend:** Backend Agent dapat membangun router Django Ninja, skema Pydantic, service logic, dan test suite secara mandiri berdasarkan kontrak modul yang berstatus `APPROVED` atau `FROZEN`, tanpa membutuhkan generated TypeScript atau mock fixture frontend.
3. **Independensi Frontend:** Frontend Agent dapat membangun struktur halaman, routing, client state, dan form validasi Zod berbasis kontrak tanpa menunggu backend selesai. Mocking hanya aktif di lingkungan dev/test terisolasi dan dilarang masuk ke build produksi.
4. **Independensi Desain:** UI/UX Design Agent merancang komponen, token, dan alur interaksi di Pencil MCP (`pen.dev`) murni berdasarkan spesifikasi fungsional dan visual, tanpa bergantung pada kode aplikasi.

---

## 2. Siklus Hidup & Matriks Kesiapan Kontrak per Modul (Contract Readiness Matrix)

Setiap modul di dalam kontrak API memiliki status siklus hidup yang terpantau:

```text
[DRAFT] -> [IN_REVIEW] -> [APPROVED] -> [FROZEN] -> [IMPLEMENTED] -> [VERIFIED]
```

| Modul / Domain | Versi Revisi | Status Kontrak | Kesiapan Backend | Kesiapan Frontend | Kesiapan Desain | Catatan Bisnis & Blocker Terbuka |
|---|---|---|---|---|---|---|
| **Fondasi & Base Envelope** | `rev-1.1.0` | **FROZEN** | READY (`BE-M1`) | READY (`FE-M1`) | READY (`UX-M1`) | ErrorEnvelope, RequestId, Pagination, Cors selaras penuh |
| **Accounts & Auth** | `rev-1.1.0` | **FROZEN** | READY (`BE-M2`) | READY (`FE-M2`) | READY (`UX-M2`) | 5 operasi, BearerAuth, rotasi token, Redis blacklist, RBAC baseline |
| **Master Data** | `rev-1.1.0` | **APPROVED** | READY (`BE-M3`) | READY (`FE-M3`) | READY (`UX-M3`) | 19 operasi (termasuk 6 PATCH mutasi & siklus penugasan). TU tambah siswa PENDING |
| **Attendance** | `rev-1.1.0` | **APPROVED** | READY (`BE-M4`) | READY (`FE-M4`) | READY (`UX-M4`) | 3 operasi (termasuk respon 409 Conflict pada bulk). Koreksi >24 jam PENDING |
| **Student Affairs** | `rev-1.1.0` | **APPROVED** | READY (`BE-M5`) | READY (`FE-M5`) | READY (`UX-M5`) | 4 operasi (termasuk aksi CATAT_TINDAKAN & response filtering BK). Ambang alpa PENDING |
| **Administration** | `rev-1.1.0` | **APPROVED** | READY (`BE-M6`) | READY (`FE-M6`) | READY (`UX-M6`) | 10 operasi (termasuk PATCH jenis layanan, upload/download privat). SOP dinas PENDING |
| **Reports & Audit** | `rev-1.1.0` | **APPROVED** | READY (`BE-M7`) | READY (`FE-M7`) | READY (`UX-M7`) | 4 operasi (dashboard agregat, ekspor xlsx/pdf, audit-logs). Audit log pimpinan PENDING |

> [!IMPORTANT]
> Kontrak dengan status `APPROVED` telah siap digunakan untuk implementasi kode teknis, dengan penegakan runtime **Deny-by-Default** pada seluruh fungsi yang bertanda `PENDING_APPROVAL`. Kontrak baru dinaikkan ke status `FROZEN` penuh setelah SOP sekolah tervalidasi secara resmi.

---

## 3. Tata Kelola Perubahan Kontrak (Contract Change Management Protocol)

Dilarang keras mengubah endpoint, parameter kueri, nama field payload, enum, atau kode error secara sepihak di kode backend maupun frontend. Jika ditemukan kebutuhan teknis mendesak untuk mengubah kontrak, wajib melalui 7 tahapan berikut:

1. **Contract Change Request (CCR):** Pengusul membuat usulan pada berkas `coordination/CONTRACT_CHANGE_REQUESTS.md` dengan menyertakan alasan teknis dan rincian perubahan.
2. **Impact Analysis:** Integration Agent meninjau dampak perubahan terhadap skema database, logika backend, tipe TypeScript frontend, dan dokumen PRD/UID.
3. **Approval:** Persetujuan resmi diberikan sebelum file kontrak diubah.
4. **Contract Update:** Integration Agent memperbarui `contracts/openapi.v1.yaml` atau `contracts/database.dbml` dengan nomor revisi baru.
5. **Backend Task Update:** Backend Agent menjadwalkan penyesuaian router atau skema serializer.
6. **Frontend Task Update:** Frontend Agent menggenerasi ulang tipe TypeScript via `openapi-typescript` dan memperbarui form/view terkait.
7. **Design Update:** Design Agent memperbarui spesifikasi kanvas jika terjadi perubahan data antarmuka.

---

## 4. Berkas Kontrak

1. **[openapi.v1.yaml](file:///d:/Kuliah/joki/radit/PROJEK%20istri%20bg%20givo/contracts/openapi.v1.yaml):** Spesifikasi lengkap REST API OpenAPI 3.1.0 (37 paths, 49 operations, 71 schemas terstandar) mencakup seluruh skenario antarmuka S01 s/d S18, mutasi data master, dan kontrol konkurensi.
2. **[database.dbml](file:///d:/Kuliah/joki/radit/PROJEK%20istri%20bg%20givo/contracts/database.dbml):** Definisi visual dan struktural 18 tabel basis data, relasi foreign key, constraint unik komposit (`UNIQUE(student_id, class_id, date)`), audit snapshot (`HistoricalRecords`), dan kolom kontrol konkurensi optimistik (`version`).
