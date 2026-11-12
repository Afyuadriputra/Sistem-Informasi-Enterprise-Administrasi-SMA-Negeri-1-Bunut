# Project Architectural & Business Decision Log

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Status Log | ACTIVE & MANAGED |
| Terakhir Diperbarui | 12 November 2026 |
| Pengelola | Senior Software Architect / Integration Agent |
| Acuan | PRD, TRD, DBD, BSD, AFD, IPD, UID, AGENTS.md |

---

## 1. Bagian A: Keputusan Arsitektur & Teknis (Approved Technical Decisions)

Bagian ini memuat keputusan arsitektur dan teknis yang telah diselaraskan lintas dokumen untuk memandu pengerjaan Backend, Frontend, Design, dan Integrasi.

### DEC-TECH-01: Pendekatan Pengembangan Paralel Berbasis Kontrak (Contract-First Parallel Development)
- **Context:** Pengembangan frontend, backend, dan desain dikerjakan secara paralel oleh agent mandiri.
- **Source Document:** TRD §1, IPD §2, task/task1.md §3.
- **Problem:** Ketergantungan sekuensial memperlambat siklus iterasi dan menimbulkan risiko inkonsistensi payload antarmuka.
- **Decision:** Menetapkan `contracts/openapi.v1.yaml` dan `contracts/database.dbml` sebagai acuan spesifikasi. Modul yang kontraknya telah `APPROVED` atau `FROZEN` dapat diimplementasikan mandiri oleh masing-masing agen tanpa saling memblokir.
- **Alternative:** Code-first development (backend membuat endpoint terlebih dahulu lalu mengekspor OpenAPI).
- **Impact:** Frontend dan Backend Agent dapat bekerja di branch/worktree terisolasi.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `contracts/openapi.v1.yaml`, `contracts/README.md`, `IPD.md`.

---

### DEC-TECH-02: Otorisasi Berbasis Objek (Object-Level Scoping) dan Resolusi Multi-Peran
- **Context:** Staf sekolah dapat mengemban beberapa peran sekaligus (contoh: Guru yang juga Wali Kelas).
- **Source Document:** PRD §2/§8, BSD §4, UID §2.1.
- **Problem:** Pengecekan berbasis peran global berisiko memicu celah IDOR (Guru A mengakses presensi kelas Guru B).
- **Decision:** Server Django Ninja selalu memverifikasi penugasan objek riil di basis data (`ClassAssignment`, penugasan kasus kesiswaan). Evaluasi izin multi-peran bersifat aditif (*disjunctive union*) tanpa membatalkan hak peran lain, kecuali terdapat larangan keamanan global (*global security boundary*). Pemilihan konteks peran di UI hanya sebagai filter tampilan.
- **Alternative:** Mengandalkan klaim token peran yang dipilih pengguna di antarmuka frontend.
- **Impact:** Mencegah celah IDOR pada tingkat arsitektur kueri (`selectors.py`), diverifikasi melalui test suite terotomasi.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `docs/RBAC_MATRIX.md`, `BSD.md §4`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-03: Kontrol Konkurensi Optimistik pada Entitas Kasus dan Permohonan
- **Context:** Banyak pengguna dapat membuka kasus kesiswaan atau permohonan surat yang sama secara bersamaan.
- **Source Document:** DBD §8, BSD §3/§7, UID §8.
- **Problem:** Terjadinya *lost update* saat dua pengguna menimpa status tanpa mengetahui perubahan yang terjadi di server.
- **Decision:** Menambahkan kolom `version: integer` pada entitas `StudentCase` dan `ServiceRequest`. Setiap aksi mutasi status wajib mengirimkan `expected_version`. Jika versi di database tidak cocok, server mengembalikan status HTTP 409 Conflict.
- **Alternative:** Pessimistic locking menggunakan `SELECT FOR UPDATE` sepanjang sesi antarmuka (dapat mengunci koneksi basis data terlalu lama).
- **Impact:** Antarmuka frontend menangani HTTP 409 dengan menyajikan dialog rekonsiliasi dan memuat ulang data terbaru.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `DBD.md §8`, `BSD.md §7`, `contracts/database.dbml`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-04: Transaksi Atomik dan Bulk History untuk Absensi Kelas Harian
- **Context:** Penyimpanan absensi harian melibatkan puluhan siswa sekaligus dalam satu request batch.
- **Source Document:** DBD §5, BSD §3.1, TRD §6.
- **Problem:** `django-simple-history` pada pemanggilan `bulk_create` bawaan melewati sinyal `post_save`, sehingga histori audit absensi massal dapat terlewat.
- **Decision:** Wajib menggunakan `simple_history.utils.bulk_create_with_history` dan `bulk_update_with_history` di dalam blok transaksi atomik (`transaction.atomic()`). Jika satu siswa tidak valid, seluruh batch di-rollback (*all-or-nothing*).
- **Alternative:** Iterasi `save()` satu per satu (lambat dan memicu banyak round-trip basis data).
- **Impact:** Seluruh baris presensi tersimpan lengkap bersama rekam jejak audit; kegagalan input tertolak secara konsisten.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `DBD.md §5`, `BSD.md §3.1`, `TRD.md §6`.

