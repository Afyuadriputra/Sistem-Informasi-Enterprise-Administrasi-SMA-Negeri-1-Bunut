# Integration & Parallel Workflow Plan

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Dokumen | APPROVED INTEGRATION BASELINE |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Integration Agent / Technical Lead |
| Acuan | task/task1.md, contracts/openapi.v1.yaml, IPD §1-10, DESIGN_EXECUTION_PLAN, BACKEND_EXECUTION_PLAN, FRONTEND_EXECUTION_PLAN |

---

## 1. Model Pengerjaan Fleksibel (Six Operational Scenarios)

Sistem perencanaan proyek ini dirancang agar dapat memfasilitasi 6 skenario pengerjaan mandiri maupun paralel:

1. **Scenario A (Backend First):** Backend Agent dapat mengimplementasikan seluruh modul backend, database, dan API integration tests secara mandiri berdasarkan skema kontrak tanpa memerlukan antarmuka frontend maupun selesainya desain visual.
2. **Scenario B (Frontend First):** Frontend Agent dapat menyelesaikan fondasi antarmuka, routing, client state, dan form validasi Zod secara mandiri dengan contract-based mock fixture tanpa menunggu server backend aktif.
3. **Scenario C (Design First):** Design Agent dapat merancang wireframe, tata letak, dan token visual secara independen di Pencil MCP (`pen.dev`) tanpa memerlukan kode backend maupun frontend.
4. **Scenario D (Full Parallel Three-Track):** Design Agent, Backend Agent, dan Frontend Agent dapat mengerjakan milestone masing-masing secara simultan di branch/worktree terpisah tanpa risiko benturan file (*zero file collision*).
5. **Scenario E (Interrupted Development):** Sesi pengerjaan AI agent dapat dijeda dan dilanjutkan kapan saja berkat struktur pelacakan persisten pada folder `coordination/`.
6. **Scenario F (Incremental Integration):** Setiap modul (misal Presensi atau Layanan TU) dapat diintegrasikan dan diverifikasi secara bertahap begitu backend dan frontend modul tersebut siap, tanpa menunggu seluruh sistem selesai.

---

## 2. Grafik Dependensi Multi-Jalur (Multi-Track Dependency Graph)

Konvergensi tiga jalur produksi (Pencil Design, Frontend, Backend) diikat oleh kontrak dan dievaluasi pada setiap Gerbang Integrasi (*Integration Gate*):

```text
[Kontrak Modular: APPROVED/FROZEN]
       │
       ├─────────────────────────────────┬─────────────────────────────────┐
       ▼                                 ▼                                 ▼
[UX-M1: Design System]          [FE-M1: FE Foundation]            [BE-M1: BE Foundation]
       │                                 │                                 │
       │ (Tokens Blueprint)              │                                 │
       ▼                                 ▼                                 ▼
[UX-M2: Auth/Shell]             [FE-M2: Auth/Shell]               [BE-M2: Auth/RBAC]
       │                                 │                                 │
       │                                 └───────────────┬─────────────────┘
       │ (Visual Sign-off)                               ▼
       └───────────────────────────────────────> [INT-M2: Auth Gate]
                                                         │
       ┌─────────────────────────────────────────────────┴─────────────────────────────────┐
       ▼                                                 ▼                                 ▼
[UX-M3: Master UI]                              [FE-M3: Master UI]                [BE-M3: Master Data]
       │                                                 │                                 │
       └───────────────────────────────────────┬─────────┴─────────────────────────────────┘
                                               ▼
                                     [INT-M3: Master Gate]
                                               │
       ┌───────────────────────────────────────┴───────────────────────────────────────────┐
       ▼                                       ▼                                           ▼
[UX-M4: Attendance]                   [FE-M4: Attendance UI]                      [BE-M4: Attendance BE]
       │                                       │                                           │
       └───────────────────────────────────────┼───────────────────────────────────────────┤
                                               ▼                                           │
                                     [INT-M4: Attendance Gate]                             │
                                               │                                           │
       ┌───────────────────────────────────────┴───────────────────┐                       │
       ▼                                                           ▼                       ▼
[UX-M5: Student Affairs]                              [FE-M5: Affairs UI]         [BE-M5: Student Affairs]
       │                                                           │                       │
       └───────────────────────────────────────────────────────────┼───────────────────────┤
                                                                   ▼                       │
                                                         [INT-M5: Affairs Gate]            │
                                                                   │                       │
       ┌───────────────────────────────────────────────────────────┴───────────────────────┤
       ▼                                                           ▼                       ▼
[UX-M6: Administration]                               [FE-M6: Admin UI]           [BE-M6: Administration]
       │                                                           │                       │
       └───────────────────────────────────────────────────────────┼───────────────────────┤
                                                                   ▼                       │
                                                          [INT-M6: Admin Gate]             │
                                                                   │                       │
       ┌───────────────────────────────────────────────────────────┴───────────────────────┘
       ▼                                                           ▼
[UX-M7: Dashboard/Analytics]                          [BE-M7: Reports/Redis]
       │                                                           │
       └───────────────────────────────┬───────────────────────────┘
                                       ▼
                             [FE-M7: Dashboard UI]
                                       │
                                       ▼
                             [INT-M7: Reports Gate]
                                       │
                                       ▼
                       [UX-M8 / FE-M8 / BE-M8 / INT-M8: Full System E2E]
```

