# Backend Specification Document (BSD)

**Status:** spesifikasi teknis backend; path, payload, status bisnis, dan aturan otorisasi menjadi acuan implementasi Django Ninja. Skema OpenAPI menjadi sumber kebenaran kontrak antarmuka.

## 1. Struktur dan tanggung jawab kode

Arsitektur kode berbasis Django Modular Monolith:
- `config/{settings,asgi,urls,api}.py`: Konfigurasi global, inisialisasi Ninja API, dan routing root.
- `apps/{core,accounts,master_data,attendance,student_affairs,administration,reports}`:
  - `api.py`: Router endpoint HTTP, autentikasi JWT, validasi otorisasi peran, dan penanganan HTTP response.
  - `schemas.py`: Kontrak data request/response berbasis Pydantic (tipe data, enum, panjang karakter, batasan nilai).
  - `services.py`: Logika bisnis use-case, validasi domain, eksekusi transaksi atomik, penulisan event riwayat, dan pemicu invalidasi cache pasca commit.
  - `selectors.py`: Akses pembacaan basis data terotorisasi (*scoped querysets*), filter, paginasi, dan kueri agregasi laporan.
  - `models.py`: Definisi persistensi ORM, constraint integritas basis data, dan konfigurasi `HistoricalRecords`.

## 2. Kontrak endpoint API

Semua endpoint berada di bawah prefix `/api/`. Respon daftar (*list*) selalu mendukung parameter paginasi (`page`, `page_size`), pencarian (`search`), dan filter relevan.

| Method dan path | Deskripsi | Peran / Hak akses minimal |
|---|---|---|
| POST `/auth/login` | Autentikasi kredensial dan penerbitan pasangan token JWT | Publik (dibatasi rate limiting) |
| POST `/auth/refresh` | Memperbarui access token menggunakan refresh token | Pemegang refresh token sah |
| POST `/auth/logout` | Mencabut refresh token (blacklist) dan mengakhiri sesi | Pengguna terautentikasi |
| GET `/auth/me` | Informasi profil pengguna, daftar peran aktif, dan penugasan | Pengguna terautentikasi |
| GET, POST `/master/academic-years` | Daftar dan tambah tahun ajaran | Admin sistem |
| GET, PATCH `/master/academic-years/{id}` | Detail dan ubah tahun ajaran | Admin sistem |
| GET, POST `/master/classes` | Daftar dan tambah kelas | Admin sistem / Staf terotorisasi |
| GET, PATCH `/master/classes/{id}` | Detail dan ubah data kelas | Admin sistem / Staf terotorisasi |
| GET, POST `/master/employees` | Daftar dan tambah pegawai/guru | Admin sistem |
| GET, PATCH `/master/employees/{id}` | Detail dan ubah pegawai/guru | Admin sistem |
| GET, POST `/master/students` | Daftar dan tambah data siswa | Admin sistem / TU terotorisasi |
| GET, PATCH `/master/students/{id}` | Detail dan ubah data siswa | Admin sistem / TU terotorisasi |
| GET, POST `/master/enrollments` | Daftar dan buat penempatan siswa di kelas | Admin sistem / TU terotorisasi |
| DELETE, PATCH `/master/enrollments/{id}` | Batalkan atau sesuaikan penempatan kelas | Admin sistem / TU terotorisasi |
| GET, POST `/master/assignments` | Daftar dan buat penugasan guru/wali kelas | Admin sistem |
| DELETE, PATCH `/master/assignments/{id}` | Batalkan atau sesuaikan penugasan guru | Admin sistem |
| GET `/attendance` | Rekapitulasi absensi terfilter periode/kelas | Guru / Wali Kelas / Kesiswaan / Pimpinan |
| POST `/attendance/bulk` | Simpan catatan absensi satu kelas harian secara atomik | Guru mata pelajaran / Wali kelas terkait |
| GET, POST `/student-affairs/cases` | Antrean daftar kasus dan pembuatan kasus baru | Kesiswaan / Wali kelas terkait |
| GET `/student-affairs/cases/{id}` | Detail kronologis kasus dan tindakan | Kesiswaan / Wali kelas terkait |
| POST `/student-affairs/cases/{id}/transitions` | Perbarui status kasus dan rekam tindakan | Kesiswaan berwenang |
| GET `/administration/service-types` | Daftar jenis layanan administrasi yang aktif | Tata Usaha / Seluruh staf aktif |
| GET, POST `/administration/requests` | Daftar antrean dan pembuatan permohonan persuratan | Tata Usaha berwenang |
| GET `/administration/requests/{id}` | Detail data dan riwayat permohonan | Tata Usaha / Pejabat pemberi persetujuan |
| POST `/administration/requests/{id}/transitions` | Perbarui status alur permohonan | Pihak berwenang sesuai tahapan transisi |
| POST `/administration/requests/{id}/documents` | Unggah lampiran berkas permohonan | Tata Usaha / Pembuat permohonan |
| GET `/administration/documents/{id}/download` | Unduh berkas privat dengan proteksi hak akses | Pihak yang memiliki akses ke permohonan |
| GET `/reports/dashboard` | Metrik ringkasan teragregasi sesuai cakupan peran | Seluruh peran (data difilter otomatis) |
| GET `/reports/attendance.xlsx` | Ekspor rekapitulasi kehadiran ke berkas Excel | Guru / Wali / Kesiswaan / Pimpinan |
| GET `/reports/administration.pdf` | Ekspor rekapitulasi layanan ke berkas PDF | Tata Usaha / Pimpinan |
| GET `/audit-logs` | Penelusuran log aktivitas sistem terfilter | Administrator sistem |