---

### DEC-TECH-05: Penyimpanan Berkas Privat Terisolasi dan Streaming Unduhan Terproteksi
- **Context:** Permohonan surat menyertakan lampiran berkas identitas siswa (KK, Akta, Surat Pengantar).
- **Source Document:** PRD §3 (FR-06), TRD §5, BSD §3.3.
- **Problem:** Menyimpan berkas di folder publik (`/media/`) memungkinkan eksfiltrasi dokumen oleh pihak yang menebak URL.
- **Decision:** Berkas disimpan di direktori privat (`PRIVATE_MEDIA_ROOT`) dengan penamaan UUID acak tanpa ekstensi terbuka di filesystem. Unduhan dilayani melalui endpoint terproteksi (`GET /api/administration/documents/{id}/download`) menggunakan Django `FileResponse` yang memvalidasi otorisasi pengguna.
- **Alternative:** Direct static URL dengan token signature di query param (rawan bocor di history browser).
- **Impact:** Berkas privat siswa terlindungi dari akses publik dan akses tidak sah.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `TRD.md §5`, `BSD.md §3.3`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-06: Penanganan Kompatibilitas Dependensi Lingkungan Windows Lokal
- **Context:** Pengembangan dan demonstrasi prototype dijalankan pada lingkungan sistem operasi Windows.
- **Source Document:** TRD §2, task/task1.md §2.
- **Problem:** Pustaka `python-magic` membutuhkan binary C `libmagic.dll` dan `WeasyPrint` membutuhkan dependensi native GTK/Cairo.
- **Decision:** Menggunakan `python-magic-bin` atau modul inspeksi byte header murni sebagai fallback deteksi MIME, serta menggunakan `ReportLab` sebagai generator PDF default di lingkungan Windows.
- **Alternative:** Memaksakan container Docker WSL2 (dapat membebani sumber daya mesin lokal).
- **Impact:** Lingkungan pengujian backend di Windows berjalan stabil tanpa kendala kompilasi binary C.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `TRD.md §2`, `docs/execution/BACKEND_EXECUTION_PLAN.md`.

---

### DEC-TECH-07: Strategi Penyimpanan JWT, Mitigasi CSRF, dan Session Revocation
- **Context:** Pengelolaan token autentikasi pada Single Page Application (React) dan REST API (Django Ninja).
- **Source Document:** TRD §5, BSD §2/§4.
- **Problem:** Menyimpan access dan refresh token di `localStorage` rentan terhadap pencurian via Cross-Site Scripting (XSS). Sementara itu, JWT stateless secara default sulit dicabut sebelum masa kedaluwarsa berakhir.
- **Decision:**
  - Access token berumur pendek (15 menit) disimpan di memory client (Zustand store).
  - Refresh token (7 hari) dikirimkan via cookie `httpOnly`, `secure`, `SameSite=Strict`.
  - Endpoint yang menerima cookie dilindungi verifikasi header anti-CSRF (`X-CSRFToken`).
  - Sesi revocation: Saat logout atau penggantian password, refresh token dan identifier sesi dimasukkan ke daftar blacklist di Redis/basis data.
