# Implementation Plan Document (IPD)

**Status:** rencana implementasi bertahap mengacu metodologi DSRM (enam bulan); jadwal diselaraskan dengan ketersediaan akses data sekolah dan responden pengujian.

## 1. Tahap penelitian dan luaran

| Tahap | Perkiraan | Kegiatan utama | Luaran / Kriteria selesai |
|---|---|---|---|
| 0. Persiapan | Bulan 1 | Perizinan sekolah, identifikasi stakeholder, telaah literatur | Surat izin riset dan rencana studi lapangan tersedia |
| 1. Penemuan kebutuhan | Bulan 1-2 | Observasi, wawancara, inventarisasi data/proses, pemetaan as-is | Dokumen kebutuhan tervalidasi dan proses prioritas disepakati |
| 2. Arsitektur enterprise | Bulan 2-3 | Penerapan TOGAF ADM: visi, arsitektur bisnis, data, aplikasi, teknologi | Blueprint EA dan matriks keterlacakan ditinjau stakeholder |
| 3. Fondasi teknis | Bulan 3 | Setup repositori, penguncian dependensi, inisialisasi Django Ninja & React Vite, setup database dan auth | Aplikasi berjalan di lokal, endpoint login/me lulus uji keamanan |
| 4. Konstruksi prototype | Bulan 4-5 | Implementasi data master, absensi batch, kasus kesiswaan, layanan TU, dokumen privat, dashboard dan ekspor | Dua skenario utama (A dan B) dapat dijalankan menggunakan data sintetis |
| 5. Pengujian & evaluasi | Bulan 5 | Uji black box, integrasi API, review arsitektur, UAT, kuesioner SUS, dan pengukuran efisiensi tugas | Bukti evaluasi tercatat objektif sesuai protokol uji |
| 6. Analisis & penyusunan tesis | Bulan 5-6 | Analisis data uji, pembahasan keterbatasan, perumusan rekomendasi pengembangan masa depan | Laporan tesis lengkap menghubungkan artefak DSRM dan bukti evaluasi |

## 2. Urutan kerja teknis

1. Mengunci dependensi runtime Python dan Node.js melalui lockfile, menyiapkan berkas `.env.example`, dan menyusun skrip inisialisasi awal.
2. Membangun Custom User Model sebelum migrasi pertama dijalankan, konfigurasi grup peran Django, endpoint autentikasi JWT (`django-ninja-jwt`), serta penanganan error terstandar.
3. Merancang skema data master (tahun ajaran, kelas, pegawai, siswa, penempatan enrollment, dan penugasan guru), membuat migrasi basis data, dan memuat fixture data sintetis.
4. Membangun modul absensi: validasi penempatan aktif, transaksi batch atomik, pencatatan histori perubahan via bulk history helper, dan invalidasi cache.
5. Membangun modul kesiswaan (state machine status kasus dan timeline event), dilanjutkan modul persuratan tata usaha dan penyimpanan berkas privat.
6. Membangun kueri agregasi dashboard, generator ekspor Excel dan PDF, serta mekanisme invalidasi cache Redis pasca commit.
7. Membangun frontend React: generasi tipe dari skema OpenAPI backend, form validasi Zod, tabel server-side, state management TanStack Query dan Zustand.
8. Melakukan pengujian integrasi end-to-end terhadap Skenario A dan B, verifikasi hak akses per objek (IDOR), dan pengujian responsivitas peramban.

## 3. Keterlacakan artefak DSRM

| Dimensi penelitian | Artefak dan bukti fisik |
|---|---|
| Masalah & kebutuhan aktual | Catatan wawancara, diagram alur kerja as-is (BPMN), daftar kebutuhan terverifikasi |
| Blueprint arsitektur | Visi EA, model proses to-be, diagram relasi data (ERD), arsitektur aplikasi dan teknologi (TOGAF) |
| Realisasi prototype | Kode sumber backend dan frontend, skema migrasi ORM, dokumentasi OpenAPI, data uji sintetis |
| Validitas fungsi | Laporan uji black box, pengujian integrasi API (pytest), uji komponen antarmuka (Vitest) |
| Penerimaan & evaluasi proses | Hasil penilaian kuesioner SUS, lembar UAT, pengukuran durasi waktu tugas dan pencatatan ulang |

