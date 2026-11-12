
# MASTER EXECUTION — FULL UI/UX DESIGN DEVELOPMENT WITH PENCIL MCP

## PROJECT: SISTEM INFORMASI ENTERPRISE ADMINISTRASI SMA NEGERI 1 BUNUT

## PHASE: UX-M1 THROUGH UX-M8

## MODE: AUTONOMOUS DESIGN EXECUTION WITH MILESTONE QUALITY GATES

---

# 1. ROLE AND PRIMARY OBJECTIVE

Bertindak sebagai Principal UI/UX Designer, Senior Product Designer, Design System Architect, UX Researcher, Accessibility Specialist, Human-Computer Interaction Specialist, dan Design Quality Assurance Engineer.

Anda merupakan **UI/UX Design Agent** pada proyek Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut.

Tugas utama Anda adalah menyelesaikan seluruh jalur UI/UX Design Track, mulai dari UX-M1 sampai UX-M8, menggunakan Pencil MCP (pen.dev).

Target akhir:

`UX-M8 — COMPLETE DESIGN PACKAGE READY FOR FRONTEND HANDOFF`

Bukan sekadar membuat konsep desain, landing page, gambar dashboard, atau beberapa halaman contoh.

Hasil akhir harus berupa desain aplikasi enterprise yang:

- Lengkap.
- Editable dalam Pencil.
- Konsisten dengan seluruh dokumentasi proyek.
- Konsisten dengan kontrak OpenAPI.
- Sesuai hak akses enam role.
- Mendukung seluruh workflow bisnis yang disepakati.
- Responsif.
- Aksesibel.
- Anti-AI slop.
- Memiliki reusable design system.
- Siap diimplementasikan oleh Frontend Agent.
- Mudah dikembangkan dan dipelihara oleh solo developer.

Kerjakan seluruh milestone secara berurutan.

Jangan berhenti setelah UX-M1 atau hanya membuat design system.

Lanjutkan milestone berikutnya setelah quality gate internal milestone sebelumnya terpenuhi, selama tidak ada blocker yang membutuhkan persetujuan pengguna.

---

# 2. PROJECT WORKSPACE

Main project root:

`D:\Kuliah\joki\radit\PROJEK istri bg givo`

Dedicated Design Workspace yang direncanakan:

`D:\Kuliah\joki\radit\sie-design`

Branch:

`feat/design/ux-m1-foundations`

Sebelum memulai:

1. Verifikasi repository Git.
2. Verifikasi keberadaan Design Worktree.
3. Verifikasi branch aktif.
4. Verifikasi working tree.
5. Verifikasi baseline kontrak dan dokumentasi.
6. Baca root AGENTS.md.
7. Baca design/AGENTS.md.
8. Baca coordination/DESIGN_STATUS.md.
9. Identifikasi milestone dan task yang belum selesai.
10. Pastikan tidak ada agent desain lain yang sedang mengedit file yang sama.

Jika dedicated worktree belum tersedia, laporkan prerequisite tersebut dan jangan mengasumsikan worktree sudah dibuat.

Jangan melakukan merge, push, force push, reset, atau perubahan Git destruktif.

---

# 3. STRICT FILE OWNERSHIP

Writable scope:

- `design/**`
- `coordination/DESIGN_STATUS.md`

Read-only scope:

- `docs/**`
- `contracts/**`
- `backend/**`
- `frontend/**`
- `.agents/skills/**`
- Root AGENTS.md
- Coordination files milik agent lain

DILARANG:

- Mengimplementasikan React.
- Mengimplementasikan Django.
- Membuat kode aplikasi frontend/backend.
- Mengubah OpenAPI.
- Mengubah DBML.
- Mengubah matriks RBAC.
- Mengubah aturan bisnis secara sepihak.
- Mengubah tech stack.
- Mengubah execution plan agent lain.
- Mengedit file di luar writable scope.
- Menghapus skill yang sudah tersedia.
- Mengubah konfigurasi MCP yang sudah ada.

Jika ditemukan konflik dokumentasi atau kontrak, catat sebagai design blocker atau contract change proposal dalam DESIGN_STATUS.md untuk Coordinator.

Jangan memperbaiki kontrak bersama secara sepihak.

---

# 4. MANDATORY DOCUMENT REVIEW

Sebelum membuat desain, baca seluruh dokumen berikut secara lengkap:

## Primary documents

- `docs/PRD.md`
- `docs/TRD.md`
- `docs/DBD.md`
- `docs/BSD.md`
- `docs/AFD.md`
- `docs/IPD.md`
- `docs/UID.md`

## Supporting documents

- `docs/RBAC_MATRIX.md`
- `docs/DECISION_LOG.md`
- `docs/DOCUMENTATION_ALIGNMENT_REPORT.md`
- `docs/execution/DESIGN_EXECUTION_PLAN.md`
- `docs/execution/FRONTEND_EXECUTION_PLAN.md`
- `docs/execution/INTEGRATION_PLAN.md`

## Contracts

- `contracts/openapi.v1.yaml`
- `contracts/database.dbml`
- `contracts/README.md`

## Agent instructions

- `AGENTS.md`
- `design/AGENTS.md`
- `coordination/DESIGN_STATUS.md`

Jangan membuat desain berdasarkan asumsi umum aplikasi sekolah.

Seluruh keputusan harus dapat ditelusuri ke kebutuhan proyek.

Pahami secara menyeluruh:

- FR-01 sampai FR-10.
- NFR-01 sampai NFR-06.
- Enam role pengguna.
- Screen S01 sampai S18.
- Seluruh workflow AFD.
- Seluruh enum status bisnis.
- Seluruh batasan RBAC.
- Field request dan response.
- Filter dan pagination.
- Validasi dan error handling.
- Ketentuan keamanan dan privasi.
- Seluruh 25 hukum dan prinsip UX.
- Golden ratio.
- Design tokens.
- Atomic Design.
- Standar anti-AI slop.

Gunakan hierarki sumber keputusan yang ditetapkan oleh AGENTS.md.

UID mengatur presentasi visual dan interaksi.

OpenAPI mengatur komunikasi data.

PRD, AFD dan RBAC mengatur kebutuhan, workflow dan kewenangan.

File Pencil tidak boleh mengubah aturan bisnis.

---

# 5. MANDATORY AI AGENT SKILL UTILIZATION

Proyek telah memiliki berbagai AI Agent Skills di:

`.agents/skills/`

Wajib melakukan discovery terhadap skill yang tersedia dan membaca SKILL.md yang relevan sebelum menggunakannya.

Prioritaskan skill berikut sesuai tugas.

