# PANDUAN PENGGUNA SISTEM (USER GUIDE)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

Dokumen ini merupakan panduan lengkap penggunaan aplikasi Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut untuk seluruh staf pengajar, tenaga kependidikan, dan pimpinan sekolah.

---

## BAB 1 - Pengenalan Aplikasi

### 1.1 Tujuan Aplikasi
Aplikasi Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut dibangun untuk mempermudah, mempercepat, dan menertibkan tata kelola administrasi sekolah sehari-hari secara digital, terpusat, dan aman.

### 1.2 Fungsi Utama Aplikasi
1. **Administrasi Data Akademik**: Pengelolaan data tahun ajaran, rombongan belajar (kelas), biodata siswa, data kepegawaian guru, serta penugasan wali kelas dan guru mata pelajaran.
2. **Pencatatan Presensi Terpadu**: Pengisian presensi kehadiran siswa harian secara langsung oleh guru, pemantauan rekapitulasi kehadiran oleh wali kelas, serta pengunduhan laporan kehadiran berkala.
3. **Layanan Bimbingan dan Kasus Kesiswaan**: Pencatatan kejadian kedisiplinan dan pembinaan siswa oleh tim kesiswaan dan guru BK, pemantauan alur penanganan, serta perlindungan ketat terhadap kerahasiaan catatan konseling privat siswa.
4. **Pelayanan Persuratan Tata Usaha**: Pengajuan permohonan surat keterangan, legalisir ijazah, atau mutasi siswa oleh tata usaha, verifikasi berkas lampiran, dan penerbitan persetujuan resmi oleh Kepala Sekolah.
5. **Dashboard Informasi Eksekutif**: Penyajian ringkasan data statistik sekolah bagi pimpinan untuk mendukung pengambilan keputusan berbasis data.

### 1.3 Pengguna Sistem
Sistem ini digunakan oleh enam kelompok pengguna utama:
1. **Administrator**: Pengelola teknis sistem dan data induk sekolah.
2. **Guru**: Tenaga pengajar pengampu mata pelajaran di kelas.
3. **Wali Kelas**: Guru penanggung jawab rombongan belajar binaan.
4. **Kesiswaan / Guru BK**: Staf pembimbing dan penegak tata tertib siswa.
5. **Tata Usaha**: Petugas pelayanan persuratan dan kearsipan dokumen sekolah.
6. **Pimpinan (Kepala Sekolah)**: Penanggung jawab sekolah dan pemberi persetujuan surat resmi.

### 1.4 Cara Mengakses Aplikasi
Buka aplikasi melalui peramban web (Google Chrome, Microsoft Edge, atau Mozilla Firefox) pada komputer atau laptop yang terhubung ke jaringan sekolah:
- **Alamat Web Aplikasi**: `http://localhost:3000`

---

## BAB 2 - Login dan Navigasi

### 2.1 Langkah Masuk ke Sistem (Login)
1. Buka alamat `http://localhost:3000` pada peramban web Anda.
2. Layar akan menampilkan halaman **Masuk Sistem Informasi Enterprise Administrasi SMAN 1 Bunut**.
3. Masukkan **Nama Pengguna (Username)** dan **Kata Sandi (Password)** Anda pada kolom yang tersedia.
4. Klik tombol **Masuk ke Sistem**.
5. Jika data yang dimasukkan benar, sistem akan mengarahkan Anda langsung ke Halaman Utama (Dashboard) sesuai peran tugas Anda.

### 2.2 Mengenali Halaman Utama (Dashboard)
Setelah berhasil masuk, Anda akan melihat:
- **Header Atas**: Menampilkan nama sekolah, nama lengkap Anda, peran tugas aktif, dan menu akun profil.
- **Menu Navigasi Samping (Sidebar)**: Menampilkan daftar modul aplikasi yang berhak Anda akses.
- **Kartu Ringkasan Data**: Menampilkan data statistik penting, seperti persentase kehadiran hari ini, permohonan surat yang membutuhkan tindak lanjut, atau jumlah kasus aktif.

### 2.3 Menggunakan Menu Navigasi Samping (Sidebar)
- Klik ikon atau nama menu di sisi kiri untuk berpindah modul.
- Pada layar berukuran kecil (ponsel atau tablet), menu samping dapat disembunyikan atau dimunculkan menggunakan tombol menu tiga garis di pojok kiri atas.

