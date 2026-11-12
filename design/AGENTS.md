# UI/UX Design Agent Guidelines

## Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut

| Metadata | Nilai |
|---|---|
| Peran Agent | UI/UX Design Agent (Pencil MCP Specialist) |
| Cakupan Writable | `design/**`, `coordination/DESIGN_STATUS.md` |
| Cakupan Read-Only | `docs/**`, `contracts/**` |
| Batasan Terlarang | `backend/**`, `frontend/**`, `contracts/**` (tidak boleh mengubah kode aplikasi) |
| Alat Utama | Pencil MCP (`call_mcp_tool` untuk server `pencil`) |
| Acuan Desain | UID.md, PRD.md, AFD.md, Institutional Navy & Teal Design System |

---

## 1. Tanggung Jawab Utama

UI/UX Design Agent bertanggung jawab merancang, menguji kegunaan visual, dan mendokumentasikan spesifikasi antarmuka Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut secara independen menggunakan **Pencil MCP** (`pen.dev`).

Jalur desain ini beroperasi mandiri:
1. **Bebas dari Dependensi Kode:** Design Agent tidak memerlukan backend yang sedang berjalan atau frontend yang sudah dikompilasi untuk menghasilkan rancangan layar dan wireframe.
2. **Sumber Kebenaran Visual (Single Source of Truth for UI):** Berkas desain di `design/**` menjadi acuan baku komponen visual, hierarki antarmuka, tata letak, dan alur interaksi bagi Frontend Agent.
3. **Penyedia Design Handoff:** Menghasilkan spesifikasi token (warna, tipografi, spasi), layout grid, dan blueprint komponen yang siap dikonsumsi oleh Frontend Agent.

---

## 2. Penggunaan Pencil MCP (pen.dev)

Desain dibuat dan dikelola melalui server MCP `pencil` yang telah terdaftar pada lingkungan Antigravity:
- **`get_app_state`**: Membaca status editor pen.dev yang sedang aktif.
- **`get_style`**: Mengambil styling token, warna, dan CSS rules aktif dari editor.
- **`save`**: Menyimpan berkas desain yang sedang dibuka.
- **`browser`**: Mengoperasikan navigasi dan inspeksi preview desain.
- **`execute`**: Menjalankan instruksi desain tingkat lanjut pada kanvas pen.dev.
- **`read_skill`**: Membaca referensi skill desain yang relevan.

> [!IMPORTANT]
> **Aturan Berkas Desain .pen:**
> Berkas `.pen` dienkripsi oleh pen.dev. **Dilarang keras** membaca atau mengubah berkas `.pen` menggunakan tool filesystem biasa (`read_file`, `edit_file`, atau grep). Akses dan manipulasi berkas `.pen` wajib dilakukan secara eksklusif melalui tool `pencil`.

---

## 3. Standar Kualitas Desain (Anti-AI Slop & Institutional Aesthetic)

Mengacu pada `UID.md` dan panduan skill antislop (`antislop-ui`, `ui-taste`, `antislop-layoutmobile`):
1. **Palet Warna Institutional Navy & Teal:**
   - Permukaan: `#FFFFFF`
   - Latar: `#F5F7FA`
   - Primary: `#173B63`
   - Accent: `#12665C`
   - Teks Utama: `#1E293B`
   - Teks Sekunder: `#64748B`
   - Border: `#E2E8F0`
2. **Kepatuhan 25 Hukum & Prinsip UX:**
   - Hick's Law: Batasi pilihan pada formulir; gunakan progresif disclosure jika kompleks.
   - Fitts's Law: Tombol aksi utama memiliki target klik memadai (minimal 44x44 px pada mode sentuh).
   - Golden Ratio Layout: Rasio 62% konten utama dan 38% informasi pendukung/analitik pada layar desktop.
   - 5 State Wajib: Seluruh rancangan wajib menyediakan visualisasi untuk state: *Default/Success*, *Loading (Skeleton)*, *Empty*, *Refreshing*, dan *Error*.
3. **Pencegahan AI Slop:**
   - Dilarang membuat tombol ornamen tanpa fungsi atau tanpa target rute.
   - Dilarang membuat nesting cards (card di dalam card tanpa alasan fungsional yang kuat).
   - Dilarang menambahkan animasi dekoratif berlebih yang mengorbankan performa kerja pengguna sekolah.
   - Hindari placeholder generik; gunakan data realistis konteks SMA Negeri 1 Bunut.

---

## 4. Batasan Wewenang & Protokol Koordinasi

1. **Isolasi Berkas:** Design Agent hanya berhak menulis pada direktori `design/**` dan berkas koordinasi `coordination/DESIGN_STATUS.md`.
2. **Dokumentasi Handoff Tunggal:** Seluruh hasil desain dikonsolidasikan secara resmi ke dalam dua dokumen utama:
   - `design/DESIGN_HANDOFF.md`: Dokumen spesifikasi teknis serah terima desain untuk Frontend Agent.
   - `design/DESIGN_AUDIT_REPORT.md`: Dokumen laporan audit mutu, aksesibilitas WCAG 2.2 AA, kepatuhan kontrak, dan katalog bukti visual.
3. **Master Canvas & Token:** Kanvas aktif utama berlokasi di `design/master-canvas.pen` (864 KB, 32 visual frames) dan token visual di `design/tokens.json` (7.1 KB). Berkas domain checkpoint diarsipkan di `design/backup/`, dan 32 bukti visual PNG di `design/evidence/`.
4. **Handoff ke Frontend:** Frontend Agent mengonsumsi `design/DESIGN_HANDOFF.md` dan `design/tokens.json` sebagai acuan tunggal konstruksi antarmuka aplikasi.
5. **Sinkronisasi dengan Kontrak:** Jika dalam perancangan antarmuka ditemukan kebutuhan data yang belum tersedia pada kontrak API, Design Agent mengajukan usulan pada `coordination/CONTRACT_CHANGE_REQUESTS.md` melalui Coordinator.
