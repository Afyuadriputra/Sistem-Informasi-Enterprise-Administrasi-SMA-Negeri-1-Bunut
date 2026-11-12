# Application Flow Document (AFD)

**Status:** alur usulan untuk evaluasi prototype; nama peran, SOP, transisi status, dan ketentuan sekolah diselaraskan dengan kebutuhan pengujian. Simbol `->` menunjukkan urutan langkah antarmuka.

## 1. Alur navigasi dan manajemen sesi

`Login -> validasi kredensial & rate limit -> sesi aktif -> verifikasi peran & penugasan -> dashboard sesuai akses -> modul fitur terotorisasi -> logout`.

- Kredensial tidak valid menghasilkan pesan kegagalan generik.
- Percobaan melebihi ambang batas menghasilkan respons HTTP 429 dengan waktu tunggu.
- Akun nonaktif atau pengguna dengan izin yang dicabut ditolak oleh server pada permintaan API berikutnya.
- Kedaluwarsa token mengarahkan pengguna kembali ke halaman login tanpa menghapus pesan informatif terkait.

## 2. Persiapan data master

1. Administrator membuat tahun ajaran, kelas, pegawai, akun pengguna, dan data siswa.
2. Petugas menempatkan siswa pada kelas tertentu (`Enrollment`) dan menetapkan penugasan guru/wali kelas (`ClassAssignment`).
3. Sistem memvalidasi data untuk mencegah tumpang tindih penempatan kelas atau nomor identitas ganda.
4. Modul absensi dan kesiswaan merujuk pada data penempatan yang aktif pada tanggal transaksi.

## 3. Skenario demonstrasi A: Kehadiran hingga tindak lanjut kesiswaan

1. **Pencatatan guru:**
   - Guru memilih tahun ajaran, kelas tugas, dan tanggal transaksi.
   - Sistem memuat daftar siswa yang terdaftar aktif pada kelas dan tanggal tersebut beserta status yang tersimpan sebelumnya (jika ada).
   - Guru mengisi status kehadiran (Hadir, Sakit, Izin, Alpa) dan catatan per siswa.
   - Guru menekan tombol "Simpan Kehadiran". Sistem memvalidasi seluruh baris dan mengeksekusi penyimpanan batch atomik di basis data.
2. **Pemantauan wali kelas:**
   - Wali kelas membuka rekapitulasi kehadiran kelasnya untuk rentang periode tertentu.
   - Sistem menampilkan rekap persentase dan daftar siswa dengan ketidakhadiran berulang.
   - Wali kelas hanya dapat mengakses kelas binaannya dan tidak dapat mengakses kelas lain.
3. **Penanganan kesiswaan:**
   - Berdasarkan kriteria sekolah atau hasil pantauan, petugas kesiswaan membuat kasus baru (`StudentCase`) untuk siswa terkait.
   - Petugas kesiswaan mencatat tindakan dan memperbarui status kasus melalui transisi yang sah: `BARU -> DIPROSES -> SELESAI` (atau `DIBATALKAN`).
   - Setiap tindakan tersimpan dalam riwayat kronologis (`CaseEvent`) bersama identitas aktor dan catatan penanganan.
4. **Tinjauan pimpinan:**
   - Pimpinan (Kepala Sekolah) membuka dashboard laporan untuk meninjau agregat kehadiran per tingkat/jurusan dan statistik penanganan kasus.
   - Pimpinan melihat metrik ringkasan tanpa membuka rincian identitas kasus sensitif secara sembarangan.

**Penanganan kondisi perkecualian:**
- Siswa di luar kelas atau tanggal tugas otomatis ditolak oleh validasi server.
- Percobaan input ganda ditolak melalui batasan integritas basis data.
- Upaya guru mengakses kelas di luar penugasannya menghasilkan HTTP 403 Forbidden.
- Jika terjadi benturan pembaruan kasus bersamaan, server mengembalikan HTTP 409 Conflict dan meminta antarmuka memuat versi terbaru.

## 4. Skenario demonstrasi B: Layanan persuratan tata usaha dan arsip

1. **Pengajuan permohonan:**
   - Petugas Tata Usaha (TU) membuka modul permohonan layanan dan memilih jenis permohonan (misal Surat Keterangan Siswa Aktif atau Legalisir).
   - Petugas mengisi data pemohon, rincian keperluan, dan mengunggah berkas pendukung bila disyaratkan.
   - Sistem memvalidasi format dan ukuran berkas, lalu menyimpannya di direktori privat dengan kode unik. Status awal diset ke `DIAJUKAN`.
2. **Pemrosesan dan verifikasi:**
   - Staf TU memeriksa kelengkapan data dan mengubah status menjadi `DIPROSES`.
   - Jika layanan membutuhkan tanda tangan/persetujuan pimpinan, status dialihkan menjadi `MENUNGGU_PERSETUJUAN`.
3. **Persetujuan dan penyelesaian:**
   - Pimpinan/pejabat berwenang meninjau permohonan dan memilih `DISETUJUI` atau `DITOLAK` disertai alasan tertulis.
   - Setelah disetujui, TU menyelesaikan dokumen dan memperbarui status menjadi `SELESAI`.
4. **Pengarsipan dan unduh berkas:**
   - Dokumen permohonan tersimpan dalam arsip privat.
   - Hanya pihak yang terotorisasi yang dapat mengunduh berkas fisik melalui endpoint pengunduhan aman.