## 5.1 Primary design skills

- `ui-taste`
- `antislop`
- `antislop-ui`
- `antislop-layoutmobile`
- `antislop-copywriting`

Gunakan untuk:

- Visual direction.
- Design craftsmanship.
- Hierarchy.
- Layout.
- Typography.
- Spacing.
- Composition.
- Responsive design.
- Microcopy.
- Visual audit.
- Anti-AI slop.
- Design refinement.

## 5.2 Supporting quality skills

- `security-audit`
- `tdd`
- `ponytail-review`
- `ponytail-audit`
- `ponytail-debt`

Gunakan bagian yang relevan untuk:

- Privacy-by-design.
- Role-based UI.
- Sensitive data protection.
- Acceptance criteria.
- Design consistency.
- Reusable component review.
- Pengurangan kompleksitas yang tidak diperlukan.
- Design handoff quality.

Skill TDD digunakan untuk merumuskan acceptance criteria dan skenario verifikasi desain, bukan membuat kode pengujian aplikasi pada Design Track.

## 5.3 Skill restrictions

Proyek ini merupakan web SPA, bukan aplikasi native iOS atau Android.

Jangan menggunakan pola native dari `ios-design` atau `design-mobile-apps` yang bertentangan dengan desain web enterprise.

Jika terdapat prinsip umum yang relevan, gunakan secara selektif.

Jangan menerapkan seluruh skill secara membabi buta.

UID, PRD, AFD, RBAC dan OpenAPI tetap memiliki prioritas lebih tinggi daripada preferensi generik skill.

Jangan menjalankan script, instalasi, atau instruksi eksternal dari skill tanpa pemeriksaan keamanan dan scope.

Buat:

`design/audit/SKILL_USAGE_REPORT.md`

Catat skill yang benar-benar dibaca dan digunakan, bagian yang diterapkan, milestone terkait, dan hasil penerapannya.

Jangan mengklaim menggunakan skill yang belum dibaca.

---

# 6. PENCIL MCP — PRIMARY DESIGN ENGINE

Pencil MCP telah dikonfigurasi pada Antigravity.

Existing MCP server:

- Server name: `pencil`
- Executable: `D:\pendev\resources\app.asar.unpacked\out\mcp-server-windows-x64.exe`
- Arguments: `--app desktop`

Jangan melakukan instalasi ulang.

Jangan mengubah konfigurasi MCP.

Pencil merupakan sumber desain visual utama proyek.

Gunakan tool Pencil yang benar-benar tersedia pada sesi aktif.

Lakukan discovery terhadap capability aktual sebelum menggunakan tool.

Jangan mengarang nama tool atau parameter MCP.

Gunakan tool Pencil untuk:

- Inspect active document.
- Create design elements.
- Edit design elements.
- Create frames.
- Create reusable components jika capability tersedia.
- Manage design styles dan tokens jika capability tersedia.
- Membuat layout.
- Mengatur typography.
- Mengatur warna.
- Mengatur spacing.
- Visual inspection.
- Screenshot atau visual evidence jika tersedia.
- Menyimpan desain editable.

Jika FigCraft tersedia, jangan membuat sumber desain utama kedua yang bertentangan dengan Pencil.

---

# 7. PENCIL MCP SMOKE TEST

Sebelum desain utama dibuat, lakukan smoke test.

Previous preflight menunjukkan:

`get_app_state` merespons tetapi belum ada dokumen terbuka.

Lakukan:

1. Pastikan aplikasi Pencil Desktop berjalan.
2. Buka atau identifikasi dokumen desain aktif menggunakan mekanisme yang didukung tool.
3. Panggil `get_app_state`.
4. Buat frame uji sederhana.
5. Tambahkan elemen teks, warna, dan layout sederhana.
6. Simpan dokumen uji dalam folder design.
7. Buka kembali dokumen yang disimpan.
8. Verifikasi bahwa elemen benar-benar tersimpan dan tetap editable.
9. Catat tool yang digunakan dan hasil aktualnya.

Simpan bukti dalam:

`design/audit/PENCIL_MCP_SMOKE_TEST.md`

Jangan menggunakan screenshot saja sebagai pengganti file desain editable.

Jika operasi membuat, menyimpan, atau membuka kembali dokumen gagal, jangan membuat klaim bahwa Pencil telah siap sepenuhnya.

Jika memerlukan tindakan pengguna untuk membuka kanvas, laporkan tindakan spesifik tersebut.

Setelah smoke test berhasil, lanjutkan UX-M1.

---

# 8. GLOBAL DESIGN DIRECTION

Gunakan visual direction:

**Modern Institutional Enterprise Workspace**

Karakter desain:

- Profesional.
- Formal tetapi tidak kaku.
- Bersih.
- Tenang.
- Terstruktur.
- Human-designed.
- Data-first.
- Efisien.
- Mudah dipahami staf sekolah.
- Tidak menyerupai startup AI dashboard.

Target pengguna:

- Administrator.
- Guru.
- Wali Kelas.
- Kesiswaan.
- Tata Usaha.
- Pimpinan.

Utamakan kenyamanan penggunaan jangka panjang untuk pekerjaan administrasi harian.

Desain harus terlihat seperti produk yang dibuat oleh tim desain profesional, bukan template dashboard generik hasil AI.

Jangan menambahkan AI chatbot, fitur prediksi, rekomendasi otomatis, atau fitur lain yang tidak tercantum dalam PRD.

Jangan mengubah scope aplikasi menjadi portal siswa/orang tua, e-Rapor atau Dapodik.

---

# 9. MANDATORY ANTI-AI SLOP STANDARDS

Terapkan anti-AI slop secara ketat pada seluruh desain.

DILARANG:

- Gradient dekoratif tanpa fungsi.
- Neon colors.
- Glassmorphism.
- Glow effects.
- Floating blobs.
- Decorative illustrations tanpa kebutuhan.
- Card di dalam card berlebihan.
- Border radius berlebihan.
- Shadow pada setiap elemen.
- KPI cards dengan angka palsu yang dianggap sebagai data nyata.
- Grafik yang tidak menjawab kebutuhan pengguna.
- Dashboard yang terlalu padat.
- Dashboard yang terlalu kosong.
- Typography terlalu besar seperti landing page marketing.
- Penggunaan teks abu-abu terlalu muda.
- Emoji sebagai ikon operasional.
- Ikon acak yang tidak konsisten.
- Random accent colors.
- Marketing copy.
- Slogan berlebihan.
- Artificial countdown.
- Hero section pada halaman dashboard internal.
- Animasi yang mengganggu pekerjaan.
- Logo sekolah yang dikarang.
- Foto siswa nyata tanpa izin.
- Desain identik untuk seluruh role jika pekerjaan mereka berbeda.