### 2.4 Mengakses Profil dan Ganti Peran
- Klik nama Anda di sudut kanan atas untuk melihat informasi profil pegawai Anda.
- Bagi pengguna yang memiliki lebih dari satu peran (misalnya Guru yang juga menjabat sebagai Wali Kelas), sistem menyediakan menu peralihan peran di header untuk berpindah konteks kerja secara instan tanpa perlu keluar dari sistem.

### 2.5 Keluar dari Sistem (Logout)
1. Klik foto atau nama pengguna Anda di sudut kanan atas.
2. Pilih menu **Keluar (Logout)**.
3. Sistem akan menghapus sesi kerja Anda dan mengembalikan tampilan ke halaman login. Selalu biasakan keluar dari sistem jika menggunakan komputer bersama di ruang guru atau laboratorium.

### 2.6 Mengatasi Kendala Saat Masuk Sistem
- **Pesan "Nama pengguna atau kata sandi salah"**: Periksa kembali penulisan huruf besar dan kecil pada nama pengguna serta kata sandi Anda.
- **Pesan "Terlalu banyak percobaan masuk"**: Sistem mendeteksi beberapa kali kesalahan kata sandi berturut-turut. Tunggu selama 60 detik sebelum mencoba kembali.
- **Halaman tidak merespons**: Pastikan kabel jaringan atau sambungan Wi-Fi Anda dalam keadaan aktif, lalu muat ulang halaman dengan menekan tombol `F5`.

---

## BAB 3 - Pemetaan Peran dan Hak Akses

Setiap pengguna di SMAN 1 Bunut hanya dapat membuka menu dan menjalankan fungsi yang sesuai dengan wewenang tugas kedinasannya:

| Peran (Role) | Menu yang Dapat Diakses | Tindakan yang Diperbolehkan | Batasan dan Larangan Akses |
|---|---|---|---|
| **Administrator** | Data Master, Akun Pengguna, Penugasan Guru, Log Aktivitas | Membuat dan mengubah akun, rombel, tahun ajaran, dan memeriksa riwayat aktivitas sistem. | Dilarang membuka catatan konseling privat kesiswaan dan dilarang menyetujui surat dinas pimpinan. |
| **Guru** | Presensi Harian, Rekap Presensi Kelas | Memilih rombel penugasan, mencatat kehadiran harian siswa, dan mengunduh rekap presensi kelas. | Hanya dapat membuka rombel yang ditugaskan; tidak dapat mengubah data siswa atau membuka kasus kesiswaan. |
| **Wali Kelas** | Dashboard Rombel, Rekap Presensi, Kasus Siswa Binaan | Memantau seluruh siswa di kelas binaan, memeriksa rekap absensi rombel, dan membaca status pembinaan siswa binaan. | Catatan konseling privat BK disamarkan secara otomatis demi etika kerahasiaan siswa; tidak dapat membuka kelas lain. |
| **Kesiswaan / BK** | Manajemen Kasus Siswa, Riwayat Pembinaan | Mencatat kasus pelanggaran, mediasi orang tua, mencatat bimbingan konseling privat, dan menutup kasus. | Tidak dapat mengubah data rombel atau memproses permohonan surat tata usaha. |
| **Tata Usaha** | Permohonan Surat, Pengarsipan Dokumen | Mendaftarkan permohonan surat siswa, mengunggah berkas syarat, meneruskan ke pimpinan, dan mengunduh arsip. | Tidak dapat mengubah hasil presensi guru atau memutuskan persetujuan surat yang menjadi wewenang pimpinan. |
| **Pimpinan (Kepsek)**| Dashboard Pimpinan, Antrean Persetujuan Surat, Rekapitulasi Eksekutif | Memeriksa permohonan surat tata usaha, memberikan tanda tangan persetujuan resmi, menolak surat dengan catatan, dan mengunduh laporan tahunan. | Tidak dapat mengubah absensi harian kelas dan tidak dapat membuka rincian teks rahasia konseling bimbingan siswa. |

---

## BAB 4 - Panduan Administrator

Peran Administrator bertanggung jawab atas kelancaran operasional data induk sekolah.