## 4. Protokol evaluasi penelitian

- **Pemilihan responden:** Melibatkan perwakilan peran sebenarnya dari sekolah (guru, staf tata usaha, petugas kesiswaan, dan pimpinan).
- **Skenario tugas berpasangan:** Responden menjalankan tugas terstandar yang sepadan (Skenario A untuk absensi dan kasus, Skenario B untuk layanan tata usaha).
- **Pengukuran kuantitatif:**
  - Waktu penyelesaian tugas dihitung dari saat instruksi dimulai hingga konfirmasi sukses.
  - Keberhasilan tugas dinyatakan jika seluruh kriteria tugas terpenuhi tanpa intervensi fasilitator.
  - Jumlah pencatatan ulang dihitung berdasarkan entri data berulang yang semestinya dapat digunakan bersama.
- **Penyajian data:** Menyajikan distribusi waktu dan data mentah secara transparan; kesimpulan penelitian dibatasi pada lingkup tugas prototype yang diuji.

## 5. Matriks risiko dan mitigasi

| Risiko teknis / operasional | Tindakan mitigasi |
|---|---|
| Keterlambatan perizinan akses data sekolah | Siapkan dan gunakan data sintetis terstruktur untuk pembangunan dan pengujian awal |
| Ruang lingkup membengkak | Batasi dan bekukan lingkup prototype pada dua skenario utama (Skenario A dan Skenario B) |
| Kendala dependensi C di Windows (`libmagic`, `WeasyPrint`) | Gunakan `python-magic-bin` atau inspeksi bytes murni; siapkan `ReportLab` sebagai alternatif PDF |
| Perbedaan konkurensi SQLite vs PostgreSQL | Terapkan transaksi atomik eksplisit dan verifikasi migrasi pada kedua basis data |
| Riwayat bulk attendance tidak tercatat otomatis | Wajib gunakan utilitas `bulk_create_with_history` di blok transaksi yang sama |
| Angka dashboard usang karena cache | Gunakan `transaction.on_commit` untuk pembersihan cache Redis pasca mutasi |
| Risiko kebocoran berkas permohonan | Simpan berkas di luar folder publik; wajibkan verifikasi peran dan objek pada endpoint unduh |

## 6. Kriteria penyelesaian (Definition of Done)

- Seluruh artefak arsitektur TOGAF (bisnis, data, aplikasi, teknologi) terdokumentasi dan konsisten.
- Seluruh endpoint API kritis memiliki pengujian otomatis (pytest) yang lulus 100%.
- Kedua skenario demonstrasi utama (Kehadiran dan Layanan TU) dapat dijalankan lancar melalui antarmuka peramban.
- Seluruh aturan otorisasi peran dan proteksi data per objek terverifikasi.
- Tidak ada rahasia, kredensial, atau data pribadi siswa yang masuk ke repositori kode.
- Panduan deployment, backup, restore basis data, dan seed data sintetis tersedia lengkap.

## 7. Backlog implementasi terstruktur