### Penjelasan Pola Dependensi:
- **Backend Track (`BE-Mx`):** Hanya membutuhkan spesifikasi kontrak OpenAPI dan DBML modul terkait berstatus `APPROVED` atau `FROZEN`. Tidak membutuhkan generated TypeScript frontend maupun selesainya desain Pencil.
- **Frontend Track (`FE-Mx`):** Scaffolding logika, routing, state TanStack Query, dan form validasi Zod dapat dibangun segera setelah kontrak modul berstatus `APPROVED`. Finalisasi visual antarmuka diselaraskan dengan hasil sign-off desain dari Pencil Track.
- **Pencil Design Track (`UX-Mx`):** Beroperasi mandiri berdasarkan dokumen kebutuhan PRD, AFD, dan standar UID.md tanpa menunggu kode.
- **Integration Gate (`INT-Mx`):** Menguji sambungan HTTP nyata, kebenaran otorisasi peran, kesesuaian visual terhadap hasil sign-off Pencil, dan konsistensi data di database.

---

## 3. Rincian Milestone Integrasi (INT-M1 s/d INT-M8)

| Milestone | Prasyarat Masuk | Fokus Pengujian & Verifikasi Nyata | Kriteria Lolos (Exit Criteria) |
|---|---|---|---|
| **INT-M1: Foundation Gate** | BE-M1, FE-M1, UX-M1 | Kompatibilitas skema error envelope, token styling dasar, CORS header, healthcheck | API healthcheck merespons 200, frontend menangani format error terstandar |
| **INT-M2: Auth Gate** | BE-M2, FE-M2, UX-M2, INT-M1 | Alur Login riil, penyimpanan token JWT, header Authorization, refresh token otomatis, dan Logout | Pengguna berhasil login, navigasi menu sesuai peran, logout memutus sesi |
| **INT-M3: Master Gate** | BE-M3, FE-M3, UX-M3, INT-M2 | Kueri daftar siswa terpaginasi, pencarian server-side, form tambah/edit data master | Data yang dibuat di frontend tersimpan di database dan tampil pada tabel |
| **INT-M4: Attendance Gate** | BE-M4, FE-M4, UX-M4, INT-M3 | Skenario A (Tahap 1): Roster kelas termuat, toggle H/S/I/A, simpan batch atomik, rekap kehadiran | Seluruh baris kehadiran tersimpan, rekap kelas terhitung akurat, histori audit tercipta |
| **INT-M5: Affairs Gate** | BE-M5, FE-M5, UX-M5, INT-M4 | Skenario A (Tahap 2): Pembuatan kasus, transisi status, pencatatan kronologis tindakan | Timeline kasus bertambah, optimistic locking 409 terverifikasi saat konflik |
| **INT-M6: Admin Gate** | BE-M6, FE-M6, UX-M6, INT-M3 | Skenario B: Pengajuan surat, upload berkas privat, persetujuan pimpinan, unduh privat | Alur status tuntas, berkas tersimpan privat dan dapat diunduh pihak berwenang |
| **INT-M7: Reports Gate** | BE-M7, FE-M7, UX-M7, INT-M4-6 | Sinkronisasi metrik dashboard, ekspor Excel dan PDF dengan filter tanggal, Redis cache | Angka dashboard cocok dengan database, berkas Excel dan PDF berhasil diunduh |
| **INT-M8: Final Verification** | BE-M8, FE-M8, UX-M8, INT-M7 | Skenario E2E penuh (A dan B), audit keamanan IDOR, audit a11y WCAG 2.2 AA, evaluasi DSRM | Seluruh skenario penerimaan lulus tanpa cacat kritis; kesiapan evaluasi DSRM |