- **Alternative:** Menyimpan seluruh token di `localStorage` (rawan XSS) atau sesi berbasis session cookie stateful tradisional (kurang cocok untuk arsitektur API modular).
- **Impact:** Memitigasi risiko pencurian token XSS dan menyediakan mekanisme pemutusan sesi aktif secara seketika.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `TRD.md §5`, `BSD.md §4`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-08: Kebijakan Keamanan Kegagalan Redis (Redis Security Failure Policy)
- **Context:** Redis digunakan untuk caching respon kueri, pembatasan laju (*rate limiting*), dan pengecekan blacklist sesi token.
- **Source Document:** TRD §2/§5, BSD §4.
- **Problem:** Jika layanan Redis mengalami gangguan atau terputus, sistem harus menentukan apakah operasi diizinkan (*fail-open*) atau ditolak (*fail-closed*).
- **Decision:**
  - **Fail-Closed untuk Keamanan Kritis:** Pengecekan blacklist sesi token saat autentikasi dan counter rate limiting brute-force login wajib beroperasi secara *fail-closed* (jika Redis mati, alihkan pengecekan ke tabel blacklist database; jika verifikasi keamanan gagal total, tolak permintaan demi mencegah penyalahgunaan token dicabut).
  - **Fail-Open untuk Caching Non-Kritis:** Caching respon dashboard dan rekapitulasi kehadiran beroperasi secara *fail-open* (jika Redis mati, kueri langsung diarahkan ke basis data relasional tanpa melempar HTTP 500).
- **Alternative:** Seluruh sistem fail-open (membuka celah keamanan saat Redis mati) atau seluruh sistem fail-closed (sistem mati total jika cache padam).
- **Impact:** Keamanan autentikasi tetap terjaga ketat sementara layanan data tetap beroperasi secara *graceful*.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `TRD.md §5`, `BSD.md §4`, `docs/execution/BACKEND_EXECUTION_PLAN.md`.

---

### DEC-TECH-09: Isolasi Cache Redis Berdasarkan Cakupan Akses Efektif
- **Context:** Pemanfaatan caching Redis untuk mempercepat kueri rekapitulasi kehadiran dan ringkasan dashboard operasional.
- **Source Document:** BSD §5, TRD §6.
- **Problem:** Kunci cache generik (misal `cache:attendance:summary`) berisiko membocorkan data antarkelas atau antarperan pengguna.
- **Decision:** Kunci cache wajib menyertakan namespace cakupan akses: `{domain}:{scope_type}:{scope_id}:{params_hash}`. Contoh: `attendance:class:10:recap_hash` atau `dashboard:user:12:guru_hash`. Pembersihan cache dilakukan otomatis via `transaction.on_commit()` pada saat transaksi mutasi data terkait selesai dieksekusi.
- **Alternative:** Caching global per peran tanpa menyertakan ID objek penugasan.
- **Impact:** Menghilangkan risiko kebocoran data silang (*cross-tenant data leakage*) di tingkat cache memory.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `BSD.md §5`, `docs/execution/BACKEND_EXECUTION_PLAN.md`.

---

### DEC-TECH-10: Pembedaan Tegas Transaksi Atomik vs Pencegahan Lost Update
- **Context:** Penanganan konkurensi pada operasi mutasi kasus kesiswaan, permohonan surat, dan absensi harian.
- **Source Document:** DBD §8, BSD §3/§7.
- **Problem:** Sering terjadi salah kaprah bahwa membungkus kueri dengan `transaction.atomic()` otomatis menyelesaikan masalah *lost update*.
- **Decision:**
  - `transaction.atomic()` hanya menjamin sifat *Atomicity* (seluruh baris berhasil ditulis atau seluruhnya dibatalkan); transaksi atomik **tidak mencegah** *lost update* jika dua klien membaca versi data yang sama secara bersamaan lalu menimpa record tersebut secara berurutan.
  - Pencegahan *lost update* dilakukan secara eksplisit menggunakan **Optimistic Concurrency Control** via kolom `version: integer` dan parameter `expected_version`. Mutasi dieksekusi dengan klausa `UPDATE ... WHERE id = :id AND version = :expected_version`. Jika baris yang terpengaruh bernilai 0, sistem membatalkan transaksi dan mengembalikan HTTP 409 Conflict.