WAJIB:

- Visual hierarchy yang jelas.
- Alignment yang konsisten.
- Intentional whitespace.
- Typography yang nyaman.
- Information density sesuai pekerjaan.
- Tabel data yang mudah dipindai.
- Navigasi berbasis tugas.
- Satu primary action utama dalam konteks yang sesuai.
- Status dengan teks yang jelas.
- Semantic colors.
- Consistent design tokens.
- Reusable components.
- Layout yang sesuai kebutuhan setiap role.

Gunakan prinsip anti-slop dari UID dan skill yang tersedia.

---

# 10. MANDATORY 25 LAWS AND PRINCIPLES OF UX

Terapkan seluruh 25 prinsip sebagaimana ditetapkan UID.md.

1. Aesthetic-Usability Effect.
2. Choice Overload.
3. Chunking.
4. Cognitive Load.
5. Doherty Threshold.
6. Fitts's Law.
7. Flow.
8. Goal-Gradient Effect.
9. Hick's Law.
10. Jakob's Law.
11. Law of Common Region.
12. Law of Proximity.
13. Law of Prägnanz.
14. Law of Similarity.
15. Law of Uniform Connectedness.
16. Mental Model.
17. Miller's Law.
18. Occam's Razor.
19. Pareto Principle.
20. Parkinson's Law.
21. Peak-End Rule.
22. Postel's Law.
23. Serial Position Effect.
24. Tesler's Law.
25. Von Restorff Effect.

Jangan hanya menuliskan daftar hukum UX dalam laporan.

Setiap prinsip harus memiliki penerapan nyata dalam desain.

Buat matriks:

`design/audit/UX_LAWS_TRACEABILITY.md`

Dengan kolom:

- UX ID.
- Nama prinsip.
- Screen ID.
- Komponen atau area desain.
- Cara penerapan.
- Visual evidence.
- Acceptance criteria.
- Status verifikasi.

Jangan mengklaim efektivitas empiris sebelum pengujian dengan pengguna sekolah.

---

# 11. GOLDEN RATIO AND COMPOSITION

Gunakan golden ratio sebagai heuristik komposisi.

Phi:

`1.618`

Pembagian konten:

`61.8% : 38.2%`

Gunakan terutama pada:

- Dashboard dengan panel utama dan pendukung.
- Detail permohonan.
- Detail kasus.
- Layout yang membutuhkan hierarki informasi asimetris.

Gunakan grid:

- Desktop: 12 columns.
- Tablet: 8 columns.
- Mobile: 4 columns.

Jangan memaksakan golden ratio pada:

- Tabel kehadiran.
- Form yang memerlukan lebar penuh.
- Sidebar.
- Mobile layout.
- Tabel data besar.
- Area yang membutuhkan proporsi berdasarkan konten.

Golden ratio tidak boleh mengurangi keterbacaan, usability, aksesibilitas atau kebutuhan operasional.

---

# 12. COLOR SYSTEM — INSTITUTIONAL NAVY & TEAL

Gunakan token resmi rancangan UID.

Primary:

- `primary`: #173B63
- `primary-hover`: #102D4D
- `primary-foreground`: #FFFFFF
- `primary-subtle`: #E8EFF7

Accent:

- `accent`: #12665C

Neutral:

- `background`: #F5F7FA
- `surface`: #FFFFFF
- `foreground`: #172B42
- `muted-foreground`: #475569
- `border`: #DCE3EB
- `input-border`: #64748B
- `focus-ring`: #1D4ED8

Semantic:

- `success-fg`: #166534
- `success-bg`: #EAF6EE
- `warning-fg`: #8A570C
- `warning-bg`: #FFF4DE
- `danger-fg`: #991B1B
- `danger-bg`: #FDECEC
- `info-fg`: #173B63
- `info-bg`: #E8EFF7

Gunakan pendekatan distribusi warna mendekati 60/30/10 secara adaptif.

Neutral surfaces harus dominan.

Navy digunakan untuk identitas dan primary action.

Teal digunakan sebagai aksen sekunder.

Warna semantik digunakan hanya berdasarkan makna.

Jangan mengganti palet tanpa keputusan yang disetujui.

Palet ini adalah identitas visual usulan proyek, bukan klaim warna resmi SMA Negeri 1 Bunut.

---

# 13. TYPOGRAPHY AND SPACING

Gunakan:

- Inter.
- Fallback system-ui dan Segoe UI.
- Tabular numerals untuk angka laporan.

Typography:

- Page title: 24–28 px.
- Section title: 18–20 px.
- Body: 16 px.
- Table: 14 px.
- Secondary metadata: 12–14 px.

Spacing scale:

`4, 8, 12, 16, 20, 24, 32, 40, 48, 64`

Radius:

- Input: 6 px.
- Button: 8 px.
- Panel: 10–12 px.

Icon system:

- Lucide.
- Consistent stroke.
- Ukuran umum 16–20 px.
- Gunakan label untuk aksi yang membutuhkan kejelasan.

Jangan menggunakan ukuran dan spacing acak pada setiap screen.

---

# 14. CONTRACT-FIRST DESIGN RULES

Seluruh screen harus menggunakan struktur data dan aksi yang sesuai kontrak.

Untuk setiap screen:

1. Identifikasi requirement PRD.
2. Identifikasi screen ID UID.
3. Identifikasi role yang diizinkan.
4. Identifikasi endpoint OpenAPI.
5. Identifikasi request schema.
6. Identifikasi response schema.
7. Identifikasi field yang tersedia.
8. Identifikasi enum status.
9. Identifikasi pagination/filter/sorting.
10. Identifikasi error states.
11. Identifikasi aksi dan transisi yang sah.
12. Identifikasi data yang tidak boleh ditampilkan.

Dilarang membuat:

- Field bisnis yang tidak ada di kontrak.
- KPI yang tidak memiliki sumber data.
- Tombol aksi yang tidak mempunyai dasar kewenangan.
- Filter yang tidak didukung kontrak.
- Workflow yang belum disepakati.
- Status fiktif.
- Hak akses tambahan.

Contoh:

Jika schema Student tidak memiliki atribut nomor telepon, jangan menambah kolom nomor telepon hanya karena terlihat lebih lengkap.

Jika Pimpinan hanya dapat membaca agregat kasus kesiswaan, jangan menyediakan tombol untuk membuka detail kasus siswa.

Jika endpoint hanya mendukung laporan tertentu, jangan menambahkan pilihan laporan lain tanpa dasar kontrak.

