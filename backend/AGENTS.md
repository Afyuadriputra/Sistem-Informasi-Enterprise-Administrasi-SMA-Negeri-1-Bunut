# Backend Agent Guidelines & Technical Instructions

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Peran Agent | Backend Agent |
| Cakupan Writable | `backend/**`, `coordination/BACKEND_STATUS.md` |
| Cakupan Read-Only | `frontend/**`, `design/**`, `contracts/**`, `docs/**` |
| Acuan Utama | TRD.md, BSD.md, DBD.md, contracts/openapi.v1.yaml, contracts/database.dbml |

---

## 1. Tanggung Jawab Utama Backend Agent

1. Mengimplementasikan Django 5.x Modular Monolith menggunakan Django Ninja dan Granian ASGI.
2. Mengelola skema persistensi basis data, relasi foreign key, constraint unik, dan file migrasi ORM.
3. Mengimplementasikan use case bisnis terisolasi pada service layer dengan transaksi atomik.
4. Menerapkan autentikasi JWT (`django-ninja-jwt`), rotasi refresh token, blacklist logout, dan rate limiting login via Redis.
5. Menjamin seluruh endpoint menerapkan otorisasi tingkat objek (*object-level permissions*) dan mencegah celah IDOR.
6. Menerapkan kontrol konkurensi optimistik (`version: integer`) pada entitas kasus kesiswaan dan permohonan surat.
7. Membangun generator ekspor berkas Excel (`openpyxl`) dan PDF (`ReportLab`).
8. Menulis unit test, API integration test, dan security test menggunakan `pytest` dan `pytest-django`.

---

## 2. Struktur Modul & Batas Tanggung Jawab File

Setiap modul di bawah `backend/apps/<modul>/` wajib mematuhi pemisahan tanggung jawab berikut:
- **`api.py`:** Definisi router Django Ninja. Menangani parsing parameter HTTP, otentikasi JWT, pemeriksaan izin peran, dan memanggil service/selector. Dilarang menulis kueri ORM kompleks langsung di sini.
- **`schemas.py`:** Skema Pydantic untuk validasi payload input dan serialisasi response output. Wajib mencocokkan tipe data dan field dengan `contracts/openapi.v1.yaml`.
- **`services.py`:** Logika bisnis mutasi data (*write operations*). Bertanggung jawab atas `transaction.atomic()`, validasi domain, penulisan snapshot audit `HistoricalRecords`, dan invalidasi cache pasca commit via `transaction.on_commit()`.
- **`selectors.py`:** Logika pembacaan data (*read operations*). Mengembalikan queryset terfilter berdasarkan cakupan izin pengguna (*scoped querysets*), menangani paginasi, pencarian, dan kueri agregasi.
- **`models.py`:** Definisi model Django ORM, constraint basis data, indeks komposit, dan audit trail `HistoricalRecords()`.

---

## 3. Aturan Teknis Mutlak (Non-Negotiable)

1. **Kepatuhan Kontrak API:**
   - Nama field JSON, enum status, kode status HTTP, dan amplop respons error wajib identik 100% dengan `contracts/openapi.v1.yaml`.
   - Amplop error wajib menyertakan `code`, `message`, `details` (jika ada), dan `request_id`.
2. **Bulk History pada Operasi Absensi Massal:**
   - Pemanggilan `bulk_create` atau `bulk_update` bawaan Django ORM melewati sinyal `post_save`.
   - Pada `apps/attendance/services.py`, operasi penyimpanan absensi kelas harian **wajib** menggunakan `simple_history.utils.bulk_create_with_history` di dalam blok `transaction.atomic()` yang sama.
3. **Penyimpanan Berkas Privat:**
   - Berkas lampiran permohonan persuratan wajib disimpan di folder `PRIVATE_MEDIA_ROOT` di luar direktori publik.
   - Nama fisik berkas di-hash menjadi UUID acak tanpa ekstensi terbuka di filesystem.
   - Pengunduhan dilayani oleh Django `FileResponse` melalui endpoint `GET /api/administration/documents/{id}/download` yang memeriksa otorisasi pengguna.
4. **Sanitasi Log Audit:**
   - Dilarang keras mencatat kata sandi, token otorisasi, atau NIK lengkap siswa pada berkas log sistem.
5. **Kompabilitas Windows Lokal:**
   - Gunakan `python-magic-bin` atau inspeksi byte header murni jika binary C `libmagic` tidak tersedia di Windows.
   - Gunakan `ReportLab` sebagai generator PDF default untuk menghindari dependensi GTK/Cairo di Windows.

---

## 4. Standar Pengujian Terotomasi (Pytest)

Sebelum menandai suatu milestone backend selesai:
1. Jalankan pemeriksaan sistem Django: `python manage.py check`.
2. Jalankan pemeriksaan linter: `ruff check .`.
3. Jalankan pengujian terotomasi: `pytest`.
4. Seluruh kasus uji kritis (termasuk skenario BE-01 hingga BE-10 pada BSD.md) wajib lulus 100%.

---

## 5. Protokol Pelaporan Status

Setelah menyelesaikan pekerjaan atau sebelum sesi berakhir:
- Perbarui progress pada berkas `coordination/BACKEND_STATUS.md`.
- Cantumkan: Milestone yang dikerjakan, langkah terakhir yang tuntas, bukti pengujian (pytest output), dan langkah berikutnya.
- **Dilarang memodifikasi file di luar `backend/**` dan `coordination/BACKEND_STATUS.md`.**
