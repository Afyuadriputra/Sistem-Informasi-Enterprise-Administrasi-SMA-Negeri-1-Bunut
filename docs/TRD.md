# Technical Requirements Document (TRD)

**Status:** rancangan teknis awal; versi, kompatibilitas, dan keputusan operasional diverifikasi saat implementasi. Lihat PRD untuk ruang lingkup dan BSD untuk kontrak backend.

## 1. Arsitektur

Aplikasi web SPA React/TypeScript berkomunikasi melalui HTTPS dengan REST API Django Ninja dalam arsitektur Django modular monolith. ORM mengakses SQLite WAL untuk demonstrasi lokal atau PostgreSQL pada lingkungan deployment. Redis menyediakan cache bersama dan rate limiting. Penyimpanan privat menyimpan dokumen layanan. Granian menjalankan aplikasi ASGI. Admin Django digunakan untuk pengelolaan referensi oleh administrator sistem berwenang.

Alur permintaan: `Browser -> reverse proxy/HTTPS -> Granian (ASGI) -> Django middleware -> Ninja API -> services / selectors -> database / Redis / private storage`. Ini merupakan rancangan teknologi prototype; blueprint EA penelitian tetap memerlukan artefak TOGAF dan validasi stakeholder sekolah.

## 2. Stack teknologi

| Lapisan | Pilihan | Catatan kompatibilitas |
|---|---|---|
| Backend | Django, Django Ninja, Pydantic, Granian, orjson renderer, psycopg, dj-database-url, python-decouple | Python runtime modern; Granian menangani ASGI dengan performa tinggi |
| Keamanan & audit | django-ninja-jwt, Argon2 password hasher, django-cors-headers, django-simple-history, structlog | Token access berumur pendek dengan rotasi refresh token; audit model berbasis transaksi |
| Data & dokumen | SQLite WAL (demo lokal); PostgreSQL (target deployment); Redis (cache & rate limit); openpyxl; ReportLab / WeasyPrint | Pada Windows, gunakan `python-magic-bin` atau inspeksi header bytes murni jika `libmagic` C DLL tidak tersedia; gunakan `ReportLab` jika dependensi GTK/Cairo untuk `WeasyPrint` belum terpasang |
| Frontend | React, TypeScript, Vite, Tailwind CSS, shadcn/ui, Radix Primitives, Lucide Icons, clsx, tailwind-merge | SPA tipe ketat, komponen aksesibel tanpa dependensi berlebih |
| Data frontend | Axios, TanStack Query, Zustand, React Router, React Hook Form, Zod, TanStack Table, Recharts, Sonner | TanStack Query untuk server state; Zustand untuk client/UI state; Zod untuk validasi skema form |
| Tooling & tes | pytest, pytest-django, Ruff, openapi-typescript, ESLint, Prettier, Vitest, Testing Library | Kontrak tipe frontend digenerate langsung dari skema OpenAPI backend |

Dependensi dikunci melalui lockfile (`requirements.txt` / `poetry.lock` / `package-lock.json`). Versi Python, Node, Redis, dan OS didokumentasikan dalam panduan instalasi.

## 3. Struktur dan batas modul

Backend:
```text
backend/
  config/              # settings, asgi, urls, api router utama
  apps/
    core/              # middleware, exception handler, envelope response, utilitas
    accounts/          # custom user, roles/groups, JWT auth, sesi
    master_data/       # tahun ajaran, kelas, pegawai, siswa, penempatan (enrollment), penugasan
    attendance/        # pencatatan absensi batch, rekap kelas/siswa, histori absensi
    student_affairs/   # kasus kesiswaan, transisi status, tindakan (case events)
    administration/    # permohonan layanan TU, alur persetujuan, dokumen privat
    reports/           # ringkasan dashboard teragregasi, ekspor Excel dan PDF
```

Pola modul bisnis:
- `api.py`: Endpoint HTTP, skema routing, dan delegasi otorisasi.
- `schemas.py`: Kontrak data input/output menggunakan Pydantic.
- `services.py`: Logika bisnis, use case, mutasi database, transaksi atomik, audit trail, dan invalidasi cache pasca commit.
- `selectors.py`: Akses baca, filtering terotorisasi (*scoping*), dan agregasi metrik.
- `models.py`: Definisi persistensi tabel, constraint database, dan histori.