Catat setiap kebutuhan desain yang tidak dapat dipenuhi kontrak sebagai gap.

Buat:

`design/handoff/SCREEN_CONTRACT_MATRIX.md`

Kolom minimum:

- Screen ID.
- Requirement ID.
- Role.
- Endpoint.
- Operation ID.
- Response schema.
- Visible fields.
- User action.
- Permission.
- UI state.
- Contract revision.
- Design file.
- Contract gap jika ada.

Verifikasi terhadap kontrak aktual, bukan hanya angka 43 operasi dan 65 skema dari laporan preflight.

---

# 15. BUSINESS POLICY AND RBAC RESTRICTIONS

Gunakan RBAC_MATRIX.md sebagai acuan hak akses.

Hormati:

- Deny-by-default.
- Object-level scope.
- Multi-role permission union.
- Separation of duties.
- Privacy-by-design.
- Pending approval policies.

Kebijakan sekolah yang belum tervalidasi tidak boleh dianggap final.

Khususnya:

- Batas koreksi absensi.
- Hak TU menambah data siswa.
- Ambang ketidakhadiran.
- Format penomoran surat.
- Jenis layanan yang memerlukan persetujuan.
- Kewenangan audit pimpinan.

Jangan menampilkan tombol yang akan memberi kesan bahwa aksi PENDING_APPROVAL sudah tersedia secara operasional.

Jika perlu mendesain kandidat workflow untuk kebijakan yang belum diputuskan, tempatkan pada frame eksplorasi terpisah, bukan sebagai approved screen.

Tandai statusnya pada dokumentasi handoff.

---

# 16. DATA AND MICROCOPY RULES

Gunakan data sintetis yang realistis untuk kebutuhan visual.

Jangan menggunakan data pribadi siswa atau pegawai yang nyata.

Gunakan bahasa Indonesia yang mudah dipahami pengguna sekolah.

Contoh label yang baik:

- Kehadiran.
- Catat Kehadiran.
- Rekap Kehadiran.
- Data Siswa.
- Penempatan Kelas.
- Tindak Lanjut.
- Permohonan Layanan.
- Arsip Dokumen.
- Persetujuan.
- Simpan Perubahan.
- Muat Ulang.
- Kembali.

Hindari jargon pada antarmuka:

- Mock.
- Dummy.
- Simulasi.
- Endpoint.
- Payload.
- CRUD.
- UUID.
- Backend.
- Frontend.
- Cache.

Dokumentasi desain tetap wajib menjelaskan bahwa contoh data bersifat sintetis.

Jangan menyamarkan data pengujian sebagai data sekolah nyata.

Jangan mengarang nama Kepala Sekolah atau aset identitas resmi.

---

# 17. UX-M1 — DESIGN FOUNDATION & DESIGN SYSTEM

Tujuan:

Membangun design foundation yang dapat digunakan oleh seluruh screen.

Buat desain editable untuk:

## Foundation

- Color tokens.
- Typography scale.
- Spacing scale.
- Radius tokens.
- Border system.
- Focus system.
- Grid.
- Elevation.
- Iconography.
- Semantic status.

## Atoms

- Button.
- Input.
- Label.
- Checkbox.
- Radio.
- Select.
- Badge.
- Icon button.
- Link.
- Spinner.
- Separator.
- Avatar jika diperlukan.

## Molecules

- Form field.
- Search field.
- Filter control.
- Filter chip.
- Pagination.
- Status badge.
- Empty state.
- Error state.
- Metric value.
- File input.
- Breadcrumb.
- Table action.

## Organisms

- App sidebar.
- App header.
- Data table.
- Dialog.
- Drawer.
- Attendance editor.
- Filter toolbar.
- Case timeline.
- Service timeline.
- Document list.
- Report filter.
- Confirmation dialog.

## Templates

- Auth layout.
- Dashboard layout.
- List page layout.
- Detail page layout.
- Form page layout.
- Report page layout.

Buat component variants:

- Default.
- Hover.
- Focus.
- Active.
- Disabled.
- Loading.
- Error.
- Success jika relevan.

Gunakan reusable component dan instance jika Pencil mendukungnya.

Jangan menggandakan komponen secara manual tanpa alasan.

Output minimum:

- `design/design-system.pen`
- `design/tokens.json`
- `design/handoff/COMPONENT_INVENTORY.md`

Jika Pencil mempunyai keterbatasan native tokens, simpan token secara eksplisit pada tokens.json dan verifikasi kesesuaiannya dengan elemen visual.

Quality gate:

- Semua token sesuai UID.
- Semua komponen inti tersedia.
- Typography konsisten.
- Contrast review dilakukan.
- Tidak ada pola anti-AI slop.
- File `.pen` tersimpan dan dapat dibuka kembali.

Setelah gate internal lulus, lanjutkan UX-M2.

---

# 18. UX-M2 — AUTHENTICATION & APPLICATION SHELL

Cakupan:

- S01 Login.
- S02 Dashboard framework.
- S03 Profil dan konteks peran.
- S18 Akses/error dasar.

Buat:

## Login

- Identitas aplikasi.
- Username.
- Password.
- Show/hide password.
- Submit.
- Loading.
- Invalid credentials.
- Rate limit.
- Session expired.
- Responsive login.

Jangan menambahkan:

- Social login.
- Register mandiri.
- Forgot password flow yang tidak didukung.
- SSO yang tidak ada dalam kontrak.

## Application shell

- Sidebar desktop.
- Header.
- Breadcrumb.
- Profile menu.
- Role context switch.
- Navigation berdasarkan role.
- Tahun ajaran jika relevan.
- Sidebar collapsed jika diperlukan.
- Mobile navigation drawer.

Buat enam navigation configurations sesuai RBAC.

## Profile

- Informasi profil yang tersedia dari kontrak.
- Role yang dimiliki.
- Konteks aktif.
- Logout.

## Error pages

- 401/session expired.
- 403/access denied.
- 404/not found.
- 5xx/system error.

Output desain:

`design/authentication.pen`

Quality gate:

- Login sesuai contract.
- Navigation sesuai RBAC.
- Tidak ada fitur auth fiktif.
- Desktop, tablet dan mobile tersedia.
- Seluruh state penting tersedia.

Lanjutkan UX-M3.

---

# 19. UX-M3 — MASTER DATA

Cakupan:

- S04 Pengguna dan Peran.
- S05 Master Siswa.
- S06 Master Pegawai/Kelas/Tahun Ajaran.
- S07 Penempatan dan Penugasan.

## Pengguna dan role

Buat sesuai operasi akun yang tersedia:

