# Product Requirements Document (PRD)

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

**Status:** rancangan awal untuk validasi sekolah dan pembimbing. **Sumber:** proposal tesis dan diskusi kebutuhan proyek. Tidak ada temuan lapangan atau hasil pengujian yang diasumsikan dalam dokumen ini.

## 1. Latar belakang dan tujuan

Sekolah membutuhkan pemetaan hubungan proses administrasi, data, aplikasi, dan pengguna. Penelitian ini mengusulkan blueprint enterprise architecture (EA) dan prototype web untuk menguji integrasi proses administrasi terpilih. Kondisi aktual, hambatan, dan prioritas harus dikonfirmasi melalui observasi, wawancara, dan telaah dokumen berizin.

Tujuan produk adalah menyediakan data bersama, mendukung alur kerja lintas peran, menampilkan informasi yang dapat ditelusuri, dan memungkinkan evaluasi proses berdasarkan skenario yang setara. Pengembangan prototype merupakan bagian dari penelitian DSRM; TOGAF ADM digunakan untuk menyusun arsitektur bisnis, data, aplikasi, dan teknologi.

## 2. Sasaran pengguna dan peran awal

| Peran | Kebutuhan awal | Batasan akses awal |
|---|---|---|
| Administrator | Mengelola akun, peran, dan data referensi | Administrasi sistem sesuai kewenangan |
| Guru | Mencatat dan melihat kehadiran | Kelas yang ditugaskan |
| Wali kelas | Memantau kehadiran dan tindak lanjut | Kelas yang menjadi tanggung jawab |
| Kesiswaan | Memantau dan mencatat tindak lanjut | Kasus dalam lingkup penugasan |
| Tata usaha | Memproses layanan dan arsip | Layanan sesuai kewenangan |
| Pimpinan | Melihat ringkasan dan memproses persetujuan | Ringkasan dan persetujuan sesuai kebijakan |

Peran dapat dirangkap (misalnya Guru yang merangkap Wali Kelas). Nama peran, penugasan, detail akses, dan pejabat pemberi persetujuan harus divalidasi dengan sekolah. Otorisasi server mengevaluasi izin riil dan penugasan objek, bukan sekadar label peran aktif di peramban.

## 3. Ruang lingkup prototype

| ID | Kebutuhan | Prioritas | Kriteria penerimaan ringkas |
|---|---|---|---|
| FR-01 | Login, logout, profil, dan multi-peran | Wajib | Pengguna aktif dapat masuk; akses tanpa izin ditolak; pemilihan konteks peran UI tidak membatalkan validasi izin sisi server |
| FR-02 | Kelola siswa, pegawai, tahun ajaran, kelas dan penempatan | Wajib | Data tervalidasi, dapat dicari, dan digunakan bersama modul terkait |
| FR-03 | Pencatatan dan rekap kehadiran | Wajib | Petugas berwenang menyimpan kehadiran kelas; satu siswa tidak memiliki catatan ganda pada konteks yang ditetapkan |
| FR-04 | Kasus dan riwayat tindak lanjut kesiswaan | Wajib | Kasus merujuk siswa; status sah dan tindakan tercatat serta dapat ditelusuri |
| FR-05 | Permohonan layanan dan riwayat proses | Wajib | Petugas membuat permohonan, memproses status yang sah, dan melihat riwayat sesuai akses |
| FR-06 | Arsip dokumen layanan | Wajib untuk skenario layanan jika dibutuhkan | Unggahan dibatasi jenis dan ukurannya, tersimpan privat, dan unduhan wajib memeriksa hak akses per objek |
| FR-07 | Dashboard dan laporan | Wajib | Ringkasan sesuai sumber berdasarkan filter dan aturan pembaruan data yang ditentukan |
| FR-08 | Ekspor Excel/PDF | Penting | Isi ekspor sesuai data dan filter yang dipilih; aktivitas ekspor dicatat |
| FR-09 | Riwayat perubahan dan aktivitas penting | Wajib | Perubahan penting, aktor, waktu, dan peristiwa penting dapat ditelusuri |
| FR-10 | Pencarian, filter, dan paginasi | Wajib | Daftar besar dapat ditelusuri berdasarkan filter relevan dan cakupan pengguna |

Kriteria detail, jenis layanan, status kehadiran, aturan ambang, serta format dokumen ditetapkan setelah validasi sekolah. Prototype minimal harus menjalankan dua skenario pada AFD; pemotongan lingkup harus disepakati apabila data atau izin terbatas.

## 4. Di luar lingkup

Menggantikan Dapodik atau e-Rapor; integrasi langsung tanpa mekanisme dan izin sah; seluruh fungsi operasional sekolah; mengukur dampak terhadap prestasi siswa atau mutu pendidikan secara keseluruhan; dan menyatakan kesiapan produksi hanya berdasarkan keberhasilan prototype.

## 5. Kebutuhan nonfungsional