- **Alternative:** Mengandalkan database isolation level SERIALIZABLE (dapat menurunkan throughput secara drastis).
- **Impact:** Logika konkurensi terdefinisi jelas pada arsitektur service layer dan kontrak API.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `DBD.md §8`, `BSD.md §7`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-11: Penanganan Konkurensi Penyimpanan Batch Absensi Kelas
- **Context:** Input absensi satu rombel kelas (30-40 siswa) dikirim serentak dan berpotensi mengalami koreksi atau tumpang-tindih input antar guru/wali kelas.
- **Source Document:** BSD §3.1, DBD §5.
- **Problem:** Kemungkinan terjadi duplikasi entri presensi untuk siswa dan tanggal yang sama pada kondisi balapan jaringan (*race condition*).
- **Decision:**
  - Penegakan integritas di basis data melalui constraint unik komposit: `UNIQUE(student_id, class_id, date)`.
  - Service layer memvalidasi integritas seluruh siswa sebelum penulisan, mengunci penempatan aktif dengan `select_for_update` pada transaksi atomik singkat, dan mengeksekusi operasi upsert terkontrol dengan rekam jejak `HistoricalRecords`. Jika terjadi benturan constraint unik, kueri di-rollback dan mengembalikan HTTP 409 Conflict dengan instruksi reload roster.
- **Alternative:** Mengizinkan duplikasi lalu melakukan deduplikasi kueri di level pembacaan (merusak akurasi audit).
- **Impact:** Integritas data absensi terjaga dan konkurensi jaringan ditangani secara teratur.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `DBD.md §5`, `BSD.md §3.1`, `contracts/database.dbml`.

---

### DEC-TECH-12: Strategi Isolasi Git Worktree dan Kepemilikan Berkas
- **Context:** Tiga jalur produksi (Design, Backend, Frontend) dan Integrasi dikembangkan secara simultan.
- **Source Document:** TRD §1, AGENTS.md §3, IPD §2.
- **Problem:** Konflik penggabungan berkas (*merge conflicts*) dan risiko agen memodifikasi kode di luar wewenangnya.
- **Decision:** Menerapkan struktur repositori Git Worktree terpisah: `sie-design` (`feat/design/...`), `sie-backend` (`feat/backend/...`), `sie-frontend` (`feat/frontend/...`), dan `sie-integration` (`integration/...`). Aturan kepemilikan berkas (*file ownership*) ditegakkan secara ketat pada `AGENTS.md`.
- **Alternative:** Pengerjaan pada satu working tree tunggal (rawan modifikasi file silang).
- **Impact:** Agen dapat mengeksekusi build, run server, dan pengujian secara simultan tanpa konflik berkas.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `AGENTS.md`, `docs/execution/INTEGRATION_PLAN.md`.

---

### DEC-TECH-13: Jalur Produksi Desain Independen Menggunakan Pencil MCP
- **Context:** Pembuatan antarmuka visual, screen mock, dan pengujian kegunaan UX memerlukan lingkungan terstandar.
- **Source Document:** UID.md, task/task1.md.
- **Problem:** Desain seringkali hanya menjadi gambar statis terpisah yang tidak terhubung dengan siklus hidup pengembangan agen.
- **Decision:** Menetapkan **Pencil MCP** (`pen.dev`) sebagai lingkungan perancangan antarmuka resmi. Berkas desain dikelola pada `design/**` dan berkas `.pen` diakses secara eksklusif via MCP tools. Desain dibagi ke dalam 8 milestone mandiri (`UX-M1` s/d `UX-M8`).
- **Alternative:** Menggunakan Figma eksternal (memerlukan akun cloud eksternal dan API token pihak ketiga).
- **Impact:** Agen Desain dapat bekerja independen secara lokal dengan representasi visual dan token yang dapat diinspeksi langsung.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `design/AGENTS.md`, `docs/execution/DESIGN_EXECUTION_PLAN.md`, `coordination/DESIGN_STATUS.md`.