### 4.1 Mengelola Akun Pengguna dan Peran
1. Buka menu **Kelola Pengguna** di sidebar.
2. Untuk mendaftarkan akun staf baru: klik tombol **Tambah Pengguna Baru**.
3. Masukkan nama pengguna, nama lengkap pegawai, dan pilih peran kedinasan yang sesuai.
4. Simpan data. Pengguna baru dapat langsung mengaktifkan akunnya.
5. Untuk menonaktifkan pengguna yang mutasi keluar: cari nama pengguna, klik tombol aksi, lalu pilih **Nonaktifkan Akun**.

### 4.2 Mengelola Tahun Ajaran Baru
1. Buka menu **Data Master -> Tahun Ajaran**.
2. Klik tombol **Tambah Tahun Ajaran**.
3. Masukkan nama tahun ajaran (contoh: `2027/2028`), tanggal mulai, dan tanggal selesai.
4. Tandai kotak **Tahun Ajaran Aktif** jika tahun ajaran ini akan menjadi acuan pembelajaran saat ini.
5. Sistem secara otomatis memastikan hanya ada satu tahun ajaran yang berstatus aktif.

### 4.3 Mengelola Rombongan Belajar (Kelas)
1. Buka menu **Data Master -> Rombel (Kelas)**.
2. Klik **Tambah Rombel**.
3. Tentukan tingkat kelas (10, 11, atau 12) dan nama kelas (contoh: `X-1` atau `XI-MIPA-1`).
4. Hubungkan rombel dengan tahun ajaran aktif, lalu klik **Simpan**.

### 4.4 Mengelola Biodata Siswa dan Penempatan Kelas
1. Buka menu **Data Master -> Siswa**.
2. Untuk mendaftarkan siswa: klik **Tambah Siswa**, masukkan NISN, Nama Lengkap, Jenis Kelamin, dan simpan.
3. Untuk menempatkan siswa ke kelas: buka tab **Penempatan Siswa (Enrollment)**, pilih nama siswa, pilih kelas tujuan, dan masukkan tanggal mulai masuk rombel.

### 4.5 Menugaskan Wali Kelas dan Guru Mata Pelajaran
1. Buka menu **Data Master -> Penugasan Guru**.
2. Pilih kelas rombel yang ingin ditentukan pengampunya.
3. Pilih nama guru yang bertugas sebagai **Wali Kelas** (satu rombel wajib memiliki satu Wali Kelas).
4. Tambahkan guru pengampu mata pelajaran (**Guru Mapel**) pada rombel tersebut.
5. Klik **Simpan Penugasan**.

### 4.6 Memeriksa Rekam Jejak Audit (Log Aktivitas)
1. Buka menu **Audit Sistem**.
2. Anda dapat melihat riwayat setiap mutasi data, aksi pembuatan permohonan, perubahan presensi, dan waktu login pengguna.
3. Manfaatkan kolom pencarian untuk melacak aktivitas staf berdasarkan nama pengguna atau rentang tanggal.

---

## BAB 5 - Panduan Guru

Peran Guru fokus pada pencatatan presensi siswa secara akurat setiap hari pembelajaran.

### 5.1 Mencatat Presensi Harian Siswa
1. Masuk ke aplikasi menggunakan akun guru Anda, lalu pilih menu **Presensi Harian**.
2. Pada dropdown pilihan kelas, pilih rombel yang Anda ajar (hanya kelas penugasan Anda yang ditampilkan).
3. Pilih tanggal pembelajaran yang bersangkutan (default: hari ini).
4. Layar akan menampilkan daftar seluruh siswa yang terdaftar di kelas tersebut secara berurutan.
5. Tetapkan status kehadiran setiap siswa:
   - **Hadir (H)**: Siswa hadir di kelas (default otomatis terpilih Hadir).
   - **Sakit (S)**: Siswa berhalangan karena sakit. Isi kolom keterangan dengan diagnosis singkat (contoh: "Demam").
   - **Izin (I)**: Siswa berhalangan karena izin resmi. Isi keterangan (contoh: "Keperluan keluarga").
   - **Alpa (A)**: Siswa tidak hadir tanpa keterangan yang sah.
6. Periksa kembali seluruh baris siswa.
7. Klik tombol **Simpan Presensi Kelas**.
8. Sistem akan menampilkan pemberitahuan hijau bahwa presensi berhasil disimpan.