Frontend:
```text
frontend/src/
  app/                 # bootstrap, router, providers, error boundaries
  components/
    atoms/             # button, input, label, badge, icon
    molecules/         # form-field, search-field, filter-chip, pagination
    organisms/         # data-table, attendance-editor, timeline, dialog konfirmasi
    templates/         # auth-layout, dashboard-layout, page-layout
  pages/               # komponen per route (S01 s/d S18)
  features/            # slice domain (api hooks, state lokal, schema Zod per fitur)
  lib/                 # HTTP client (Axios interceptor), helper format tanggal/angka
  stores/              # Zustand stores (UI state, konteks filter aktif)
  types/               # tipe TypeScript hasil generasi openapi-typescript
```

## 4. Antarmuka dan integrasi data

- Seluruh endpoint berada di bawah `/api/`. Dokumentasi OpenAPI Ninja tersedia otomatis pada environment lokal. Skema OpenAPI menjadi sumber kebenaran (*single source of truth*) untuk menghasilkan tipe TypeScript di frontend.
- Amplop respons error konsisten:
  ```json
  {
    "code": "VALIDATION_ERROR",
    "message": "Periksa kembali data yang dimasukkan.",
    "details": [{"field": "date", "message": "Tanggal di luar tahun ajaran aktif"}],
    "request_id": "req-abcdef123456"
  }
  ```
- Otorisasi server bersifat mutlak: memvalidasi status akun, peran pengguna, dan cakupan objek (*object-level permissions*). Pengecekan di frontend hanya untuk panduan antarmuka (*UI affordance*), bukan batas keamanan.
- Claim peran dalam payload JWT tidak boleh menjadi satu-satunya acuan hak akses: server memvalidasi status akun aktif dan penugasan riil di database atau cache Redis untuk setiap transaksi sensitif.

## 5. Keamanan dan operasi sistem

- **Autentikasi:** JWT access token (masa berlaku singkat 15-30 menit) dan refresh token (1-7 hari) dengan mekanisme rotasi serta blacklist saat logout.
- **Penyimpanan dokumen:** Berkas lampiran permohonan disimpan pada direktori privat di luar root publik (`PRIVATE_MEDIA_ROOT`). Nama berkas di-hash/acak (UUID) untuk mencegah tabrakan nama dan *path traversal*.
- **Unduh berkas:** Dilayani melalui endpoint terotorisasi menggunakan Django `FileResponse` yang memeriksa kepemilikan dan kewenangan peran pemohon.
- **Validasi unggahan:** Memvalidasi ekstensi berkas (allowlist `.pdf`, `.jpg`, `.jpeg`, `.png`), ukuran maksimum berkas (misalnya 5 MB), serta verifikasi magic bytes.
- **Perlindungan brute-force:** Rate limiting pada `/api/auth/login` berbasis alamat IP dan username via Redis operasi atomik dengan respons HTTP 429 jika melebihi ambang batas.
- **Observability:** Format log terstruktur (JSON) dengan request ID unik, path, metode, status HTTP, durasi eksekusi, dan identitas pengguna minimal. Kata sandi, token, dan data pribadi sensitif (seperti NIK lengkap) disanitasi agar tidak masuk ke berkas log.

## 6. Konsistensi, database dan cache

- **SQLite WAL vs PostgreSQL:** SQLite dengan mode WAL (*Write-Ahead Logging*) digunakan untuk demonstrasi lokal dan pengujian cepat. SQLite memiliki keterbatasan satu writer konkuren; kondisi ini ditangani dengan timeout yang memadai. PostgreSQL adalah target lingkungan staging/deployment dengan kontrol transaksi `SELECT FOR UPDATE` dan isolasi transaksi yang teruji.
- **Bulk history:** `django-simple-history` pada pemanggilan `bulk_create` / `bulk_update` bawaan dapat melewati sinyal `post_save`. Operasi massal (seperti simpan absensi kelas) wajib menggunakan helper `bulk_create_with_history` atau pencatatan riwayat eksplisit dalam transaksi yang sama.
- **Strategi cache:** Cache disimpan di Redis berdasarkan cakupan peran dan parameter filter. Invalidasi cache dijalankan setelah transaksi berhasil di-commit (`transaction.on_commit`). Jika Redis mengalami kendala, aplikasi tetap berjalan normal dengan melakukan pembacaan langsung dari database (*graceful fallback*).

