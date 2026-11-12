# Documentation Alignment & Consistency Audit Report (M0.1)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Tanggal Audit | 12 November 2026 |
| Tahap Proyek | M0.1 - Documentation Alignment Correction & Pencil Design Track |
| Auditor | Senior Software Architect, Security Auditor & Integration Lead |
| Cakupan Dokumen | PRD, TRD, DBD, BSD, AFD, IPD, UID, RBAC_MATRIX, DECISION_LOG, Contracts |
| Status Baseline | PARTIALLY_ALIGNED (Technical Architecture Fully Aligned; Open Business Policies Governed by Deny-by-Default) |

---

## 1. Ringkasan Eksekutif Audit

Audit konsistensi silang (*cross-document consistency audit*) tahap M0.1 meninjau kembali 22 poin audit arsitektur dan bisnis untuk memisahkan secara tegas antara:
1. **Keputusan teknis yang telah tervalidasi dan disepakati (RESOLVED).**
2. **Poin yang telah selaras secara arsitektural namun masih memerlukan penegasan kebijakan atau verifikasi runtime (PARTIALLY_RESOLVED).**
3. **Keputusan bisnis yang masih terbuka (*open proposals*) dan diatur secara ketat dengan aturan Deny-by-Default (OPEN / PENDING_APPROVAL).**

Dokumen ini secara jujur menetapkan status proyek sebagai **PARTIALLY_ALIGNED** (bukan *Fully Aligned* semu), karena terdapat batasan operasional sekolah riil yang sedang menunggu validasi wawancara lapangan di SMA Negeri 1 Bunut.

---

## 2. Klasifikasi Status Audit 22 Poin

| Status | Definisi Operasional | Jumlah Poin |
|---|---|---|
| `RESOLVED` | Telah diselaraskan penuh lintas seluruh dokumen, kontrak, dan rencana eksekusi | 18 poin |
| `PARTIALLY_RESOLVED` | Solusi arsitektur telah ditetapkan, namun menunggu verifikasi runtime atau konfirmasi SOP sekolah | 4 poin |
| `OPEN` | Masalah bisnis terbuka yang menunggu data observasi/wawancara (diatur via Deny-by-Default) | 0 poin (terakomodasi di PENDING_APPROVAL) |
| `BLOCKED` | Terdapat hambatan yang menghentikan pekerjaan berikutnya | 0 poin (tidak ada blocker untuk fondasi M1) |
| `NOT_VERIFIED` | Spesifikasi lengkap tetapi belum diverifikasi oleh test suite eksekusi riil | Seluruh implementasi kode (Tahap M0 adalah documentation-only) |

---

## 3. Rincian Evaluasi Mendalam 22 Poin Audit