- **NFR-01 Keamanan:** autentikasi JWT, otorisasi sisi server berbasis peran dan cakupan objek (IDOR protection), validasi input ketat, unggahan privat, dan konfigurasi aman.
- **NFR-02 Privasi:** gunakan data sintetis atau anonim jika data riil tidak diizinkan; batasi akses dan isi log agar tidak memuat kata sandi atau data pribadi sensitif.
- **NFR-03 Usability:** antarmuka responsif dan dapat digunakan melalui keyboard; evaluasi dengan SUS setelah skenario tugas.
- **NFR-04 Integritas:** batasan basis data, transaksi atomik, dan validasi aturan transisi status; perubahan penting diaudit dengan snapshot riwayat.
- **NFR-05 Performa:** paginasi pada server, indeks sesuai query, pengukuran latensi dan ukuran data pada lingkungan uji; target kuantitatif ditetapkan setelah baseline tersedia.
- **NFR-06 Pemeliharaan:** modular monolith, kontrak API terdokumentasi via OpenAPI, konfigurasi environment, dan pengujian terotomasi pada alur penting.

## 6. Alur dan evaluasi penelitian

Dua kandidat demonstrasi: (1) guru mencatat kehadiran -> wali kelas/kesiswaan meninjau -> petugas mencatat tindak lanjut -> pimpinan melihat ringkasan; (2) tata usaha mencatat permohonan -> pihak berwenang memproses -> status dan dokumen ditelusuri. Detail mengikuti SOP sekolah.

Evaluasi meliputi review arsitektur, black box, UAT, SUS, efisiensi tugas, dan konsistensi data. Ukur waktu, keberhasilan tugas, jumlah pencatatan ulang, dan pemeriksaan aturan data menggunakan skenario pembanding yang setara. Protokol, responden, target dan aturan pencatatan ditetapkan sebelum uji utama. Target UAT 80% dan SUS 68 adalah tolok ukur internal proposal untuk evaluasi, bukan klaim hasil sebelum pengujian. Laporkan juga hasil tanpa perbaikan dan batasi kesimpulan pada skenario uji.

## 7. Keputusan terbuka

Daftar dan jumlah pengguna, SOP serta peran aktual; ruang lingkup final; jenis layanan dan dokumen; aturan kehadiran dan kriteria kasus; data dan izin; baseline, instrumen, target dan responden; kebijakan penyimpanan serta pemulihan data; format laporan dan infrastruktur sekolah.

## 8. Matriks hak akses awal

Legenda: **K** = kelola; **L** = lihat sesuai cakupan; **P** = proses sesuai penugasan; **-** = tidak diberikan secara default. Matriks ini bukan pengganti pemeriksaan izin per objek.

| Fitur | Admin | Guru | Wali kelas | Kesiswaan | TU | Pimpinan |
|---|---|---|---|---|---|---|
| Pengguna dan peran | K | - | - | - | - | - |
| Data siswa/kelas | K | L kelas tugas | L kelas tugas | L sesuai tugas | L sesuai tugas | L agregat |
| Kehadiran | K terbatas | K kelas tugas | L/K sesuai tugas | L sesuai tugas | - | L agregat |
| Kasus kesiswaan | Administrasi izin | - | L/P kelas tugas | K sesuai tugas | - | L agregat |
| Permohonan layanan | Administrasi izin | - | - | - | K sesuai tugas | L/P sesuai tugas |
| Arsip layanan | Administrasi izin | - | - | - | K sesuai tugas | L sesuai tugas |
| Laporan | Konfigurasi | L sesuai tugas | L sesuai tugas | L sesuai tugas | L sesuai tugas | L sesuai kewenangan |
| Audit | L sesuai kebijakan | - | - | - | - | L terbatas jika disetujui |

Hak admin sistem untuk mengelola akun tidak otomatis memberikan akses ke rincian kasus sensitif. Akses istimewa, ekspor dan unduhan harus ditetapkan secara eksplisit.

## 9. Rincian kebutuhan fungsional

### FR-01 Akun dan sesi
- Pengguna memasukkan identitas dan kata sandi; sistem memberikan pesan kegagalan generik dan membatasi percobaan login (rate limit).
- Akun aktif dapat melihat profil dan peran yang diberikan. Pemilihan peran aktif di antarmuka hanya memengaruhi konteks tampilan; otorisasi final mutlak diputuskan di sisi server.
- Pengguna dapat keluar. Admin berwenang dapat menonaktifkan akun dan mengubah penugasan/peran dengan catatan audit. Mekanisme pencabutan sesi harus memvalidasi status akun di setiap panggilan penting.
- **Penerimaan:** akun nonaktif, peran yang dicabut, dan akses tanpa izin ditolak; logout dan refresh token kedaluwarsa diuji; tidak ada kata sandi atau token pada berkas log.

### FR-02 Data master
- Kelola siswa, pegawai, tahun ajaran, kelas, penempatan siswa, dan penugasan kelas bagi guru. Setiap form memeriksa field wajib dan menampilkan kesalahan per baris atau field.
- Pengguna berwenang mencari dan memfilter data, melihat detail, dan mengubah status sesuai kebijakan. Riwayat penempatan tidak boleh dihapus saat siswa pindah kelas.
- **Penerimaan:** nomor identitas unik (NIS/NIP) tidak duplikat; penempatan tumpang tindih ditolak; siswa yang tidak terdaftar pada tanggal transaksi absensi ditolak dari pencatatan.

