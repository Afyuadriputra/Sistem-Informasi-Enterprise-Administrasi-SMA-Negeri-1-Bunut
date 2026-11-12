# Integration Status & Release Gate Tracking

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Penanggung Jawab | **Coordinator / Integration Agent** |
| Cakupan Writable | `contracts/**`, `coordination/INTEGRATION_STATUS.md`, `coordination/PROJECT_STATUS.md` |
| Terakhir Diperbarui | 12 November 2026 |
| Status Baseline Kontrak | **BASELINE M0.2 APPROVED (OpenAPI v1.1.0, DBML v1.0.0, RBAC v1.1.0)** |
| Prasyarat Fondasi | BE-M1, FE-M1, UX-M1 s/d UX-M9.3 (Frozen) |

---

## 1. Status Gerbang Integrasi Tiga Jalur (Integration Gates)

| Gerbang Integrasi | Prasyarat Masuk | Fokus Pengujian Nyata | Status Saat Ini | Tanggal Lolos | Bukti Verifikasi |
|---|---|---|---|---|---|
| `INT-M1: Foundation Gate` | BE-M1, FE-M1, UX-M1 | Skema Error Envelope, Token visual dasar, CORS preflight, Healthcheck | STANDBY | - | - |
| `INT-M2: Auth Gate` | BE-M2, FE-M2, UX-M2 | Login riil, header Bearer JWT, refresh token, Logout blacklist, UI Shell | NOT_STARTED | - | - |
| `INT-M3: Master Gate` | BE-M3, FE-M3, UX-M3 | Paginasi server-side, 6 operasi PATCH master data, filter query, penempatan rombel | NOT_STARTED | - | - |
| `INT-M4: Attendance Gate` | BE-M4, FE-M4, UX-M4 | Skenario A (Tahap 1): Simpan absensi massal atomik, respon 409, rekap, dialog koreksi | NOT_STARTED | - | - |
| `INT-M5: Affairs Gate` | BE-M5, FE-M5, UX-M5 | Skenario A (Tahap 2): Kasus kesiswaan, CATAT_TINDAKAN, response filtering BK, timeline | NOT_STARTED | - | - |
| `INT-M6: Admin Gate` | BE-M6, FE-M6, UX-M6 | Skenario B: Permohonan surat, upload & streaming unduh berkas privat, PATCH jenis layanan | NOT_STARTED | - | - |
| `INT-M7: Reports Gate` | BE-M7, FE-M7, UX-M7 | Sinkronisasi metrik dashboard 6 peran, ekspor Excel & PDF, invalidasi cache Redis | NOT_STARTED | - | - |
| `INT-M8: Full System E2E` | BE-M8, FE-M8, UX-M8 | Skenario A & B penuh, audit IDOR, uji beban, verifikasi a11y, evaluasi DSRM | NOT_STARTED | - | - |

---

## 2. Kriteria Lolos Gerbang Integrasi (Integration Gate Exit Criteria)

Sebuah gerbang integrasi hanya boleh ditandai `INTEGRATION_PASSED` jika:
1. Panggilan HTTP nyata antara frontend peramban dan backend Django Ninja berhasil tanpa menggunakan mock.
2. Tampilan visual antarmuka telah diverifikasi mematuhi hasil sign-off desain dari Pencil MCP.
3. Seluruh assert pengujian integrasi lulus tanpa kegagalan (zero defect).
4. Respon kode status HTTP, struktur payload JSON, dan pesan error mematuhi kontrak `openapi.v1.yaml` (v1.1.0).
5. Hak akses dan batasan peran terverifikasi tidak memiliki celah keamanan IDOR.