---

## 4. Strategi Isolasi Git Worktree & Branching

Untuk menjamin Design Agent, Frontend Agent, dan Backend Agent bekerja tanpa saling mengganggu, diterapkan strategi isolasi **Git Worktree**:

### 4.1. Struktur Branching
- `main`: Branch produksi/baseline terverifikasi yang dilindungi.
- `feat/design/<milestone>`: Branch kerja UI/UX Design Agent (misal `feat/design/ux-m4-attendance`).
- `feat/backend/<milestone>`: Branch kerja Backend Agent (misal `feat/backend/be-m4-attendance`).
- `feat/frontend/<milestone>`: Branch kerja Frontend Agent (misal `feat/frontend/fe-m4-attendance`).
- `integration/<milestone>`: Branch pengujian integrasi yang dikelola Integration Agent.

### 4.2. Struktur Worktree Fisik
```text
D:\Kuliah\joki\radit\
  PROJEK istri bg givo/              # Repository Root (branch main)
  sie-design/                       # Git Worktree untuk Design (feat/design/...)
  sie-backend/                      # Git Worktree untuk Backend (feat/backend/...)
  sie-frontend/                     # Git Worktree untuk Frontend (feat/frontend/...)
  sie-integration/                  # Git Worktree untuk Integrasi (integration/...)
```

### 4.3. Perintah Standar Pembuatan Worktree (Dijalankan Saat Memulai Implementasi)
```bash
# Membuat worktree untuk pengerjaan desain Pencil
git worktree add -b feat/design/ux-m1-foundations ../sie-design main

# Membuat worktree untuk pengerjaan backend
git worktree add -b feat/backend/be-m1-foundation ../sie-backend main

# Membuat worktree untuk pengerjaan frontend
git worktree add -b feat/frontend/fe-m1-foundation ../sie-frontend main

# Membuat worktree untuk integrasi modul
git worktree add -b integration/int-m1-foundation ../sie-integration main
```

### 4.4. Isolasi Lingkungan Eksekusi
- **Pencil MCP:** Beroperasi di `design/**` dan berkomunikasi via MCP stdio client.
- **Python venv:** Virtual environment terisolasi di direktori backend (`.venv`).
- **Node modules:** Dependensi terinstal lokal di direktori frontend (`frontend/node_modules`).
- **Database & Media:** Basis data pengujian menggunakan file terpisah (`test_db.sqlite3` atau skema terisolasi), dan private storage terpisah (`test_private_media/`).
- **Port Layanan:** Backend dev server pada `localhost:8000`, Frontend dev server pada `localhost:5173`.

---

## 5. Tata Kelola Konflik dan Batas Perbaikan Kode

1. **Aturan Kepemilikan Mutlak:**
   - Backend Agent **DILARANG KERAS** memodifikasi file di dalam direktori `frontend/**` atau `design/**`.
   - Frontend Agent **DILARANG KERAS** memodifikasi file di dalam direktori `backend/**` atau `design/**`.
   - Design Agent **DILARANG KERAS** memodifikasi kode di dalam direktori `backend/**` atau `frontend/**`.
2. **Penanganan Masalah Saat Integrasi:**
   - Jika saat pengujian integrasi ditemukan bahwa backend mengembalikan format data yang salah, Integration Agent atau Frontend Agent **TIDAK BOLEH** memperbaiki backend secara langsung.
   - Buat tiket temuan pada `coordination/PROJECT_STATUS.md` dan delegasikan perbaikan kepada Backend Agent.
3. **Ketidaksesuaian Kontrak:**
   - Jika ditemukan kekurangan pada kontrak API yang ada, seluruh agent wajib menahan perubahan kode dan mengajukan perubahan melalui protokol *Contract Change Request* pada `coordination/CONTRACT_CHANGE_REQUESTS.md`.