## 3. Kontrak logika bisnis use-case penting

### 3.1. Penyimpanan kehadiran kelas massal (POST `/attendance/bulk`)
- **Validasi:**
  - Verifikasi pengguna terautentikasi memiliki penugasan aktif (`ClassAssignment`) pada kelas dan tanggal yang diminta.
  - Tanggal absensi tidak boleh melebihi tanggal berjalan.
  - Verifikasi seluruh `student_id` terdaftar secara aktif (`Enrollment`) pada kelas dan tanggal terkait.
  - Tolak permintaan jika terdapat duplikasi `student_id` dalam satu payload.
- **Eksekusi:**
  - Operasi dijalankan dalam `transaction.atomic()`.
  - Menggunakan `bulk_create_with_history` atau `bulk_update_with_history` untuk menjamin pencatatan snapshot riwayat pada setiap baris absensi.
  - Atribut aktor audit diisi dari `request.auth.id`.
- **Pasca transaksi:**
  - Picu invalidasi cache rekapitulasi kelas terkait melalui `transaction.on_commit()`.
  - Kembalikan ringkasan data yang tersimpan.

### 3.2. Transisi status dan tindakan kasus kesiswaan
- **Kontrol konkurensi (Optimistic Locking):**
  - Payload wajib menyertakan `expected_version`.
  - Jika versi saat ini di basis data berbeda dengan `expected_version`, kembalikan HTTP 409 Conflict.
- **Validasi state machine:**
  - Transisi status hanya diizinkan sesuai tabel alur yang sah (`BARU -> DIPROSES -> SELESAI / DIBATALKAN`).
- **Eksekusi atomik:**
  - Simpan perubahan status model `StudentCase` dengan menaikkan `version = version + 1`.
  - Buat satu baris baru pada `CaseEvent` yang merekam status awal, status akhir, aksi, catatan tindakan, dan ID aktor.

### 3.3. Alur permohonan persuratan tata usaha dan berkas privat
- **Transisi status:**
  - Mengikuti tahapan sah (`DIAJUKAN -> DIPROSES -> MENUNGGU_PERSETUJUAN -> DISETUJUI / DITOLAK -> SELESAI`).
  - Setiap transisi mencatat `ServiceEvent` secara atomik dan memeriksa `expected_version`.
- **Keamanan berkas privat:**
  - Validasi ekstensi berkas (`.pdf`, `.jpg`, `.jpeg`, `.png`) dan ukuran berkas (maksimal 5 MB).
  - Verifikasi integritas format melalui inspeksi magic bytes.
  - Berkas fisik disimpan dengan nama acak (UUID v4) di luar direktori publik.
  - Pengunduhan dilayani oleh Django `FileResponse` yang memvalidasi bahwa pengguna memiliki hak akses terhadap permohonan induk.

## 4. Autentikasi, otorisasi dan kontrol akses

- **Manajemen token JWT:**
  - Access token berumur pendek (15 menit) berisi `user_id` dan daftar peran dasar.
  - Refresh token berumur 7 hari; rotasi refresh token diterapkan saat pembaruan sesi.
  - Logout memasukkan refresh token ke daftar hitam (*blacklist*) di Redis/database.
- **Prinsip otorisasi (RBAC & Object-Level Permission):**
  - Server selalu memverifikasi hak akses per objek (*object scoping*). Contoh: Guru hanya boleh membaca dan menyimpan absensi untuk kelas tugasnya; Wali Kelas hanya dapat melihat rekap kelas yang diampunya; Pimpinan hanya melihat agregat tanpa membuka rincian identitas kasus sensitif.
  - Multi-peran: Pengguna yang memiliki beberapa peran (misal Guru dan Wali Kelas) dievaluasi berdasarkan gabungan izin yang sah. Pilihan peran di antarmuka pengguna hanya sebagai filter konteks tampilan, bukan pemotong verifikasi server.