---

### DEC-TECH-14: Protokol Design Handoff dan Review Antarmuka Visual
- **Context:** Serah terima spesifikasi visual dari Pencil Design Track ke Frontend Development Track.
- **Source Document:** UID §1-15, DESIGN_EXECUTION_PLAN §1.
- **Problem:** Frontend mengimplementasikan antarmuka secara bebas sehingga menyimpang dari standar UID dan prinsip 25 hukum UX.
- **Decision:** Design Agent mengekspor paket token sistem (`tokens.json`), spesifikasi Golden Ratio, dan visualisasi 5 state antarmuka. Frontend Agent membangun fondasi dari kontrak OpenAPI, namun penutupan milestone frontend wajib memenuhi kriteria kelulusan *Design Sign-off Gate*.
- **Alternative:** Frontend mengarang sendiri styling antarmuka dari deskripsi teks.
- **Impact:** Kualitas antarmuka konsisten, bebas dari AI slop, dan memenuhi standar aksesibilitas WCAG 2.2 AA.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `docs/execution/DESIGN_EXECUTION_PLAN.md`, `frontend/AGENTS.md`, `docs/execution/INTEGRATION_PLAN.md`.

---

### DEC-TECH-15: Tata Kelola Versi Kontrak Modular (Modular Contract Versioning)
- **Context:** Kesiapan kontrak API dan DBML sebelum dimulainya konstruksi kode.
- **Source Document:** contracts/README.md, IPD §4.
- **Problem:** Menuntut seluruh kontrak sistem berstatus `FROZEN` sebelum pekerjaan dimulai menciptakan hambatan kaku (*artificial blocker*) bagi milestone fondasi.
- **Decision:** Kontrak dikelola menggunakan Semantic Versioning dokumen (`v1.0.0`) dengan siklus hidup kesiapan terpisah per modul (`DRAFT` -> `IN_REVIEW` -> `APPROVED` -> `FROZEN`). Fondasi teknis (`BE-M1`, `FE-M1`, `UX-M1`) dapat dimulai segera setelah base envelope dan skema inti disetujui. Setiap revisi kontrak dicatat eksplisit pada `coordination/CONTRACT_CHANGE_REQUESTS.md`.
- **Alternative:** Menunda seluruh pengerjaan sampai wawancara sekolah memfinalisasi seluruh kebijakan bisnis.
- **Impact:** Tim dapat membangun fondasi teknis berkualitas tinggi tanpa melanggar batasan bisnis sekolah.
- **Status:** APPROVED.
- **Dokumen Terdampak:** `contracts/README.md`, `IPD.md`, `coordination/CONTRACT_CHANGE_REQUESTS.md`.

---

## 2. Bagian B: Usulan Kebijakan Bisnis Sekolah (Open Business Proposals Pending School Validation)

Bagian ini memuat aspek bisnis dan tata tertib sekolah yang masih menunggu konfirmasi wawancara dan observasi resmi di SMA Negeri 1 Bunut. Seluruh poin di bawah ini **berstatus PROPOSED dan secara default diperlakukan sebagai DENIED / DRAFT pada runtime sistem**.

### DEC-BIZ-01: Alur Persetujuan Permohonan Surat Tata Usaha
- **Context:** Pemrosesan surat keluar dan permohonan administrasi siswa.
- **Source Document:** PRD §7, AFD §4.
- **Problem:** Apakah seluruh jenis surat wajib ditandatangani/disetujui Kepala Sekolah, atau surat tertentu dapat disahkan langsung oleh Kepala Tata Usaha?
- **Proposed Option:** Menyediakan atribut `requires_approval: boolean` pada master data `ServiceType`. Surat formal membutuhkan persetujuan Kepala Sekolah, sedangkan arsip/legalisir tertentu dapat diselesaikan langsung oleh staf TU jika dikonfigurasi demikian.
- **Status:** PROPOSED (Menunggu validasi dokumen SOP Tata Usaha sekolah).
- **Dampak Teknis:** Skema database dan router API telah mendukung kedua variasi transisi status.

---

