# Pengetahuan penelitian prediksi tiket D4–D10

> Status 9 Oktober 2026: folder percobaan dipindahkan ke [ARSIP_LENGKAP_PERCOBAAN.zip](ARSIP_LENGKAP_PERCOBAAN.zip). Ringkasan hasil terbaru ada di [RANGKUMAN_SEMUA_PERCOBAAN.md](RANGKUMAN_SEMUA_PERCOBAAN.md). Path folder percobaan di bawah adalah path arsip; ekstrak ZIP ke direktori induk `final_joints_v2` jika perlu membukanya kembali. Arsip lama `ARSIP_PERCOBAAN.zip` tersimpan di dalam ZIP baru.

## Berkas yang dipakai sekarang

- `dataset/`: tujuh CSV kompetisi dan snapshot Wikipedia yang dipakai untuk label film lokal.
- `Inference_Terbaru_Dani.ipynb`: notebook utama untuk melatih model dan membuat prediksi.
- `submission_v7_patuh_lebaran_x150.csv`: submission 72.611 baris yang dilaporkan mendapat MASE publik sekitar **0,475**.
- `ARSIP_LENGKAP_PERCOBAAN.zip`: folder percobaan terbaru dan arsip lama yang berisi 128 file. Arsip menyimpan path aslinya agar percobaan dapat dipulihkan.
- `audit_artefak_lanjutan_2026/`: audit file yang benar-benar tersedia, salinan kerja v7/champion/h5 dan cache OOF, serta keputusan eksperimen lanjutan. Tidak ada model atau submission baru.

Jalankan notebook utama dengan direktori kerja `KNOWLEDGE`, sehingga `dataset/` ditemukan. Untuk memulihkan folder percobaan, ekstrak ZIP baru ke direktori induk `final_joints_v2`.

## Masalah dan batas kompetisi

Setiap pasangan film–klaster memiliki tiket D1–D3 sebagai riwayat dan harus diprediksi pada D4–D10. Ketujuh tanggal target adalah tanggal kalender berurutan. Jika suatu hari tidak memiliki transaksi, tiket aktualnya nol. `train.csv` adalah riwayat harian April–September 2025, bukan tabel contoh D1–D10; contoh validasi harus dibentuk dari riwayat itu. `test_history.csv` hanya menyediakan D1–D3, sedangkan `test.csv` tidak menyediakan label D4–D10.

Skor resmi adalah rata-rata `abs(aktual - prediksi) / max(rata-rata tiket D1–D3, 1)` per baris. Dengan demikian, galat pada pasangan kecil dapat berpengaruh besar. Aturan yang dipakai dalam penelitian ini: seed tetap, data eksternal berhenti paling lambat 30 September 2025, tanpa AutoML atau AI API untuk inference, dan bobot model maksimal 200 MB. Sekitar 90% nilai kompetisi berasal dari private leaderboard. Skor publik dan CV lokal mengukur hal yang berbeda; label test private tidak tersedia.

## Model Dani dan data yang dipakai

Notebook Dani awal memperkirakan D1 film train sebagai hari pertama ketika jumlah klaster aktif mencapai 50% puncak dalam 21 hari awal. Tanggal transaksi pertama sering berupa premiere atau penayangan terbatas, sehingga kurang cocok dengan D1 film test. Pseudo-train mempertahankan pasangan yang aktif pada D3 dan mengisi nol pada hari target tanpa transaksi. Definisi 50% lebih baik daripada tanggal transaksi pertama pada CV utama. Pengguna melaporkan bahwa enam film test yang punya tanggal rilis pada revisi Wikipedia 30 September 2025 semuanya cocok dengan D1 model; cakupan enam film terlalu kecil untuk menyatakan semua film telah terverifikasi.

Fitur inti Dani memakai skala dan bentuk penjualan D1–D3, jumlah hari awal yang aktif, jenis film lokal, kalender target, harga relatif, serta tabel median rasio. HGB dilatih terpisah untuk film lokal dan impor, XGBoost menghasilkan prediksi kedua, dan klasifier memperkirakan peluang tiket nol. Prediksi mentah adalah 40% HGB, 40% XGBoost, dan 20% tabel; peluang nol di atas 0,55 menjadikan prediksi nol. Label lokal pada versi patuh berasal dari `movies.csv` dan snapshot Wikipedia bertanggal paling lambat 30 September 2025. Empat model terlatih berukuran sekitar **4,25 MB** jika diserialisasi tanpa kompresi, jauh di bawah batas 200 MB.