**Penanganan kondisi perkecualian:**
- Jenis layanan nonaktif ditolak dari pembuatan permohonan baru.
- Berkas melebihi batas ukuran atau berekstensi terlarang ditolak saat validasi unggah.
- Transisi status di luar urutan yang diizinkan ditolak oleh validasi state machine backend.

## 5. Pelaporan dan ekspor data

1. Pengguna memilih jenis laporan, rentang periode tanggal, dan filter yang diizinkan.
2. Sistem menghitung agregasi data sumber secara langsung atau dari cache yang valid.
3. Pengguna dapat meninjau ringkasan di layar atau mengunduh ekspor Excel/PDF.
4. Setiap pengunduhan ekspor dicatat pada log audit sistem. Data ekspor menerapkan filter dan batasan otorisasi yang sama dengan tampilan antarmuka.

## 6. Keputusan transisi status

| Modul | Status asal | Aksi transisi | Peran berwenang | Status tujuan | Prasyarat aksi |
|---|---|---|---|---|---|
| Kasus Kesiswaan | BARU | Mulai Penanganan | Kesiswaan / Wali Kelas | DIPROSES | Petugas penanggung jawab telah ditentukan |
| Kasus Kesiswaan | DIPROSES | Selesaikan Kasus | Kesiswaan berwenang | SELESAI | Catatan hasil penanganan wajib diisi |
| Kasus Kesiswaan | BARU / DIPROSES | Batalkan Kasus | Kesiswaan berwenang | DIBATALKAN | Alasan pembatalan wajib diisi |
| Layanan TU | DIAJUKAN | Mulai Verifikasi | Staf Tata Usaha | DIPROSES | Data pemohon lengkap |
| Layanan TU | DIPROSES | Ajukan Persetujuan | Staf Tata Usaha | MENUNGGU_PERSETUJUAN | Draf surat siap ditinjau pimpinan |
| Layanan TU | MENUNGGU_PERSETUJUAN | Berikan Persetujuan | Pimpinan / Kepala Sekolah | DISETUJUI | Verifikasi administrasi terpenuhi |
| Layanan TU | MENUNGGU_PERSETUJUAN | Tolak Permohonan | Pimpinan / Kepala Sekolah | DITOLAK | Alasan penolakan wajib dicatat |
| Layanan TU | DISETUJUI | Selesaikan & Terbitkan | Staf Tata Usaha | SELESAI | Surat selesai dicetak atau diserahkan |

## 7. Alur antarmuka per halaman

- **Dashboard:** Pilih periode -> Tampilkan ringkasan metrik sesuai cakupan peran -> Klik metrik untuk membuka daftar terfilter yang berizin.
- **Master Siswa & Pegawai:** Cari/filter berdasarkan identitas -> Buka form tambah/ubah -> Validasi input -> Simpan data -> Daftar diperbarui otomatis.
- **Pencatatan Kehadiran:** Pilih kelas dan tanggal -> Muat daftar siswa aktif -> Isi status per siswa -> Validasi form -> Simpan satu batch -> Tampilkan status keberhasilan atau rincian baris yang bermasalah.
- **Rekap Kehadiran:** Tentukan filter kelas dan rentang tanggal -> Tampilkan tabel rekap dan persentase kehadiran -> Opsi ekspor berkas Excel.
- **Kasus Kesiswaan:** Buka daftar antrean kasus -> Buka rincian kasus -> Lakukan transisi status disertai catatan tindakan -> Riwayat kronologis (*timeline*) bertambah.
- **Layanan TU:** Tampilkan antrean permohonan -> Buat permohonan baru dengan lampiran privat -> Proses tahapan status hingga tuntas -> Unduh lampiran terverifikasi.
- **Laporan & Ekspor:** Tentukan filter periode -> Tinjau tabel agregat -> Ekspor ke berkas Excel atau PDF.

## 8. Skenario pengujian alur terintegrasi (End-to-End)

| ID | Kondisi prasyarat | Langkah pengujian | Hasil yang diverifikasi |
|---|---|---|---|
| E2E-A1 | Siswa terdaftar pada kelas 10-A, Guru B ditugaskan | Guru B mencatat kehadiran kelas 10-A; Wali kelas membuka rekap | Seluruh siswa tercatat, rekap wali kelas menampilkan angka kehadiran yang cocok |
| E2E-A2 | Terdapat siswa dengan catatan alpa berulang | Petugas kesiswaan membuat kasus baru dan mencatat tindakan | Kasus berstatus DIPROSES, entri tindakan muncul di timeline beserta nama petugas |
| E2E-A3 | Guru B tidak memiliki penugasan di kelas 11-B | Guru B mencoba mengirim data absensi untuk kelas 11-B | Server menolak permintaan dengan HTTP 403; tidak ada data yang berubah |
| E2E-B1 | Modul tata usaha aktif | Staf TU membuat permohonan Surat Keterangan dan mengajukan persetujuan | Status berpindah ke MENUNGGU_PERSETUJUAN, pimpinan melihat antrean di dashboard |
| E2E-B2 | Terdapat berkas lampiran privat pada permohonan | Pengguna luar tanpa izin mencoba mengunduh URL berkas | Pengunduhan ditolak (HTTP 403/404); berkas tidak disajikan |
| E2E-R1 | Data transaksi uji terinput | Pimpinan membuka dashboard dan mengunduh laporan PDF | Total statistik agregat di dashboard dan PDF identik dengan data transaksi |