### DEC-BIZ-02: Format Penomoran Surat dan Nomor Induk Siswa
- **Context:** Format penomoran otomatis surat dan identitas siswa.
- **Source Document:** PRD §7, DBD §6.
- **Problem:** Format tata naskah dinas resmi dan klasifikasi surat Kemendikbudristek yang diterapkan di SMA Negeri 1 Bunut belum diperoleh secara tertulis.
- **Proposed Option:** Menggunakan format penomoran sementara `REQ/YYYY/MM/XXXX` untuk prototype dan string fleksibel (maks 30 karakter) untuk nomor identitas siswa.
- **Status:** PROPOSED (Menunggu contoh berkas naskah dinas dari sekolah).
- **Dampak Teknis:** Validasi panjang kolom dan constraint keunikan telah dipersiapkan di basis data.

---

### DEC-BIZ-03: Kriteria Ambang Batas Peringatan Ketidakhadiran Siswa
- **Context:** Indikator siswa yang membutuhkan intervensi konseling pada rekapitulasi kehadiran.
- **Source Document:** PRD §3 (FR-04), AFD §3, UID §8.1.
- **Problem:** Berapa batas akumulasi ketidakhadiran (Alpa/Izin) yang memicu status "Perlu Perhatian" pada rekapitulasi wali kelas?
- **Proposed Option:** Menggunakan indikator awal 3 hari Alpa berturut-turut atau akumulasi 5 hari dalam satu bulan kalender sebagai penanda visual di antarmuka (bukan vonis otomatis).
- **Status:** PROPOSED (Menunggu SOP resmi kesiswaan dan bimbingan konseling).
- **Dampak Teknis:** Logika ambang batas diisolasi dalam konfigurasi service layer agar dapat disesuaikan tanpa migrasi skema.

---

### DEC-BIZ-04: Aturan Batas Waktu Koreksi Absensi oleh Guru dan Wewenang Wali Kelas
- **Context:** Koreksi data kehadiran siswa yang telah disimpan sebelumnya.
- **Source Document:** PRD §9 (FR-03), BSD §3.1, docs/RBAC_MATRIX.md.
- **Problem:** Apakah guru diizinkan mengoreksi absensi lebih dari 24 jam, dan apakah wali kelas berwenang mengoreksi absensi kelas binaannya tanpa persetujuan kepala sekolah?
- **Proposed Option:** Guru pencatat diizinkan mengoreksi dalam batas 1x24 jam dari tanggal transaksi. Koreksi lewat dari 24 jam atau koreksi oleh wali kelas membutuhkan persetujuan pimpinan dengan catatan audit wajib.
- **Status:** PROPOSED (Menunggu konfirmasi tata tertib guru; di runtime ditegakkan Deny-by-Default untuk koreksi > 24 jam).
- **Dampak Teknis:** Validasi batas waktu ditegakkan di `attendance/services.py`.

---

### DEC-BIZ-05: Penanganan Kasus Siswa Pindahan / Mutasi di Tengah Semester
- **Context:** Siswa yang masuk atau keluar rombel di pertengahan semester aktif.
- **Source Document:** DBD §7, PRD §9 (FR-02).
- **Problem:** Siswa mutasi tidak boleh muncul pada roster tanggal sebelum tanggal penempatan resminya.
- **Proposed Option:** Menggunakan rentang tanggal eksplisit `start_date` dan `end_date` pada tabel `Enrollment`. Kueri roster selalu memfilter siswa aktif pada tanggal transaksi.
- **Status:** PROPOSED (Secara teknis telah diakomodasi pada skema data untuk verifikasi lanjutan di lapangan).
- **Dampak Teknis:** Skema data `Enrollment` memfasilitasi kebutuhan ini secara penuh.
---