`test_history.csv` sudah dipakai sebagai masukan D1–D3 saat inference. `test.csv` tidak dapat dipakai untuk latihan supervised D4–D10 karena jumlah tiket target tersembunyi.

## Validasi dan pergeseran data

Penelitian memakai CV yang memisahkan film, beberapa split berdasarkan D1 film, MASE biasa, MASE yang diberi bobot agar komposisi skala mendekati test, selisih galat berpasangan, dan SE yang dikelompokkan per film. Kandidat biasanya disyaratkan membaik lebih dari dua paired SE di CV dan tidak memburuk pada split waktu; aturan 1-SE memilih yang paling sederhana di antara kandidat lolos. Pembobotan komposisi adalah alat diagnosis, bukan metrik resmi. Banyak split telah dilihat berulang kali; holdout akhir Agustus–September pernah dibuka dan tidak boleh diperlakukan lagi sebagai konfirmasi independen.

Pseudo-train masih berbeda dari test: median skala D1–D3 sekitar **184,7** versus **91,7**, pasangan dengan skala paling banyak 20 tiket sekitar **3,3%** versus **13,0%**, dan median klaster per film **31,5** versus **70,0**. Perbedaan ini membatasi daya ramal CV. Split waktu berdasarkan D1 juga tidak sepenuhnya meniru cutoff harian: label D4–D10 sebagian film latih dapat jatuh setelah awal periode validasi.

## Hasil percobaan

Angka pada tabel berasal dari laporan validasi lokal. Baris dengan baseline CV **0,49686** memakai protokol lama dan bobot skala; baris dengan baseline **0,56819** memakai periode pengembangan sampai 4 Agustus dan bobot skala serta lebar rilis. Kedua kelompok angka tidak boleh dibandingkan langsung.

| Percobaan | Temuan | Keputusan |
|---|---|---|
| Dani v3 yang dirapikan | CV per film 0,40482, CV berbobot skala 0,49686; submission dilaporkan sekitar 0,49 publik. | Acuan historis. |
| Nino | Notebook memakai tabel median, LightGBM, dan bagging; skor publik dilaporkan sekitar 0,63. Simulasinya membuang jendela target yang tidak memiliki baris transaksi, padahal target nol harus dinilai. | Tidak dijadikan baseline. |
| `total_show` dan `occupation_rate` D1–D3 | Okupansi memperbaiki CV biasa 0,40482 → 0,39922, tetapi CV berbobot hanya 0,49686 → 0,49605 dan holdout lama memburuk 0,27902 → 0,28402. | Tidak mengganti baseline. |
| D10 dan gerbang nol | False zero D10 pada validasi Juni 10,1% dan Juli 21,1%; sebagian besar muncul setelah gerbang. Koreksi D10 akhir pekan dan 11 variasi ambang tidak stabil antarperiode. | Ambang 0,55 dipertahankan. |
| Pageviews kru sampai 30 September 2025 | CV berbobot memburuk 0,49686 → 0,50542. | Tidak dipakai. |
| Agregat satu film lintas klaster | Pangsa penjualan dan luas rilis membuat CV berbobot memburuk 0,49686 → 0,53550. | Tidak dipakai. |
| Definisi D1 | Tanggal transaksi pertama pada validasi D1 50% membuat CV berbobot memburuk 0,49772 → 0,53334; ambang 25% hampir setara tetapi tidak konsisten. | D1 50% dipertahankan. |
| Model total mingguan D4–D10 | CV berbobot 0,56101 versus Dani 0,49686. Sedikit membantu D9–D10, tetapi merusak D4. Campuran hanya D9–D10 membaik 0,00075 ± 0,00041 SE, belum melewati 2 SE. | Tidak dipakai. |
| Hurdle dan survival hazard | CV berbobot masing-masing sekitar 0,550–0,561 dan 0,547, versus baseline 0,49686. Sekitar 9% pasangan kembali positif setelah hari nol. | Tidak dipakai. |
| Tuning campuran Dani terbaru | 27 konfigurasi bobot/gerbang; tidak ada yang lolos 2 SE dan split waktu. Faktor level 1,15 memperburuk CV berbobot sekitar 0,00961 dan split waktu sekitar 0,01697. | Campuran 40/40/20 dan ambang 0,55 tetap. |
| Tuning HGB dan XGBoost | Dua belas konfigurasi satu parameter; tidak ada yang lolos. XGBoost 400 pohon hanya membaik 0,00005 ± 0,00043 SE di CV. | Parameter Dani tetap. |
| Riwayat retensi satu klaster lintas film | CV berbobot memburuk 0,56819 → 0,56973; split waktu membaik 0,45820 → 0,45693, kurang dari 2 SE. Fitur ini berbeda dari agregat satu film lintas klaster. | Tidak dipakai. |