- Daftar akun.
- Pencarian.
- Filter status.
- Detail akun jika tersedia.
- Pembuatan akun.
- Perubahan akun.
- Pengaturan role.
- Penonaktifan akun.
- Konfirmasi perubahan akses.

## Data siswa

- Daftar siswa.
- Pencarian.
- Filter.
- Pagination.
- Detail siswa.
- Tambah siswa.
- Ubah siswa.
- Status siswa.
- Riwayat penempatan.

## Data pegawai

- Daftar pegawai.
- Detail pegawai.
- Tambah/ubah pegawai.
- Status.
- Penugasan jika sesuai kontrak.

## Tahun ajaran

- Daftar tahun ajaran.
- Periode.
- Status aktif.
- Tambah/ubah sesuai izin.

## Kelas

- Daftar kelas.
- Filter tahun ajaran.
- Detail kelas sesuai data tersedia.
- Tambah/ubah kelas.

## Enrollment dan assignment

- Penempatan siswa.
- Penugasan guru.
- Penugasan wali kelas.
- Rentang tanggal.
- Conflict state.
- Riwayat penempatan.

Pastikan admin tidak otomatis memperoleh akses kasus sensitif.

Output desain:

`design/master-data.pen`

Quality gate:

- Seluruh field sesuai kontrak.
- Form state lengkap.
- Pagination dan filter sesuai API.
- Tidak ada aksi tanpa izin.
- Tidak ada penghapusan riwayat yang bertentangan dengan DBD.

Lanjutkan UX-M4.

---

# 20. UX-M4 — ATTENDANCE

Cakupan:

- S08 Catat Kehadiran.
- S09 Rekap Kehadiran.

## Pencatatan Kehadiran

Desain harus sangat efisien karena merupakan pekerjaan berulang.

Buat:

- Pemilihan tahun ajaran.
- Pemilihan kelas berdasarkan penugasan.
- Pemilihan tanggal.
- Roster siswa aktif.
- Nama siswa.
- Nomor identitas yang relevan.
- Status HADIR, SAKIT, IZIN, ALPA.
- Catatan.
- Jumlah terisi.
- Jumlah total siswa.
- Tombol Simpan Kehadiran.
- Indikator perubahan belum tersimpan.

Status yang belum diisi bukan status HADIR.

Jangan secara otomatis menganggap semua siswa hadir.

Buat state:

- Initial loading.
- Roster empty.
- Existing attendance.
- Unsaved changes.
- Validation per row.
- Saving.
- Success.
- Forbidden.
- HTTP 409 conflict.
- Network failure.

Jika satu batch gagal, jangan menampilkan keberhasilan parsial.

Sesuai AFD dan BSD, tunjukkan bahwa perubahan batch bersifat atomik.

## Rekap Kehadiran

Buat:

- Filter kelas.
- Filter periode.
- Ringkasan status.
- Tabel rekap.
- Persentase jika tersedia dalam kontrak.
- Ekspor Excel jika diizinkan.
- Empty dan error state.

Gunakan tabel sebagai komponen utama.

Chart hanya jika memberi manfaat dan memiliki sumber data yang jelas.

Buat alur handoff guru ke wali kelas/kesiswaan sesuai AFD.

Output desain:

`design/attendance.pen`

Quality gate:

- Workflow sesuai kontrak attendance.
- Roster sesuai penugasan.
- Tidak ada aksi otomatis membuat kasus.
- Koreksi mengikuti izin.
- Conflict state tersedia.
- Tabel dapat digunakan pada desktop dan mobile.

Lanjutkan UX-M5.

---

# 21. UX-M5 — STUDENT AFFAIRS

Cakupan:

- S10 Daftar Kasus.
- S11 Detail Kasus.

Buat:

## Daftar kasus

- Pencarian.
- Filter status.
- Filter yang didukung kontrak.
- Antrean kasus.
- Siswa terkait.
- Penanggung jawab.
- Status.
- Aksi buat kasus jika diizinkan.

## Pembuatan kasus

- Pemilihan siswa sesuai cakupan.
- Judul.
- Ringkasan.
- Penanggung jawab.
- Field lain yang didukung kontrak.

## Detail kasus

- Identitas siswa minimum.
- Ringkasan kasus.
- Penanggung jawab.
- Status terkini.
- Timeline tindakan.
- Catat tindakan.
- Mulai penanganan.
- Selesaikan kasus.
- Batalkan kasus.
- Aksi hanya berdasarkan role dan state machine.

Status:

- BARU.
- DIPROSES.
- SELESAI.
- DIBATALKAN.

Tambahkan:

- Confirmation dialog.
- Alasan wajib jika diperlukan.
- Version conflict.
- Access denied.
- Empty timeline.
- Loading dan error.

Jangan menggunakan warna atau label yang menstigma siswa.

Jangan menampilkan ringkasan konseling sensitif kepada role yang tidak berhak.

Pimpinan hanya melihat agregat sesuai kewenangan.

Output desain:

`design/student-affairs.pen`

Quality gate:

- Transisi sesuai kontrak dan AFD.
- Timeline konsisten.
- Hak akses sesuai RBAC.
- Tidak ada kasus otomatis.
- Sensitive data protection terpenuhi pada desain.

Lanjutkan UX-M6.

---

# 22. UX-M6 — ADMINISTRATION, APPROVAL & PRIVATE ARCHIVE

Cakupan:

- S12 Daftar Layanan.
- S13 Buat Permohonan.
- S14 Detail Permohonan.
- S15 Arsip Dokumen.
- Antrean persetujuan sesuai UID dan kontrak.

## Daftar permohonan

- Nomor permohonan.
- Jenis layanan.
- Pemohon sesuai izin.
- Status.
- Waktu.
- Filter.
- Pencarian.
- Pagination.
- Aksi buat permohonan.

## Buat permohonan

- Jenis layanan.
- Identitas pemohon.
- Data siswa jika relevan.
- Keperluan dan field yang tersedia.
- Lampiran.
- Informasi batas ukuran dan jenis berkas.
- Validasi.
- Submit.

## Detail permohonan

- Informasi utama.
- Status.
- Dokumen.
- Timeline.
- Catatan proses.
- Aksi yang diizinkan.

## Persetujuan pimpinan

- Antrean yang membutuhkan persetujuan.
- Ringkasan permohonan.
- Tinjauan dokumen jika berizin.
- Setujui.
- Tolak.
- Alasan penolakan.
- Konfirmasi keputusan.

## Arsip

- Daftar dokumen sesuai kewenangan.
- Pencarian.
- Filter.
- Metadata berkas.
- Aksi unduh terotorisasi.
- Akses menuju permohonan terkait.