### 5.2 Memperbaiki Catatan Presensi
Jika terdapat kekeliruan (misalnya surat dokter baru diterima siang hari):
1. Buka kembali halaman **Presensi Harian**, pilih kelas dan tanggal yang ingin diperbaiki.
2. Ubah status siswa yang bersangkutan dari **Alpa** menjadi **Sakit**.
3. Klik tombol **Simpan Pembaruan**.
4. Sistem mencatat pembaruan tersebut ke dalam riwayat perubahan presensi secara otomatis.

### 5.3 Menangani Konflik Penyimpanan Data
Jika Anda dan guru piket membuka kelas yang sama secara bersamaan:
- Sistem menggunakan mekanisme penguncian aman. Jika orang lain telah menyimpan perubahan terlebih dahulu, sistem akan memunculkan pesan peringatan: *"Data presensi telah diperbarui oleh pengguna lain. Halaman akan dimuat ulang untuk membaca data terbaru."*
- Cukup muat ulang halaman, periksa perubahan terakhir, lalu simpan kembali catatan Anda.

---

## BAB 6 - Panduan Wali Kelas

Wali Kelas bertindak sebagai pembimbing utama rombongan belajar binaannya.

### 6.1 Memantau Rombongan Belajar Binaan
1. Setelah login sebagai Wali Kelas, dashboard Anda akan langsung menyajikan ringkasan kelas binaan Anda.
2. Anda dapat melihat persentase kehadiran rombel hari ini, jumlah siswa sakit atau izin, serta daftar siswa binaan yang membutuhkan perhatian khusus.

### 6.2 Memeriksa Rekapitulasi Presensi Bulanan
1. Buka menu **Rekapitulasi Presensi**.
2. Pilih rentang tanggal (misalnya dari tanggal 1 sampai 30 bulan berjalan).
3. Sistem akan menyajikan tabel persentase kehadiran setiap siswa binaan beserta rincian jumlah Hadir, Sakit, Izin, dan Alpa.
4. Klik tombol **Unduh Rekap Excel** jika Anda memerlukan salinan lembar rekap untuk arsip fisik atau laporan ke orang tua siswa.

### 6.3 Memantau Catatan Kasus Kesiswaan Siswa Binaan
1. Buka menu **Kasus Siswa Binaan**.
2. Anda hanya dapat melihat kasus yang dialami oleh siswa di kelas Anda.
3. Anda dapat membaca judul kasus, tanggal pelaporan, status penanganan (Baru, Diproses, atau Selesai), dan ringkasan arahan pembinaan.
4. **Perlindungan Privasi**: Catatan konseling privat yang ditulis oleh Guru BK akan otomatis disamarkan (tampil sebagai `[Catatan konseling privat - Terproteksi]`). Hal ini bertujuan melindungi privasi psikologis siswa sesuai kode etik bimbingan konseling nasional.

---

## BAB 7 - Panduan Kesiswaan dan Guru BK

Peran Kesiswaan bertanggung jawab atas pembinaan karakter, kedisiplinan, dan konseling siswa.

### 7.1 Mendaftarkan Kasus Kesiswaan Baru
1. Buka menu **Manajemen Kasus Kesiswaan**.
2. Klik tombol **Buat Laporan Kasus Baru**.
3. Cari nama siswa yang bersangkutan.
4. Masukkan **Judul Masalah** (contoh: "Keterlambatan Berulang Masuk Jam Pertama") dan **Ringkasan Kejadian**.
5. Klik **Simpan Laporan**. Status awal kasus adalah **Baru**.

### 7.2 Memulai Penanganan dan Penjadwalan Mediasi
1. Buka rincian kasus yang ingin ditangani.
2. Klik tombol aksi **Mulai Penanganan**. Status kasus akan berubah menjadi **Diproses**.
3. Di dalam rincian kasus, pilih aksi **Catat Tindakan Pembinaan**.
4. Pilih jenis tindakan: *Pemberian Peringatan Lisan*, *Bimbingan Konseling*, *Panggilan Orang Tua*, atau *Pembuatan Surat Perjanjian*.
5. Tuliskan catatan pembinaan. Jika tindakan merupakan konseling pribadi, catatan ini dijamin aman dan hanya dapat dibaca oleh tim Kesiswaan / BK.