Percobaan tersebut menguji hipotesis tertentu, bukan membuktikan bahwa seluruh data internal atau semua model pralatih tidak mungkin membantu. Hasil positif kecil setelah banyak percobaan rentan terpilih karena noise.

## Versi Dani terbaru dan submission 0,475

`Inference_Terbaru_Dani.ipynb` menambahkan pengali inference **1,15** untuk level umum, **1,30** pada hari kerja libur sekolah tertentu, dan **1,50** sesudah awal Lebaran 2026. Submission final berhasil direproduksi persis dari notebook pada seluruh 72.611 baris. Riwayat di notebook melaporkan skor publik 0,486 setelah level, 0,483 setelah libur sekolah, dan 0,475 setelah Lebaran. Angka publik berasal dari subset test dan tidak memastikan peringkat private.

Baseline 0,49 dan model mentah notebook terbaru juga berbeda sebelum tiga pengali: 39.349 prediksi baris berubah. Seed lama 2026 sedangkan seed terbaru 0; sumber benih label lokal juga berbeda sehingga 15 film mendapat label berlainan, termasuk delapan film test. Oleh karena itu, perbedaan dua submission akhir tidak dapat seluruhnya diatribusikan ke pengali. Pengali level sendiri menambah sekitar 1,48 juta tiket ke seluruh test. Koreksi libur sekolah mengubah 2.774 prediksi, sedangkan Lebaran mengubah 2.971 prediksi dari 4.417 baris test yang terkena tanggalnya.

Pada validasi model terbaru, MASE berbobot CV berubah **0,56819 → 0,57780** setelah level 1,15; split waktu **0,45820 → 0,47517**. Koreksi sekolah sedikit membantu pada sel sekolah di CV tetapi memburuk pada sel serupa di split Juli. Efek Lebaran 2026 tidak punya padanan berlabel yang memadai: Lebaran 2025 berada pada awal train yang tersensor. Versi 0,475 adalah kandidat dengan skor publik terbaik yang dilaporkan, tetapi keuntungan pada private belum dapat dipastikan dari validasi lokal.

## Masalah yang masih terbuka

Kesulitan utamanya adalah memindahkan pola dari film April–September 2025 ke film test Oktober 2025–Maret 2026: lebih banyak pasangan kecil dan rilis yang lebih lebar, peluang nol bertambah pada horizon akhir, dan kalender libur besar berbeda. MASE berbasis galat absolut menuntut prediksi yang dekat dengan median kondisional; rata-rata penjualan yang tampak terlalu rendah tidak otomatis berarti semua prediksi harus dinaikkan. Menambah ukuran model, memperlambat inference, atau melatih pada `test.csv` tidak menambah label D4–D10.

Usulan jadwal layar mingguan untuk film test terhalang cutoff eksternal: jadwal yang baru tersedia setelah 30 September 2025 tidak boleh dipakai. Jadwal film pesaing yang telah diumumkan sebelum cutoff mungkin legal, tetapi cakupan film test akhir periode parsial; pengguna melaporkan fitur kompetisi rilis sebelumnya tidak memperbaiki CV. Tanggal rilis lebar dari Wikipedia juga tidak memberi fitur baru untuk film test yang D1-nya sudah bertepatan dengan tanggal itu pada enam contoh yang diperiksa.

Status kerja: simpan notebook Dani terbaru dan submission 0,475 sebagai kandidat utama yang dapat direproduksi. Baseline 0,49 dan semua eksperimen tersedia dalam arsip untuk pemeriksaan ulang. Jangan menggunakan skor publik 10% atau holdout yang sudah dibuka sebagai satu-satunya dasar perubahan baru.