- **Rate Limiting:**
  - Endpoint `/auth/login` dibatasi maksimal 5 percobaan gagal per IP dan per username dalam jendela 15 menit menggunakan counter atomik Redis.
  - Melebihi batas mengembalikan HTTP 429 Too Many Requests dengan header `Retry-After`.

## 5. Standar logging dan caching

- **Format log terstruktur:**
  - Seluruh log API dicatat dalam format JSON dengan atribut: `timestamp`, `level`, `request_id`, `method`, `path`, `status_code`, `duration_ms`, dan `user_id`.
  - Kata sandi, token otorisasi, dan informasi identitas pribadi sensitif disanitasi sebelum log ditulis.
- **Strategi caching:**
  - Kueri ringkasan dashboard dan rekapitulasi kehadiran disimpan di Redis dengan key berbasis peran dan filter (misal: `dash:admin:2026-11`).
  - Waktu simpan (TTL) default adalah 5 hingga 15 menit.
  - Setiap mutasi data memicu pembersihan key cache terkait via `transaction.on_commit()`.

## 6. Contoh kontrak payload request dan response

### POST `/attendance/bulk`
Request:
```json
{
  "class_id": 12,
  "date": "2026-11-12",
  "items": [
    {"student_id": 101, "status": "HADIR", "note": ""},
    {"student_id": 102, "status": "IZIN", "note": "Izin keluarga"}
  ]
}
```
Response sukses (HTTP 200):
```json
{
  "class_id": 12,
  "date": "2026-11-12",
  "saved_count": 2,
  "message": "Kehadiran berhasil disimpan."
}
```
Response error validasi (HTTP 422):
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Data siswa tidak sesuai penempatan kelas aktif.",
  "details": [{"student_id": 102, "message": "Siswa tidak terdaftar di kelas 12 pada tanggal 2026-11-12"}],
  "request_id": "req-9876543210ab"
}
```

### POST `/student-affairs/cases/{id}/transitions`
Request:
```json
{
  "action": "MULAI_PENANGANAN",
  "note": "Menghubungi wali kelas dan menjadwalkan konseling",
  "expected_version": 1
}
```
Response sukses (HTTP 200):
```json
{
  "id": 5,
  "status": "DIPROSES",
  "version": 2,
  "updated_at": "2026-11-12T10:30:00Z"
}
```
Response konflik versi (HTTP 409):
```json
{
  "code": "CONCURRENCY_CONFLICT",
  "message": "Data kasus telah diubah oleh pengguna lain. Silakan muat ulang halaman.",
  "details": [{"current_version": 2, "provided_version": 1}],
  "request_id": "req-112233445566"
}
```

## 7. Rincian pengujian backend terotomasi

| ID | Skenario uji | Hasil yang diverifikasi |
|---|---|---|
| BE-01 | Percobaan login salah melebihi batas 5 kali berturut-turut | Mengembalikan HTTP 429 dan mencatat log percobaan tanpa mengungkap keberadaan username |
| BE-02 | Penggunaan token pengguna yang status akunnya telah dinonaktifkan | Mengembalikan HTTP 401 / 403 saat memanggil endpoint terproteksi |
| BE-03 | Guru A mencoba mencatat kehadiran pada kelas yang bukan tugasnya | Mengembalikan HTTP 403 Forbidden dan tidak ada baris yang tersimpan |
| BE-04 | Batch kehadiran menyertakan siswa yang tidak terdaftar di kelas | Transaksi dibatalkan secara penuh (0 baris tersimpan), mengembalikan HTTP 422 |
| BE-05 | Penyimpanan batch kehadiran yang sah | Seluruh baris tersimpan, snapshot riwayat terbuat via bulk history, cache terkait terhapus |
| BE-06 | Dua petugas memperbarui status permohonan yang sama secara bersamaan | Petugas pertama berhasil (HTTP 200); petugas kedua menerima HTTP 409 Conflict |
| BE-07 | Unggah berkas dokumen dengan ekstensi `.exe` atau MIME type tidak diizinkan | Berkas ditolak (HTTP 422) dan tidak tersimpan di sistem berkas privat |
| BE-08 | Pengguna tanpa wewenang mencoba mengunduh dokumen privat | Mengembalikan HTTP 403 / 404 tanpa menyajikan isi berkas |
| BE-09 | Pembacaan dashboard laporan setelah transaksi kehadiran baru | Angka rekapitulasi diperbarui secara akurat dan konsisten dengan data basis data |
| BE-10 | Permintaan ekspor data dengan filter rentang tanggal tertentu | Dokumen hasil ekspor hanya memuat data dalam cakupan izin pengguna pemohon |