## 7. Kualitas dan pengujian terotomasi

- **Pengujian backend (pytest):**
  - Unit test: Aturan transisi status kasus dan permohonan, validasi tanggal penempatan, rumus rekapitulasi.
  - API integration test: Endpoint login, otorisasi peran, penolakan akses lintas kelas (IDOR), penyimpanan absensi batch atomik, dan upload dokumen privat.
- **Pengujian frontend (Vitest & Testing Library):**
  - Form absensi: Validasi per baris, pencegahan double-submit, penanganan error batch.
  - Navigasi & state: Tampilan filter, penanganan status loading/empty/error.
- **End-to-End Test:** Memverifikasi Skenario A (Kehadiran hingga Kasus) dan Skenario B (Layanan TU hingga Arsip) berjalan tanpa hambatan dari peramban hingga basis data.

## 8. Kontrak state frontend

- TanStack Query memegang server state dengan struktur query key: `[domain, entity, id/scope, filters]`.
- Setelah mutasi berhasil, invalidasi query cache terkait dipicu agar data antarmuka selalu segar.
- Pembersihan total query cache dilakukan saat pengguna logout untuk mencegah kebocoran data pengguna sebelumnya pada perangkat bersama.
- Zustand hanya digunakan untuk menyimpan state aplikasi lokal (sidebar terbuka/tutup, filter aktif sementara, preferensi visual).
- Tabel data menerapkan paginasi di sisi server untuk menjaga performa rendering pada dataset besar.

## 9. Konfigurasi lingkungan (*environment variables*)

| Variabel | Deskripsi | Standar keamanan |
|---|---|---|
| `DJANGO_SECRET_KEY` | Kunci kriptografi Django | Wajib diisi string acak panjang, rahasia |
| `DJANGO_DEBUG` | Mode debug | `True` di lokal dev, wajib `False` di deployment |
| `DJANGO_ALLOWED_HOSTS` | Daftar host yang diizinkan | Host/domain spesifik, bukan wildcard `*` |
| `DATABASE_URL` | String koneksi database | Format standar `sqlite:///...` atau `postgres://...` |
| `REDIS_URL` | Alamat instans Redis | `redis://127.0.0.1:6379/1` |
| `CORS_ALLOWED_ORIGINS` | Origin frontend yang diizinkan | URL frontend spesifik (misal `http://localhost:5173`) |
| `PRIVATE_MEDIA_ROOT` | Lokasi berkas arsip privat | Direktori di luar direktori web server publik |
| `VITE_API_BASE_URL` | URL basis API backend | `http://localhost:8000/api` |

## 10. Strategi error dan observability

- Kode status HTTP konsisten:
  - `400 Bad Request` / `422 Unprocessable Entity`: Validasi input data tidak sesuai skema.
  - `401 Unauthorized`: Kredensial tidak valid atau token kedaluwarsa.
  - `403 Forbidden`: Pengguna tidak memiliki hak akses terhadap peran atau objek terkait.
  - `404 Not Found`: Objek tidak ditemukan (atau disembunyikan untuk menjaga privasi IDOR).
  - `409 Conflict`: Benturan konkurensi (misalnya versi data berubah atau data ganda).
  - `429 Too Many Requests`: Pembatasan laju pemanggilan API terlampaui.
  - `500 Internal Server Error`: Kesalahan server dengan pesan aman bagi pengguna dan pencatatan request ID di sisi server.
- Ambang batas investigasi: Pemanggilan API dengan durasi >500 ms dicatat sebagai peringatan untuk optimasi query (deteksi n+1).

## 11. Kriteria kesiapan teknis prototype

- Pemeriksaan tipe TypeScript dan build frontend Vite berhasil tanpa error.
- Pemeriksaan Django (`python manage.py check`) dan migrasi basis data bersih.
- Test suite pengujian backend dan frontend lulus.
- Data sintetis awal dapat dimuat melalui seed script untuk demonstrasi alur.
- Logika transaksi atomik, histori massal, dan proteksi berkas privat terverifikasi berjalan sesuai spesifikasi.