### FR-03 Kehadiran
- Petugas memilih tahun ajaran, kelas, dan tanggal; daftar siswa dimuat berdasarkan penempatan aktif pada tanggal tersebut.
- Petugas mengisi status setiap siswa dan menyimpan secara batch dalam satu transaksi atomik. Koreksi mengikuti hak akses dan rentang waktu yang disepakati sekolah.
- **Penerimaan:** input tidak valid ditolak seluruhnya tanpa menyimpan sebagian; data tersimpan muncul pada rekap; koreksi, nama aktor, dan waktu tercatat dalam histori; pengguna di luar cakupan kelas ditolak (403).

### FR-04 Tindak lanjut
- Pengguna berwenang memfilter rekap kehadiran dan melihat indikator siswa yang memerlukan perhatian berdasarkan aturan sekolah (bukan vonis otomatis).
- Buat kasus dengan memilih siswa, ringkasan alasan, dan penanggung jawab; catat tindakan, status, dan riwayat peristiwa (*case events*).
- **Penerimaan:** transisi status di luar state machine yang sah ditolak; riwayat konsisten dengan status terkini; akses detail sensitif dibatasi sesuai kewenangan penugasan.

### FR-05 dan FR-06 Layanan dan arsip
- Petugas TU membuat permohonan dengan memilih jenis layanan, identitas pemohon, keterangan pendukung, dan lampiran berkas bila disyaratkan.
- Petugas yang berwenang memproses permohonan melalui tahapan status yang sah. Setiap aksi mencatat aktor, waktu, dan catatan proses.
- Berkas disimpan pada direktori privat dengan nama acak (UUID). Pengunduhan mewajibkan autentikasi dan otorisasi hak akses terhadap permohonan terkait.
- **Penerimaan:** field wajib per jenis layanan tervalidasi; pihak tanpa izin tidak bisa mengubah status atau mengunduh lampiran; berkas gagal validasi (format/ukuran) tidak disimpan.

### FR-07 hingga FR-10 Informasi dan keterlacakan
- Dashboard dan laporan menyediakan filter periode serta keterangan satuan data yang jelas. Tabel mendukung pencarian, pengurutan, dan paginasi di sisi server.
- Ekspor Excel dan PDF menerapkan filter dan batasan hak akses yang persis sama dengan tampilan tabel; metadata waktu pembuatan dan pembuat tercatat.
- **Penerimaan:** angka rekapitulasi dashboard dan ekspor identik dengan dataset sumber; setiap aksi penting memiliki log audit; data di luar cakupan peran tidak bocor pada daftar maupun ekspor.

## 10. User story prioritas

| ID | Cerita | Hasil yang diharapkan |
|---|---|---|
| US-01 | Sebagai guru saya ingin mencatat kehadiran kelas tugas pada tanggal tertentu | Satu batch tersimpan atomik, kesalahan input dapat diperbaiki, histori penyesuaian tercatat |
| US-02 | Sebagai wali kelas saya ingin melihat rekap siswa di kelas saya | Data tersaji sesuai periode dan sistem menolak akses ke kelas lain |
| US-03 | Sebagai petugas kesiswaan saya ingin mencatat tindakan untuk siswa | Tindakan dan transisi status tercatat berurutan dalam riwayat |
| US-04 | Sebagai TU saya ingin melacak permohonan beserta lampiran | Status permohonan, penanggung jawab, dan dokumen privat hanya dapat dibuka oleh pihak berhak |
| US-05 | Sebagai pimpinan saya ingin ringkasan untuk meninjau layanan | Agregat angka konsisten dengan sumber data tanpa membuka catatan sensitif individu |
| US-06 | Sebagai peneliti saya ingin membandingkan tugas sepadan | Data durasi, keberhasilan tugas, dan pencatatan ulang tercatat secara objektif |

## 11. Definisi indikator

- **Keberhasilan tugas** = jumlah tugas selesai sesuai kriteria / jumlah tugas yang dicoba; laporkan jumlah absolut dan penyebab kegagalan.
- **Perubahan waktu** = `(waktu pembanding - waktu prototype) / waktu pembanding * 100%`, untuk pasangan tugas yang memenuhi protokol uji. Laporkan sebaran waktu, bukan hanya rata-rata.
- **Pencatatan ulang** = jumlah entri ulang informasi yang sama per tugas berdasarkan definisi protokol pengujian.
- **Konsistensi** = jumlah pemeriksaan yang sesuai aturan data / seluruh pemeriksaan yang dilakukan; laporkan rincian anomali data jika ada.
- **UAT dan SUS:** instrumen, jumlah responden, metode penilaian, dan kriteria penerimaan didokumentasikan secara transparan. Hasil uji mencerminkan prototype pada skenario yang diuji, bukan klaim kesiapan produksi seluruh sekolah.