### 7.3 Menyelesaikan Kasus Siswa
1. Setelah siswa memenuhi pembinaan dan menunjukkan perbaikan sikap, buka rincian kasus.
2. Klik tombol **Selesaikan Kasus**.
3. Masukkan catatan kesimpulan penyelesaian kasus (contoh: "Siswa telah menandatangani komitmen perbaikan dan hadir tepat waktu selama 14 hari berturut-turut").
4. Status kasus kini menjadi **Selesai**. Kasus yang telah selesai tersimpan sebagai riwayat pembinaan dan tidak dapat diubah kembali.

---

## BAB 8 - Panduan Tata Usaha

Peran Tata Usaha melayani kebutuhan administrasi persuratan siswa secara cepat dan terdokumentasi.

### 8.1 Mendaftarkan Permohonan Surat
1. Buka menu **Pelayanan Surat**.
2. Klik tombol **Buat Permohonan Baru**.
3. Pilih nama siswa yang mengajukan permohonan.
4. Pilih **Jenis Layanan** (contoh: *Surat Keterangan Aktif Sekolah*, *Surat Izin Penelitian*, *Surat Keterangan Berkelakuan Baik*, atau *Surat Keterangan Mutasi*).
5. Masukkan keperluan surat (contoh: "Persyaratan pendaftaran beasiswa prestasi kabupaten").
6. Klik **Simpan Permohonan**. Permohonan kini tercatat dengan status **Diajukan**.

### 8.2 Mengunggah Berkas Persyaratan
1. Pada rincian permohonan, cari bagian **Dokumen Lampiran**.
2. Klik tombol **Unggah Berkas**.
3. Pilih berkas persyaratan dari komputer Anda (format PDF, ukuran maksimal 5 MB; contoh: Kartu Keluarga atau Kartu Pelajar).
4. Berkas akan tersimpan secara terenkripsi pada arsip digital privat sekolah.

### 8.3 Memproses dan Meneruskan ke Pimpinan
1. Setelah seluruh syarat lengkap, klik tombol **Proses Berkas**. Status permohonan berubah menjadi **Diproses**.
2. Buat draf naskah surat resmi sesuai nomor surat yang berlaku.
3. Klik tombol **Ajukan Persetujuan ke Pimpinan**. Permohonan otomatis masuk ke antrean pimpinan sekolah.

### 8.4 Menerbitkan Surat dan Pengarsipan
1. Setelah Pimpinan memberikan persetujuan, status surat akan menjadi **Disetujui**.
2. Cetak surat resmi untuk distempel dan diserahkan kepada pemohon.
3. Pada sistem, klik tombol **Selesaikan dan Arsipkan**.
4. Surat resmi kini tersimpan rapi dalam **Arsip Surat Digital**.

---

## BAB 9 - Panduan Pimpinan (Kepala Sekolah)

Peran Pimpinan memegang wewenang pengawasan eksekutif dan persetujuan resmi dokumen sekolah.

### 9.1 Memantau Kondisi Sekolah Melalui Dashboard Pimpinan
Saat login sebagai Pimpinan, Anda akan disajikan indikator penting sekolah:
- **Tingkat Kehadiran Sekolah**: Persentase kehadiran seluruh rombel hari ini.
- **Antrean Surat Menunggu Disposisi**: Jumlah permohonan surat yang membutuhkan persetujuan Anda.
- **Jumlah Kasus Siswa Aktif**: Jumlah kasus yang sedang dalam penanganan tim kesiswaan.

### 9.2 Menyetujui atau Menolak Permohonan Surat
1. Buka menu **Antrean Persetujuan Pimpinan**.
2. Klik pada salah satu permohonan yang menunggu persetujuan.
3. Periksa rincian data pemohon, jenis surat, alasan permohonan, dan periksa berkas lampiran pendukung.
4. Pengambilan Keputusan:
   - **Menyetujui**: Klik tombol hijau **Setujui Surat**. Masukkan catatan disposisi singkat jika diperlukan. Status permohonan otomatis berubah menjadi **Disetujui**, dan tata usaha dapat mencetak surat resmi.
   - **Menolak**: Klik tombol merah **Tolak Permohonan**. Sistem mewajibkan Anda mengisi alasan penolakan (contoh: "Syarat kelulusan belum terpenuhi, harap lengkapi dokumen raport terlebih dahulu"). Status berubah menjadi **Ditolak** dan berkas dikembalikan ke tata usaha.