### Poin 1: Ketidaksesuaian izin antara PRD, AFD, BSD, dan UID
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED` (Dokumentasi), `NOT_VERIFIED` (Runtime)
- **Analisis & Resolusi:**
  - Telah disepakati prinsip universal: Otorisasi backend **wajib memvalidasi izin riil dan kepemilikan objek** (*object-level permissions*), sedangkan tombol ganti konteks peran di antarmuka web hanya bertindak sebagai filter tampilan (*view filter*).
  - Multi-peran dievaluasi secara aditif (*disjunctive union*), di mana hak akses sah dari satu peran tidak dibatalkan oleh peran lain kecuali terkena larangan keamanan global (*global security boundary*).

---

### Poin 2: Hak wali kelas memulai penanganan kasus dan koreksi absensi
- **Prioritas:** P1 (Important)
- **Status:** `PARTIALLY_RESOLVED`
- **Analisis & Resolusi:**
  - Hak Wali Kelas untuk membuat dan memulai kasus kesiswaan (`BARU -> DIPROSES`) bagi siswa di kelas binaannya telah disepakati (`ALLOWED`).
  - Terkait koreksi absensi: Koreksi <= 24 jam dengan catatan audit telah disepakati (`ALLOWED`), namun kewenangan koreksi > 24 jam tanpa izin pimpinan ditandai sebagai `PENDING_APPROVAL` dan ditegakkan sebagai `DENIED` pada runtime sistem hingga ada SOP resmi.

---

### Poin 3: Hak Tata Usaha (TU) mengelola data siswa
- **Prioritas:** P1 (Important)
- **Status:** `PARTIALLY_RESOLVED`
- **Analisis & Resolusi:**
  - Hak staf TU untuk membaca data demografis siswa (`GET /api/master/students`, `GET /api/master/students/{id}`) untuk pembuatan surat keterangan telah disepakati (`ALLOWED`).
  - Hak staf TU mendaftarkan atau memperbarui data pokok siswa baru (NIS, status) berstatus `PENDING_APPROVAL` (kebijakan Dapodik sekolah). Di tingkat runtime, izin ini berstatus `DENIED` secara default (dikelola oleh Administrator).

---

### Poin 4: Hak Administrator terhadap kehadiran dan catatan konseling sensitif
- **Prioritas:** P0 (Critical / Security)
- **Status:** `RESOLVED` (Spesifikasi), `NOT_VERIFIED` (Runtime)
- **Analisis & Resolusi:**
  - Penegakan pemisahan tugas (*separation of duties*): Administrator mengelola infrastruktur akun, peran, dan konfigurasi master data.
  - Administrator **dilarang keras** memiliki akses otomatis membaca isi narasi konseling privat bimbingan konseling atau mengunduh dokumen lampiran siswa privat tanpa penugasan fungsional operasional.

---

### Poin 5: Hak pimpinan melihat antrean persetujuan dan audit
- **Prioritas:** P1 (Important)
- **Status:** `PARTIALLY_RESOLVED`
- **Analisis & Resolusi:**
  - Pimpinan memiliki hak `LIST` dan `READ` pada antrean permohonan surat yang membutuhkan disposisi (`status=MENUNGGU_PERSETUJUAN`) serta hak aksi `APPROVE` dan `REJECT` (`ALLOWED`).
  - Hak membaca log audit teknis lengkap tetap dikhususkan bagi Administrator. Hak pimpinan membaca log aktivitas persetujuan berstatus `PENDING_APPROVAL` (diisolasi dari log teknis internal).

---

### Poin 6: Kelengkapan endpoint pendukung Screen S01-S18
- **Prioritas:** P0 (Critical / Blocking)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Seluruh 18 screen telah dipetakan ke endpoint OpenAPI yang sesuai. Endpoint untuk master pegawai (`/master/employees`), penugasan (`/master/assignments`), dan akun (`/accounts/users`) telah didefinisikan secara lengkap pada kontrak.

---

### Poin 7: Endpoint manajemen akun, role, dan penugasan
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Kontrak mencakup `/api/accounts/users` (GET, POST), `/api/accounts/users/{id}` (PATCH), `/api/accounts/roles` (GET), dan `/api/master/assignments` (GET, POST) dengan skema request/response terstandar.

---

### Poin 8: Endpoint roster kehadiran berdasarkan kelas dan tanggal
- **Prioritas:** P0 (Critical / Blocking)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Endpoint `GET /api/attendance/roster?class_id={id}&date={YYYY-MM-DD}` menyediakan daftar siswa aktif beserta status absensi historis yang telah terisi (jika ada).

---

### Poin 9: Kontrak daftar arsip dokumen dan pengunduhan aman
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Endpoint `GET /api/administration/documents` dan `GET /api/administration/documents/{id}/download` terdefinisi dengan otorisasi berbasis hak kepemilikan data.

---

### Poin 10: Pencatatan tindakan kasus tanpa perubahan status
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Kontrak transisi kasus mendukung aksi `CATAT_TINDAKAN` di mana status kasus tetap `DIPROSES`, tetapi baris rekaman baru ditambahkan pada tabel `CaseEvent`.

---

### Poin 11: Alur layanan yang memerlukan atau tidak memerlukan persetujuan
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Master data `ServiceType` memiliki flag `requires_approval: boolean`. Layanan yang memerlukan tanda tangan dialihkan ke `MENUNGGU_PERSETUJUAN`, sedangkan layanan biasa dapat langsung diselesaikan oleh staf TU.

---

### Poin 12: Status DITOLAK tidak otomatis menjadi SELESAI
- **Prioritas:** P0 (Critical / Integrity)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Status `DITOLAK` ditetapkan sebagai terminal state terpisah yang mewajibkan pencatatan alasan penolakan pada `ServiceEvent`. Surat yang ditolak dilarang diterbitkan.

---

### Poin 13: Kesesuaian kolom version dengan kontrol konkurensi optimistik
- **Prioritas:** P0 (Critical / Concurrency)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Kolom `version: integer` diterapkan pada `StudentCase` dan `ServiceRequest`. Setiap mutasi memeriksa `expected_version` dan melempar HTTP 409 Conflict jika terjadi benturan versi.

---

### Poin 14: Konkurensi penyimpanan batch kehadiran: Transaksi Atomik vs Lost Update
- **Prioritas:** P0 (Critical / Data Integrity)
- **Status:** `PARTIALLY_RESOLVED`
- **Koreksi Fundamental:**
  - **Pemberitahuan Arsitektur:** Transaksi atomik (`transaction.atomic()`) **hanya menjamin penulisan all-or-nothing**; transaksi atomik **TIDAK** otomatis menyelesaikan masalah *lost update* jika dua guru membuka roster yang sama lalu menyimpan pembaruan secara berselisih waktu!
  - **Solusi Komprehensif:** Menerapkan constraint unik komposit basis data `UNIQUE(student_id, class_id, date)`, validasi integritas seluruh siswa sebelum mutasi, dan penanganan benturan dengan melempar HTTP 409 Conflict serta instruksi reload data.

---

### Poin 15: Keamanan cache key berdasarkan cakupan akses efektif
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Format key Redis distandarkan: `{domain}:{scope_type}:{scope_id}:{params_hash}` untuk mencegah eksfiltrasi data antarkelas atau antarperan. Pembersihan cache dieksekusi via `transaction.on_commit()`.

---

### Poin 16: JWT access token, refresh token, rotasi, blacklist, dan logout
- **Prioritas:** P0 (Critical / Security)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Access token berumur 15 menit disimpan di memory client. Refresh token berumur 7 hari disimpan dalam cookie `httpOnly`, `secure`, `SameSite=Strict`. Rotasi token otomatis dijalankan pada setiap pemanggilan refresh. Logout memasukkan refresh token ke blacklist.

---

### Poin 17: Kebijakan keamanan kegagalan Redis (Fail-Closed vs Fail-Open)
- **Prioritas:** P0 (Critical / Security)
- **Status:** `RESOLVED`
- **Koreksi Fundamental:**
  - **Pemberitahuan Arsitektur:** Fallback Redis tidak boleh melemahkan sistem otentikasi, pembatasan laju, atau pencabutan sesi!
  - **Kebijakan Ditetapkan:**
    - **Fail-Closed untuk Keamanan:** Pengecekan blacklist pembatalan sesi token dan rate limiting brute-force login wajib menolak akses atau mengalihkan verifikasi ke basis data jika Redis mati.
    - **Fail-Open untuk Caching:** Caching respon kueri non-kritis (dashboard/rekapitulasi) dialihkan langsung mengeksekusi kueri ke basis data tanpa melempar error sistem.

---

### Poin 18: Validasi, penyimpanan, dan pengunduhan dokumen privat
- **Prioritas:** P0 (Critical / Security)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Berkas fisik disimpan di `PRIVATE_MEDIA_ROOT` dengan nama UUID acak tanpa ekstensi terbuka di filesystem. Streaming pengunduhan terproteksi oleh Django `FileResponse` yang memvalidasi kepemilikan data.

---

### Poin 19: Audit history pada operasi bulk
- **Prioritas:** P0 (Critical / Audit Integrity)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Wajib menggunakan `simple_history.utils.bulk_create_with_history` dan `bulk_update_with_history` di dalam transaksi atomik untuk memastikan seluruh rekaman presensi massal memiliki jejak audit.

---

### Poin 20: Protokol penelitian DSRM, pengukuran konsistensi data, dan pengendalian bias
- **Prioritas:** P1 (Important)
- **Status:** `RESOLVED`
- **Pemulihan Detail DSRM:**
  - Formula pengukuran konsistensi data dipulihkan ke `docs/IPD.md`: *Referential Integrity Ratio (RIR)*, *Data Duplication Index (DDI)*, dan *Optimistic Concurrency Success Rate (OCSR)*.
  - Pengendalian bias evaluasi mencakup pemilihan responden independen, panduan fasilitator terstandar, pengujian berpasangan (*paired t-test* / *Wilcoxon*), dan evaluasi SUS mandiri.
  - Matriks Keterlacakan Kebutuhan (*Requirements Traceability Matrix*) menghubungkan PRD -> AFD -> DBML -> OpenAPI -> Screen -> Test Suite.

---

### Poin 21: Struktur pengembangan multi-jalur (Three Production Tracks + Integration)
- **Prioritas:** P0 (Critical / Architecture)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Roadmap diselaraskan menjadi 3 jalur produksi independen:
    1. **UI/UX Design Track (Pencil MCP):** `UX-M1` s/d `UX-M8` di `design/**`.
    2. **Frontend Development Track (React TypeScript):** `FE-M1` s/d `FE-M8` di `frontend/**`.
    3. **Backend Development Track (Django Ninja):** `BE-M1` s/d `BE-M8` di `backend/**`.
    Ditambah **Coordinator / Integration Track:** `INT-M1` s/d `INT-M8`.
  - Backend tidak bergantung pada desain UI atau frontend. Frontend dapat memulai fondasi dari kontrak tanpa menunggu backend selesai. Finalisasi visual frontend mengikuti hasil sign-off desain dari Pencil.

---

### Poin 22: Pembersihan tipografi, format karakter, dan tautan dokumen
- **Prioritas:** P2 (Improvement)
- **Status:** `RESOLVED`
- **Analisis & Resolusi:**
  - Seluruh karakter rusak `?` telah diperbaiki menjadi panah `->`, em dash nonstandar dibersihkan, format tabel rapi, dan tautan internal file tervalidasi.

---

## 4. Matriks Status Penyelarasan Dokumen Akhir

| Dokumen | Status Dokumen | Status Penyelarasan | Catatan Sinkronisasi |
|---|---|---|---|
| `PRD.md` | Active Baseline | ALIGNED | Batasan multi-peran dan kebutuhan fungsional selaras |
| `TRD.md` | Active Baseline | ALIGNED | Kompatibilitas Windows, Redis failure policy, dan arsitektur selaras |
| `DBD.md` & `database.dbml` | Frozen Baseline v1.0 | ALIGNED | Kolom `version`, indeks komposit, dan relasi tabel selaras |
| `BSD.md` | Active Baseline | ALIGNED | Endpoint S01-S18, kontrol konkurensi, dan RBAC selaras |
| `AFD.md` | Active Baseline | ALIGNED | Alur kerja Skenario A & B, panah transisi `->` selaras |
| `UID.md` | Active Baseline | ALIGNED | 18 rancangan screen, tema Institutional Navy & Teal selaras |
| `IPD.md` | Active Baseline | ALIGNED | Three-track multi-production model, DSRM metrics dipulihkan |
| `RBAC_MATRIX.md` | Working Baseline | PARTIALLY_ALIGNED | Deny-by-default ditegakkan; item PENDING_APPROVAL terkendali |
| `DECISION_LOG.md` | Managed Baseline | ALIGNED | 15 keputusan teknis APPROVED & 5 usulan bisnis PROPOSED tercatat |
| `DESIGN_EXECUTION_PLAN.md` | Approved Baseline | ALIGNED | 8 milestone UX-M1 s/d UX-M8 terdefinisi dengan Pencil MCP |
| `BACKEND_EXECUTION_PLAN.md` | Approved Baseline | ALIGNED | 8 milestone BE-M1 s/d BE-M8 terdefinisi secara independen |
| `FRONTEND_EXECUTION_PLAN.md`| Approved Baseline | ALIGNED | 8 milestone FE-M1 s/d FE-M8 terdefinisi dengan design handoff |
| `INTEGRATION_PLAN.md` | Approved Baseline | ALIGNED | 8 gerbang integrasi nyata dan Git Worktrees terdefinisi |