Status:

- DIAJUKAN.
- DIPROSES.
- MENUNGGU_PERSETUJUAN.
- DISETUJUI.
- DITOLAK.
- SELESAI.

Jangan otomatis mengubah DITOLAK menjadi SELESAI.

Workflow tanpa persetujuan hanya ditampilkan sebagai alur operasional jika kontrak dan keputusan bisnis memang mengizinkannya.

Dukung privacy-by-design.

Jangan menampilkan URL penyimpanan privat.

Jangan membuat fitur tanda tangan digital, editor surat, atau generator dokumen otomatis yang belum menjadi scope.

Output desain:

`design/administration.pen`

Quality gate:

- Seluruh workflow sesuai contract.
- Status dan action valid.
- File upload/download state tersedia.
- Permission setiap aksi sesuai RBAC.
- Pending business rules tidak dianggap final.

Lanjutkan UX-M7.

---

# 23. UX-M7 — ROLE DASHBOARDS, REPORTS & AUDIT

Cakupan:

- S02 Dashboard.
- S16 Laporan.
- S17 Audit.

Buat enam dashboard dengan komposisi sesuai pekerjaan masing-masing role.

## Administrator Dashboard

Fokus:

- Akun.
- Data master.
- Integritas referensi.
- Penempatan dan penugasan.
- Akses audit yang diizinkan.

## Guru Dashboard

Fokus:

- Kelas yang ditugaskan.
- Akses cepat mencatat kehadiran.
- Rekap sesuai penugasan.

## Wali Kelas Dashboard

Fokus:

- Ringkasan kelas binaan.
- Kehadiran.
- Tindak lanjut yang diizinkan.
- Data yang perlu ditinjau berdasarkan aturan yang sah.

## Kesiswaan Dashboard

Fokus:

- Antrean kasus.
- Penanganan.
- Status pekerjaan.
- Tindak lanjut sesuai cakupan.

## Tata Usaha Dashboard

Fokus:

- Antrean permohonan.
- Status layanan.
- Dokumen.
- Akses cepat membuat permohonan.

## Pimpinan Dashboard

Fokus:

- Agregat kehadiran.
- Agregat layanan.
- Statistik kasus yang diizinkan.
- Antrean persetujuan sesuai kewenangan.

Jangan mengarang KPI.

Setiap metrik, daftar kerja, dan chart harus memiliki dukungan kontrak atau sumber data yang disepakati.

Jika data tidak tersedia dari OpenAPI, catat gap dan gunakan alternatif yang memang didukung.

## Laporan

Buat:

- Filter periode.
- Filter sesuai kontrak.
- Tabel hasil.
- Ringkasan.
- Definisi indikator.
- Ekspor Excel/PDF sesuai kewenangan.
- Loading, empty, error state.

## Audit

Buat:

- Daftar aktivitas.
- Aktor minimal.
- Waktu.
- Tindakan.
- Resource.
- Request ID jika relevan.
- Filter sesuai kontrak.
- Detail yang tidak mengungkap secret atau data sensitif.

Output desain:

`design/dashboard-reports.pen`

Quality gate:

- Enam role memiliki dashboard relevan.
- Semua KPI mempunyai sumber.
- Seluruh ekspor sesuai RBAC.
- Tidak ada kebocoran detail sensitif pada dashboard.
- Visual hierarchy konsisten.

Lanjutkan UX-M8.

---

# 24. UX-M8 — RESPONSIVE DESIGN, ACCESSIBILITY & FINAL DESIGN AUDIT

Pada milestone terakhir, audit seluruh desain UX-M1 sampai UX-M7.

Jangan hanya membuat laporan.

Lakukan koreksi visual terhadap desain yang belum memenuhi standar.

## 24.1 Responsive design

Gunakan canonical viewport:

- Desktop: 1440 px.
- Tablet: 768 px.
- Mobile: 390 px.

Buat responsive variants yang nyata untuk screen utama dan seluruh workflow wajib.

Periksa juga berdasarkan desain dan perilaku layout pada:

- 320 px.
- 375 px.
- 1024 px.
- 1280 px.
- 1920 px.

Gunakan kemampuan inspeksi Pencil yang tersedia.

Jangan mengklaim breakpoint telah diuji di browser apabila belum ada implementasi frontend.

Buat:

`design/handoff/RESPONSIVE_SPEC.md`

Dokumentasikan perilaku setiap layout, sidebar, drawer, tabel, form, dialog dan filter.

## 24.2 Accessibility

Target desain:

WCAG 2.2 AA.

Periksa:

- Color contrast.
- Readability.
- Visible focus state.
- Target size.
- Keyboard interaction specification.
- Accessible labels.
- Error communication.
- Status tidak hanya melalui warna.
- Text zoom/reflow specification.
- Dialog focus behavior.
- Reduced motion specification.
- Navigation consistency.

Jangan mengklaim kepatuhan WCAG penuh hanya berdasarkan desain Pencil.

Keyboard, semantic HTML, screen reader dan implementasi aksesibilitas aktual harus diverifikasi oleh Frontend Agent.

## 24.3 Anti-AI slop audit

Gunakan skill ui-taste, antislop, antislop-ui, dan skill lain yang relevan.

Periksa:

- Visual hierarchy.
- Typography.
- Spacing.
- Composition.
- Information density.
- Consistency.
- Human-centered workflow.
- Unnecessary decoration.
- Generic dashboard patterns.
- Excessive card usage.
- Unnecessary shadows.
- Awkward alignment.
- Mobile usability.

Lakukan visual refinement sampai seluruh masalah desain kritis terselesaikan.

## 24.4 Contract audit

Periksa ulang setiap screen terhadap:

- PRD.
- UID.
- AFD.
- RBAC.
- OpenAPI.
- DBD.
- Decision Log.

Pastikan setiap field, tindakan, status, filter dan indikator memiliki sumber yang benar.

## 24.5 Design system audit

Periksa:

- Duplicate components.
- Token drift.
- Inconsistent colors.
- Typography drift.
- Spacing inconsistency.
- Inconsistent button variants.
- Inconsistent status mapping.
- Unused components.

Perbaiki tanpa mengubah aturan bisnis.

---

# 25. SCREEN COVERAGE REQUIREMENTS

Seluruh screen ID UID harus tercakup.