### DEC-TECH-16: Operasi Mutasi Sebagian Master Data (PATCH) dan Siklus Hidup Penugasan
- **Context:** Kebutuhan operasional pembaruan data master (Tahun Ajaran, Kelas, Pegawai, Jenis Layanan) dan siklus penempatan siswa serta penugasan guru di kelas.
- **Source Document:** BSD §3/§4, DBD §5, openapi.v1.yaml, RBAC_MATRIX.md.
- **Problem:** Dokumen RBAC mengizinkan wewenang UPDATE pada entitas master data, namun kontrak OpenAPI baseline 1.0.0 belum mendefinisikan operasi PATCH untuk entitas tersebut. Selain itu, penghapusan data penugasan atau penempatan tidak boleh dilakukan secara hard delete karena merusak integritas audit historis.
- **Decision:**
  - Menambahkan endpoint PATCH resmi pada OpenAPI v1.1.0: `/master/academic-years/{id}`, `/master/classes/{id}`, `/master/employees/{id}`, `/administration/service-types/{id}`.
  - Menambahkan endpoint mutasi siklus hidup: `/master/enrollments/{id}` (PATCH) dan `/master/assignments/{id}` (PATCH) untuk mencatat pengakhiran penempatan/penugasan melalui penetapan kolom `end_date: date` tanpa menghapus record dari basis data.
  - Seluruh operasi PATCH mewajibkan wewenang Administrator (dan TU untuk penempatan siswa) dan memvalidasi keunikan serta integritas relasional.
- **Alternative:** Menggunakan PUT dengan pengiriman ulang seluruh payload (rawan menimpa data yang tidak ingin diubah) atau mengizinkan DELETE fisik (melanggar prinsip audit trail enterprise).
- **Impact:** Menutup kesenjangan wewenang antara RBAC dan OpenAPI, serta menjamin keutuhan data historis sekolah.
- **Status:** APPROVED (CCR-20261112-04).
- **Dokumen Terdampak:** `contracts/openapi.v1.yaml`, `docs/RBAC_MATRIX.md`, `contracts/README.md`.

---

### DEC-TECH-17: Mekanisme Konkurensi Absensi Kelas dan Respon HTTP 409
- **Context:** Pencatatan presensi massal harian satu rombel kelas (30-40 siswa) via endpoint `POST /attendance/bulk`.
- **Source Document:** DBD §5/§8, BSD §3.1, openapi.v1.yaml.
- **Problem:** Dua guru atau wali kelas berpotensi membuka dan mengirimkan presensi kelas yang sama pada tanggal berjalan secara serentak. Transaksi atomik `transaction.atomic()` hanya menjamin all-or-nothing, namun tidak mencegah lost update tanpa deteksi konflik eksplisit.
- **Decision:**
  - Penegakan integritas data melalui constraint unik basis data `UNIQUE(student_id, class_id, date)`.
  - Service layer Django Ninja mengeksekusi operasi simpan massal di dalam blok transaksi atomik dengan pemeriksaan konflik konkurensi. Jika terdeteksi konflik input serentak atau pelanggaran constraint unik pada tanggal terkait, backend membatalkan mutasi dan mengembalikan status HTTP 409 Conflict dengan envelope kesalahan standar (`ErrorEnvelope`).
  - Antarmuka frontend diwajibkan menyajikan dialog instruksi muat ulang data terbaru (`Reload Roster`) dan dilarang menampilkan konfirmasi sukses palsu sebelum server merespons 200 OK.
  - Setiap perubahan status kehadiran tersimpan ke tabel audit `historical_attendances` melalui `django-simple-history`.
- **Alternative:** Melakukan upsert buta (blind upsert) tanpa memberitahu pengguna jika ada data yang ditimpa oleh pengguna lain (berbahaya untuk akurasi absensi).
- **Impact:** Kontrak API mencantumkan secara resmi kode respon HTTP 409 pada `POST /attendance/bulk`, mencegah lost update dan menjamin keabsahan data presensi.
- **Status:** APPROVED (CCR-20261112-04).
- **Dokumen Terdampak:** `contracts/openapi.v1.yaml`, `contracts/database.dbml`, `docs/BSD.md`.

---