### 9.3 Mengunduh Laporan Eksekutif
Pimpinan berhak mengunduh laporan rekapitulasi sekolah:
1. Buka menu **Laporan Eksekutif**.
2. Pilih jenis laporan:
   - **Laporan Kehadiran Tahunan (Format Excel)**: Menyajikan matriks rekap kehadiran per kelas dan per siswa selama tahun ajaran berjalan.
   - **Laporan Pelayanan Administrasi (Format PDF)**: Menyajikan statistik jumlah surat masuk, jenis layanan terbanyak, dan kecepatan pemrosesan berkas.

---

## BAB 10 - Alur Kerja Antar-Peran

Berikut adalah visualisasi alur kolaborasi antar-peran dalam proses bisnis utama sekolah:

### 10.1 Alur Kerja Pencatatan dan Pemantauan Presensi

```mermaid
flowchart LR
    A["Guru Mengampu"] -->|"Isi Kehadiran Harian"| B["Sistem Presensi"]
    B -->|"Kalkulasi Otomatis"| C["Wali Kelas"]
    C -->|"Pantau Rekap Rombel"| D["Pimpinan Sekolah"]
    D -->|"Unduh Laporan Tahunan"| E["Evaluasi Sekolah"]
```

### 10.2 Alur Kerja Pelayanan Persuratan Tata Usaha

```mermaid
flowchart TD
    A["Siswa / Pemohon"] -->|"Ajukan Permohonan"| B["Tata Usaha"]
    B -->|"Verifikasi Berkas Lampiran"| C{"Syarat Lengkap?"}
    C -- "Tidak" -->|"Minta Kelengkapan"| A
    C -- "Ya" -->|"Proses & Ajukan Persetujuan"| D["Pimpinan (Kepsek)"]
    D -->|"Periksa Naskah & Dokumen"| E{"Keputusan Pimpinan"}
    E -- "Disetujui" --> F["Tata Usaha Terbitkan Surat"]
    E -- "Ditolak" --> G["Tata Usaha Beritahu Pemohon"]
    F --> H["Arsip Surat Digital Sekolah"]
```

---

## BAB 11 - Panduan Pengujian Manual Pengguna

Tabel berikut disiapkan untuk memandu verifikasi manual fungsi aplikasi oleh tim penguji atau perwakilan pengguna sekolah:

| ID Skenario | Peran Penguji | Kondisi Awal | Langkah-Langkah Pengujian | Hasil yang Diharapkan | Hasil Aktual | Status | Catatan |
|---|---|---|---|---|---|---|---|
| **TC-01** | Semua Peran | Halaman login terbuka | Masukkan username dan password resmi lokal, klik Masuk | Berhasil masuk ke dashboard sesuai peran masing-masing | | | |
| **TC-02** | Administrator | Login sebagai `admin` | Buka menu Master Data -> Kelas, tambahkan rombel baru | Rombel baru tersimpan dan muncul di daftar kelas | | | |
| **TC-03** | Administrator | Login sebagai `admin` | Buka menu Penugasan Guru, pasangkan guru ke rombel | Penugasan tersimpan; guru mendapat hak akses rombel | | | |
| **TC-04** | Guru | Login sebagai `guru` | Buka Presensi Harian, pilih kelas X-1, simpan presensi | Data kehadiran tersimpan dengan notifikasi sukses hijau | | | |
| **TC-05** | Guru | Login sebagai `guru` | Coba akses rombel kelas XII-4 (luar penugasan) | Akses ditolak dengan pesan peringatan wewenang | | | |
| **TC-06** | Wali Kelas | Login sebagai `wali_kelas` | Buka menu Rekapitulasi Presensi kelas binaan | Ringkasan persentase hadir, sakit, izin, alpa tampil akurat | | | |
| **TC-07** | Kesiswaan | Login sebagai `kesiswaan` | Buat kasus siswa baru, ubah status menjadi Diproses | Kasus baru tercatat di timeline dengan status aktif | | | |
| **TC-08** | Wali Kelas | Login sebagai `wali_kelas` | Buka kasus siswa binaan yang berisi catatan konseling BK | Rincian kasus tampil, namun teks konseling privat disamarkan | | | |
| **TC-09** | Tata Usaha | Login sebagai `tata_usaha`| Buat permohonan surat keterangan aktif, unggah berkas PDF | Permohonan terdaftar dan berkas lampiran berhasil diunggah | | | |
| **TC-10** | Tata Usaha | Login sebagai `tata_usaha`| Teruskan permohonan surat ke tahap persetujuan pimpinan | Status permohonan berubah menjadi Menunggu Persetujuan | | | |
| **TC-11** | Pimpinan | Login sebagai `kepsek` | Buka Antrean Persetujuan, klik Setujui Surat | Status surat berubah menjadi Disetujui | | | |
| **TC-12** | Pimpinan | Login sebagai `kepsek` | Buka menu Laporan, unduh Laporan Presensi Excel | Berkas spreadsheet `.xlsx` berhasil diunduh dan dapat dibuka | | | |