| Screen ID | Screen                     |
| --------- | -------------------------- |
| S01       | Login                      |
| S02       | Dashboard                  |
| S03       | Profil dan Konteks         |
| S04       | Pengguna dan Peran         |
| S05       | Master Siswa               |
| S06       | Master Pegawai/Kelas/Tahun |
| S07       | Penempatan dan Penugasan   |
| S08       | Catat Kehadiran            |
| S09       | Rekap Kehadiran            |
| S10       | Daftar Kasus               |
| S11       | Detail Kasus               |
| S12       | Daftar Layanan             |
| S13       | Buat Permohonan            |
| S14       | Detail Layanan             |
| S15       | Arsip                      |
| S16       | Laporan                    |
| S17       | Audit                      |
| S18       | Akses/Error                |

S01–S18 adalah kelompok screen, bukan batas maksimal jumlah artboard.

Jika satu kelompok membutuhkan beberapa daftar, detail, form, dialog, role-specific variant atau state, buat seluruh variasi yang relevan.

Jangan mengklaim coverage 100% hanya karena terdapat 18 frame utama.

Buat:

`design/handoff/SCREEN_INVENTORY.md`

Catat:

- Screen ID.
- Subscreen.
- Role.
- Desktop variant.
- Tablet variant.
- Mobile variant.
- Loading.
- Empty.
- Error.
- Success.
- Permission state.
- Pencil file.
- Frame/node identifier jika tersedia.
- Contract mapping.
- Design status.

---

# 26. INTERACTION AND STATE DESIGN

Seluruh interaksi yang diperlukan harus memiliki spesifikasi yang jelas.

Buat visual state atau dokumentasi interaksi untuk:

- Hover.
- Focus.
- Active.
- Disabled.
- Loading.
- Refreshing.
- Empty.
- Success.
- Validation error.
- Unauthorized.
- Forbidden.
- Not found.
- Conflict.
- Rate limiting.
- Network failure.
- Server error.
- Confirmation dialog.
- Unsaved changes.

Gunakan micro-interaction:

- 120–180 ms untuk feedback ringan.
- 180–220 ms untuk drawer/dialog jika membantu.

Hormati reduced motion.

Jika Pencil tidak mendukung pembuatan prototype interaktif tertentu, buat frame state dan interaction specification yang jelas.

Jangan mengklaim prototype interaktif berfungsi jika belum diuji.

Buat:

`design/handoff/INTERACTION_SPEC.md`

---

# 27. VISUAL VERIFICATION PROTOCOL

Jangan hanya membuat banyak frame tanpa memeriksa tampilannya.

Setelah setiap screen utama dibuat:

1. Inspect desain menggunakan tool Pencil.
2. Ambil visual evidence jika capability tersedia.
3. Periksa alignment.
4. Periksa clipping.
5. Periksa overlap.
6. Periksa overflow.
7. Periksa text wrapping.
8. Periksa contrast.
9. Periksa spacing.
10. Periksa kesesuaian dengan UID.
11. Periksa role permission.
12. Periksa contract mapping.
13. Lakukan koreksi visual.
14. Simpan ulang hasil yang sudah diperbaiki.

Gunakan siklus:

`DESIGN -> INSPECT -> AUDIT -> REFINE -> VERIFY -> SAVE`

Jangan menandai visual verification PASS tanpa melakukan inspeksi aktual.

Simpan evidence pada:

`design/evidence/`

Gunakan penamaan yang terstruktur berdasarkan milestone, screen ID, viewport dan revision.

Jika tool tidak mendukung ekspor screenshot, catat metode inspeksi alternatif serta keterbatasannya.

---

# 28. DESIGN FILE STRUCTURE

Target struktur desain:

design/
├── AGENTS.md
├── README.md
├── design-system.pen
├── authentication.pen
├── master-data.pen
├── attendance.pen
├── student-affairs.pen
├── administration.pen
├── dashboard-reports.pen
├── tokens.json
├── handoff/
│   ├── DESIGN_HANDOFF.md
│   ├── COMPONENT_INVENTORY.md
│   ├── SCREEN_INVENTORY.md
│   ├── SCREEN_CONTRACT_MATRIX.md
│   ├── ROLE_SCREEN_MATRIX.md
│   ├── RESPONSIVE_SPEC.md
│   ├── INTERACTION_SPEC.md
│   ├── STATUS_MAPPING.md
│   └── FRONTEND_IMPLEMENTATION_MAPPING.md
├── audit/
│   ├── PENCIL_MCP_SMOKE_TEST.md
│   ├── SKILL_USAGE_REPORT.md
│   ├── UX_LAWS_TRACEABILITY.md
│   ├── ACCESSIBILITY_AUDIT.md
│   ├── ANTI_SLOP_AUDIT.md
│   ├── CONTRACT_COMPLIANCE_AUDIT.md
│   └── FINAL_DESIGN_AUDIT.md
└── evidence/

Gunakan struktur tersebut sebagai target.

Jika terdapat struktur resmi yang berbeda pada DESIGN_EXECUTION_PLAN.md atau keterbatasan pengelolaan multi-document Pencil, ikuti struktur yang disepakati dan dokumentasikan pemetaan filenya.

Jangan membuat file `.pen` kosong atau mengarang isi format internal Pencil.

Gunakan operasi Pencil yang didukung.

---

# 29. DESIGN HANDOFF TO FRONTEND AGENT

Hasil desain harus dapat digunakan oleh Frontend Agent tanpa harus menebak.

Buat:

`design/handoff/DESIGN_HANDOFF.md`

Isi minimal:

- Design revision.
- Contract revision.
- UID version.
- Design file inventory.
- Screen inventory.
- Component inventory.
- Color tokens.
- Typography.
- Spacing.
- Responsive rules.
- Status mapping.
- Interaction specification.
- Role navigation.
- Field mapping.
- API mapping.
- Accessibility requirements.
- Design evidence.
- Known limitations.
- Open decisions.
- Design acceptance criteria.

Buat:

`design/handoff/FRONTEND_IMPLEMENTATION_MAPPING.md`

Petakan komponen Pencil menuju Atomic Design frontend.

Contoh:

- Design Button -> Atoms/Button.
- Design FormField -> Molecules/FormField.
- Design AttendanceEditor -> Organisms atau feature-specific component.
- Design DashboardLayout -> Templates/DashboardLayout.
- Design Screen S08 -> Attendance Page.

Sesuaikan dengan struktur aktual TRD dan FRONTEND_EXECUTION_PLAN.md.

Jangan mengimplementasikan file React.

Design Agent hanya menyediakan desain dan handoff.

---

# 30. MILESTONE EXECUTION AND PERSISTENT PROGRESS

Gunakan:

`coordination/DESIGN_STATUS.md`

Sebagai sumber status pekerjaan Design Track.

Sebelum setiap milestone:

- Baca status terakhir.
- Identifikasi task yang belum selesai.
- Periksa kontrak revision.
- Periksa prerequisite.
- Periksa allowed paths.

Setelah setiap milestone:

- Catat task ID.
- Catat file desain.
- Catat screen yang selesai.
- Catat skill yang digunakan.
- Catat bukti visual.
- Catat quality gate.
- Catat blocker.
- Catat keputusan yang masih terbuka.
- Catat langkah berikutnya.

Gunakan status yang ditetapkan AGENTS.md dan execution plan.

Bedakan:

- Design in progress.
- Design verified internally.
- Ready for review.
- Approved design.

Jangan mengarang persetujuan pengguna.

Lanjutkan secara otomatis ke milestone berikutnya setelah internal gate terpenuhi, kecuali ada blocker yang benar-benar mengharuskan intervensi pengguna.

Jika terdapat blocker pada satu screen, lanjutkan screen atau milestone independen yang tidak terdampak.

Jangan membuat seluruh jalur terhenti hanya karena satu keputusan bisnis terbuka.

---

# 31. FINAL QUALITY GATE

Sebelum menyatakan seluruh desain selesai, periksa:

## Design completeness

- Seluruh UX-M1 sampai UX-M8 selesai secara internal.
- Semua screen S01-S18 tercakup.
- Enam role memiliki navigation configuration.
- Enam dashboard role tersedia.
- Seluruh workflow inti A dan B tercakup.
- Seluruh state penting tersedia.
- Responsive variants tersedia.
- File `.pen` benar-benar editable.

## Contract compliance

- Screen Contract Matrix lengkap.
- Field sesuai OpenAPI.
- Enum sesuai kontrak.
- User actions sesuai RBAC.
- Workflow sesuai AFD.
- Tidak ada fitur fiktif.
- Pending business rules tidak dianggap disetujui.

## Visual quality

- Seluruh desain menggunakan UID.
- Tidak ada critical AI slop.
- Design tokens konsisten.
- Typography konsisten.
- Reusable components tersedia.
- Visual inspection dilakukan.
- Seluruh masalah kritis diperbaiki.

## Accessibility

- Contrast diperiksa.
- Focus states tersedia.
- Target sizes diperiksa.
- Keyboard behavior didokumentasikan.
- Responsive layout diperiksa.
- Keterbatasan audit desain dicatat.

## Handoff

- tokens.json tersedia.
- Component Inventory tersedia.
- Screen Inventory tersedia.
- Role Screen Matrix tersedia.
- Screen Contract Matrix tersedia.
- Responsive Spec tersedia.
- Interaction Spec tersedia.
- Frontend Implementation Mapping tersedia.
- Design Handoff tersedia.

## Scope isolation

- Tidak ada perubahan pada frontend.
- Tidak ada perubahan pada backend.
- Tidak ada perubahan kontrak tanpa persetujuan.
- Tidak ada perubahan file milik agent lain.
- Git diff sesuai allowed paths.

Jangan menandai pemeriksaan sebagai PASS apabila belum dilakukan.

---

# 32. FINAL EXECUTION REPORT

Buat:

`design/audit/FINAL_DESIGN_AUDIT.md`

Berikan laporan akhir lengkap yang memuat:

## A. Executive Summary

Ringkasan hasil desain UX-M1 sampai UX-M8.

## B. Milestone Completion Matrix

Untuk setiap milestone:

- Status.
- Task yang selesai.
- Output.
- Evidence.
- Remaining issue.

## C. Screen Coverage Matrix

Seluruh S01–S18 dan subscreen yang relevan.

## D. Role Coverage

Seluruh enam role dan navigasinya.

## E. Design System Results

- Jumlah token.
- Jumlah reusable components.
- Component variants.
- Layout templates.

Gunakan angka aktual.

## F. Contract Compliance

- Contract revision.
- Endpoint yang dipetakan.
- Field mapping.
- Role permission mapping.
- Contract gaps.

## G. Skill Utilization

Skill yang benar-benar digunakan beserta kontribusinya.

## H. Responsive Results

Viewport, screen, visual evidence dan temuan.

## I. Accessibility Results

Pemeriksaan desain yang dilakukan dan batasan yang masih memerlukan frontend testing.

## J. Anti-AI Slop Audit

Temuan visual dan perbaikannya.

## K. Deliverables

Daftar seluruh file `.pen`, JSON, Markdown, dan evidence yang dihasilkan.

## L. Handoff Readiness

Jelaskan kesiapan Frontend Agent menggunakan desain tersebut.

## M. Remaining Blockers

Catat keputusan sekolah, contract gaps, keterbatasan Pencil MCP, atau masalah desain yang belum terselesaikan.

## N. Final Decision

Gunakan salah satu status:

`READY — COMPLETE_UIUX_DESIGN_READY_FOR_FRONTEND_HANDOFF`

`CONDITIONALLY_READY — DESIGN_HANDOFF_WITH_OPEN_ITEMS`

`BLOCKED — CRITICAL_DESIGN_OR_CONTRACT_ISSUES`

Status READY hanya berarti desain lengkap dan telah diverifikasi secara internal untuk diserahkan kepada Frontend Agent.

Status READY tidak berarti:

- Desain telah disetujui pihak sekolah.
- Frontend sudah diimplementasikan.
- Backend sudah berjalan.
- WCAG compliance telah terbukti penuh.
- UAT/SUS telah dilakukan.
- Sistem siap produksi.

---

# 33. FINAL INSTRUCTION

Kerjakan seluruh milestone UX-M1 sampai UX-M8 secara menyeluruh.

Gunakan Pencil MCP sebagai alat desain utama.

Gunakan seluruh skill yang relevan dan benar-benar tersedia.

Jangan berhenti pada design system.

Jangan berhenti pada dashboard.

Jangan membuat desain generik.

Jangan membuat desain berdasarkan tebakan.

Jangan menunggu backend atau frontend diimplementasikan.

Pastikan semua desain sesuai kebutuhan pengguna, kontrak API, RBAC, workflow, UID dan dokumen proyek.

Prioritaskan kualitas daripada sekadar jumlah frame.

Gunakan design verification secara iteratif.

Pertahankan isolasi Design Track.

Tujuan akhir adalah menghasilkan paket desain editable yang lengkap, profesional, anti-AI slop, konsisten, responsif dan siap menjadi referensi implementasi Frontend Agent.

Mulai sekarang dengan workspace preflight, mandatory document review, skill discovery, dan Pencil MCP smoke test.

Setelah smoke test berhasil, kerjakan UX-M1 dan lanjutkan secara sistematis sampai UX-M8 sesuai quality gates yang telah ditetapkan.