### DEC-TECH-18: Response Filtering Kerahasiaan Catatan Konseling Kesiswaan
- **Context:** Perlindungan data sensitif catatan bimbingan konseling dan tindakan kedisiplinan siswa pada modul Kesiswaan (`/student-affairs/*`).
- **Source Document:** PRD §8, BSD §4/§6, UID §2.
- **Problem:** Wali Kelas memiliki hak membaca kasus siswa di rombel binaannya, namun kode etik konseling BK mewajibkan catatan konseling privat (*counseling session notes*) hanya boleh dibaca oleh Guru BK / Kesiswaan yang menangani kasus tersebut.
- **Decision:**
  - Penegakan kerahasiaan data wajib dilakukan pada sisi server (**Server-Side Response Filtering** pada service layer/serializer Django Ninja).
  - Dilarang keras mengandalkan frontend untuk menyembunyikan properti sensitif yang sudah terlanjur dikirim melalui jaringan.
  - Saat `GET /student-affairs/cases/{id}` dipanggil oleh pengguna dengan peran Wali Kelas atau Pimpinan, array `timeline` (case events) secara otomatis difilter: catatan tindakan yang bertanda privat dimasking menjadi `[Catatan konseling privat - Terproteksi]` atau dikeluarkan dari respons.
  - Kesiswaan dan Guru BK yang ditugaskan memperoleh rincian catatan lengkap.
  - Aksi `CATAT_TINDAKAN` pada `POST /student-affairs/cases/{id}/transitions` ditetapkan sebagai mekanisme resmi pencatatan sesi konseling tanpa mengubah status siklus kasus.
- **Alternative:** Membuat endpoint privat terpisah untuk konseling (meningkatkan kompleksitas routing) atau membiarkan data terkirim penuh ke klien (pelanggaran privasi berat).
- **Impact:** Keamanan data psikologis dan privasi siswa terjamin sesuai standar etika bimbingan konseling.
- **Status:** APPROVED (CCR-20261112-04).
- **Dokumen Terdampak:** `docs/BSD.md`, `docs/RBAC_MATRIX.md`, `contracts/openapi.v1.yaml`.

---

### DEC-TECH-19: Standardisasi Parameter Kueri dan Penyaringan Sisi Server
- **Context:** Dukungan parameter kueri pencarian dan filter pada seluruh endpoint daftar data (`GET list`).
- **Source Document:** PRD §6, BSD §3, openapi.v1.yaml, DESIGN_HANDOFF.md.
- **Problem:** Baseline awal OpenAPI v1.0.0 tidak memuat parameter query filter opsional pada beberapa endpoint penting (seperti filter rombel pada siswa, filter jenis surat pada permohonan, dan pencarian username pada akun), sehingga antarmuka terpaksa melakukan filtering lokal di sisi klien yang tidak dapat menjangkau seluruh dataset server.
- **Decision:**
  - Menambahkan 10 parameter kueri opsional (`required: false`) pada OpenAPI v1.1.0:
    1. `GET /master/academic-years?is_active={bool}`
    2. `GET /master/students?class_id={int}&status={status}&search={str}`
    3. `GET /master/assignments?class_id={int}&employee_id={int}&role={role}`
    4. `GET /student-affairs/cases?status={status}&student_id={int}&search={str}`
    5. `GET /administration/requests?status={status}&service_type_id={int}&search={str}`
    6. `GET /administration/documents?search={str}&service_type_id={int}`
    7. `GET /reports/administration.pdf?start_date={date}&end_date={date}&service_type_id={int}`
    8. `GET /accounts/users?search={str}&role={str}&is_active={bool}`
    9. `GET /audit-logs?action={str}&user_id={int}&start_date={date}&end_date={date}`
  - Seluruh endpoint tetap menegakkan server-side pagination (`page`, `page_size`, `total`), batas maksimal `page_size <= 100`, pengurutan stabil (*stable deterministic ordering* berdasarkan `id` atau `created_at DESC`), dan pembatasan wewenang level objek.
- **Alternative:** Mengandalkan filter lokal pada browser klien (gagal saat data melebihi 1 halaman).
- **Impact:** Mengeliminasi seluruh filter gap yang diidentifikasi oleh Design Track tanpa merusak kompatibilitas ke belakang (*backward-compatible*).
- **Status:** APPROVED (CCR-20261112-04).
- **Dokumen Terdampak:** `contracts/openapi.v1.yaml`, `contracts/README.md`, `docs/BSD.md`.