---

## BAB 12 - Masalah Umum Pengguna dan Solusinya

Berikut adalah rangkuman solusi atas pertanyaan dan masalah yang sering dihadapi pengguna di lingkungan sekolah:

### 1. Bagaimana jika saya lupa kata sandi saya?
- **Penyebab**: Kata sandi belum dicatat atau salah mengingat kombinasi huruf.
- **Solusi**: Hubungi staf Administrator SIM SMAN 1 Bunut di ruang laboratorium komputer untuk mereset kata sandi akun Anda. Sistem tidak menyediakan reset otomatis via email demi keamanan data internal sekolah.

### 2. Mengapa saya tidak dapat melihat menu pendaftaran akun atau data master?
- **Penyebab**: Akun Anda terdaftar sebagai Guru, Wali Kelas, atau Staf TU biasa yang memang tidak memiliki kewenangan mengubah struktur data induk sekolah.
- **Solusi**: Hal ini adalah perilaku normal sistem. Pengelolaan data master hanya dapat dilakukan oleh akun Administrator.

### 3. Mengapa saya sebagai Guru tidak dapat membuka kelas tertentu saat mengisi presensi?
- **Penyebab**: Anda belum ditugaskan secara resmi pada kelas rombel tersebut untuk tahun ajaran aktif.
- **Solusi**: Hubungi Administrator atau Wakil Kepala Sekolah Bidang Kurikulum untuk memeriksa dan memperbarui data penugasan mengajar Anda di menu Penugasan Guru.

### 4. Mengapa muncul peringatan "Data presensi telah diperbarui pengguna lain"?
- **Penyebab**: Terjadi pembaharuan data bersamaan (misalnya guru piket sedang mencatat izin di saat yang sama Anda menyimpan absensi).
- **Solusi**: Cukup muat ulang halaman peramban web Anda, periksa data terbaru yang sudah masuk, lalu simpan kembali catatan Anda.

### 5. Mengapa permohonan surat tidak dapat diteruskan ke Pimpinan?
- **Penyebab**: Status permohonan belum berada pada tahap "Diproses", atau berkas persyaratan wajib belum diunggah.
- **Solusi**: Pastikan Anda telah menekan tombol "Proses Berkas" terlebih dahulu dan memastikan berkas lampiran pendukung telah terunggah dengan baik.

### 6. Mengapa tombol persetujuan surat tidak muncul pada akun saya?
- **Penyebab**: Anda sedang login menggunakan akun Tata Usaha atau Guru.
- **Solusi**: Wewenang persetujuan surat resmi dinas sekolah berada secara eksklusif pada akun Pimpinan (Kepala Sekolah). Masuklah menggunakan akun Kepala Sekolah untuk memberikan persetujuan.

### 7. Mengapa sistem tiba-tiba meminta saya login kembali saat sedang bekerja?
- **Penyebab**: Masa aktif sesi keamanan (token masuk) telah berakhir (30 menit tanpa aktivitas).
- **Solusi**: Masukkan kembali nama pengguna dan kata sandi Anda. Fitur ini dirancang untuk melindungi kerahasiaan data siswa apabila komputer ditinggalkan tanpa pengawasan di meja kerja.