| ID | Aktivitas pekerjaan | Ketergantungan | Kriteria keberhasilan |
|---|---|---|---|
| P01 | Perizinan riset dan pemetaan stakeholder | - | Surat izin resmi dan jadwal wawancara disepakati |
| P02 | Analisis kebutuhan lapangan dan proses as-is | P01 | Catatan observasi terkumpul; BPMN as-is selesai |
| P03 | Penentuan prioritas alur dan protokol uji | P02 | Dua skenario uji dan instrumen evaluasi disetujui |
| P04 | Penyusunan blueprint TOGAF ADM | P02, P03 | Artefak arsitektur ditinjau dan divalidasi |
| P05 | Inisialisasi proyek, dependensi, dan linter | P03 | Django Ninja dan React Vite berjalan bersih di lingkungan lokal |
| P06 | Autentikasi JWT, Custom User, dan RBAC | P05 | Endpoint login, refresh, me, dan logout teruji lulus |
| P07 | Implementasi skema data master dan seed sintetis | P04, P06 | Migrasi selesai; siswa, kelas, penempatan, dan guru siap diuji |
| P08 | Modul absensi batch dan histori snapshot | P07 | POST `/attendance/bulk` atomik dan rekapitulasi terverifikasi |
| P09 | Modul kesiswaan dan kronologi penanganan | P08 | Transisi status kasus dan pencatatan event tervalidasi |
| P10 | Modul persuratan tata usaha dan berkas privat | P07 | Alur permohonan persetujuan dan unduh berkas aman teruji |
| P11 | Modul ringkasan dashboard dan ekspor berkas | P08, P09, P10 | Dashboard agregat dan ekspor Excel/PDF cocok dengan basis data |
| P12 | Pembangunan antarmuka frontend terintegrasi | P06-P11 | Seluruh screen (S01-S18) berfungsi terhubung ke backend |
| P13 | Uji internal terintegrasi dan pilot instrumen | P12 | Bug kritis diperbaiki; instrumen uji siap dijalankan |
| P14 | Demonstrasi sistem dan evaluasi pengguna | P13 | Pengambilan data SUS, UAT, dan waktu tugas selesai |
| P15 | Analisis hasil evaluasi dan penyusunan naskah tesis | P14 | Pembahasan hasil, keterbatasan, dan kesimpulan tesis tuntas |

## 8. Rencana matriks pengujian

| Tingkat uji | Lingkup dan fokus | Alat bantu & bukti |
|---|---|---|
| Unit Test | Validasi schema Pydantic, state machine transition, rumus agregat | Pytest, skenario batas |
| Integrasi API | Otorisasi RBAC, object scoping (IDOR), transaksi atomik, unduh privat | Test client Django, assertions status HTTP |
| Komponen UI | Validasi form React Hook Form + Zod, rendering status tabel, aksesibilitas tombol | Vitest, React Testing Library |
| End-to-End | Verifikasi alur penuh dari browser ke database untuk Skenario A dan B | Skenario AFD manual / browser automation |
| Usability & SUS | Pengukuran kemudahan penggunaan dan kepuasan pengguna | Kuesioner SUS 10 butir terstandar |
| Efisiensi tugas | Pengukuran durasi waktu dan jumlah entri ulang data | Stopwatch protokol uji berpasangan |

## 9. Matriks keterlacakan awal

| ID Kebutuhan | Sumber kebutuhan | Modul backend | Endpoint utama | Skenario uji |
|---|---|---|---|---|
| FR-01 | Pengguna dan sesi | `accounts` | `/auth/login`, `/auth/me` | BE-01, BE-02 |
| FR-02 | Data referensi master | `master_data` | `/master/students`, `/master/classes` | Integrasi master |
| FR-03 | Pencatatan kehadiran | `attendance` | `/attendance/bulk`, `/attendance` | BE-03, BE-04, BE-05, E2E-A1 |
| FR-04 | Tindak lanjut kesiswaan | `student_affairs` | `/student-affairs/cases/{id}/transitions` | BE-06, E2E-A2 |
| FR-05 & FR-06 | Layanan TU & berkas privat | `administration` | `/administration/requests`, `/documents/{id}/download` | BE-07, BE-08, E2E-B1, E2E-B2 |
| FR-07 & FR-08 | Dashboard dan ekspor | `reports` | `/reports/dashboard`, `/reports/attendance.xlsx` | BE-09, BE-10, E2E-R1 |
| FR-09 & FR-10 | Audit & paginasi | `core`, seluruh modul | Seluruh endpoint list terpaginasi | BE-05, audit log |

## 10. Prosedur serah terima dan dokumentasi operasional

Dokumentasi akhir prototype mencakup:
- Langkah instalasi dependensi backend dan frontend.
- Berkas template konfigurasi environment (`.env.example`).
- Perintah eksekusi migrasi database dan pemuatan seed data sintetis.
- Akun demo awal untuk keenam peran pengguna (dengan kata sandi aman sementara).
- Prosedur backup dan pemulihan (*disaster recovery*) untuk database dan folder berkas privat.
- Catatan batas performa dan rekomendasi kesiapan infrastruktur sebelum deployment produksi nyata di sekolah.
