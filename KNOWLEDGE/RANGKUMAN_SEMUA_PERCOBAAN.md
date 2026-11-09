# Rangkuman semua percobaan JOINTS 2026

Dokumen ini menyatukan hasil percobaan saya bersama pengguna dan hasil Dani yang tersedia sampai 9 Oktober 2026. Laporan dan folder percobaan berada di [ARSIP_LENGKAP_PERCOBAAN.zip](ARSIP_LENGKAP_PERCOBAAN.zip), termasuk arsip lama sebagai ZIP di dalamnya. Notebook utama [Inference_Terbaru_Dani.ipynb](Inference_Terbaru_Dani.ipynb) tetap tersedia, serta peta eksperimen Dani yang dikirim pengguna dalam percakapan. Tautan relatif ke laporan percobaan pada dokumen ini berlaku setelah ZIP diekstrak ke direktori induk `final_joints_v2`. Angka leaderboard Dani setelah v7 berasal dari laporan pengguna; hanya v7 dan h5 yang CSV prediksinya tersedia di folder ini. **Tidak ada label D4–D10 test**, sehingga skor publik tidak dapat dihitung ulang secara lokal.

## Cara membaca angka

MASE resmi adalah rata-rata `|y − prediksi| / max(rata-rata tiket D1–D3, 1)` pada baris target. Lebih kecil lebih baik. Semua CV berasal dari pseudo-target berlabel yang dibangun dari `train.csv`; *weighted CV* memberi bobot tambahan untuk meniru komposisi test dan bukan skor resmi. Paired SE dikelompokkan per film. Split waktu Agustus–September, Juni/Juli, dan OOT lain sudah pernah dilihat selama pengembangan; tidak satu pun merupakan konfirmasi independen yang masih tertutup.

Angka dari protokol berikut **tidak boleh disejajarkan langsung**: baseline v3 berbobot skala sekitar **0,49686**; tuning Dani pada subset pengembangan berbobot skala × lebar rilis **0,56819**; uji fitur internal tanpa label Wikipedia/koreksi luar **0,491914**; OOF v7 yang dihitung ulang dengan pipeline supply **0,491313**; dan CVw-2D pada notebook Dani yang tersedia **0,4850**. Perbedaan pseudo-train, fold/periode, bobot, label lokal, seed, dan pascaproses dapat mengubah skor.

## Perjalanan submission publik

Skor dalam kolom terakhir **dilaporkan pengguna/notebook**, bukan dihitung dari `test.csv`.

| Jalur | Perubahan utama | Public MASE | Bukti lokal dan batas |
| --- | --- | ---: | --- |
| Nino, pembanding lama | Tabel median, LightGBM, bagging | sekitar 0,63 | Simulasi notebook Nino membuang jendela yang mempunyai target tanpa transaksi, padahal aktualnya nol. |
| Dani awal | Median rasio; D1 tanggal transaksi pertama | 0,573 | Riwayat skor pada notebook Dani. |
| Dani, D1 rilis lebar | Ganti pendekatan D1 | 0,550 | Riwayat notebook. |
| Dani v2 dengan TMDB | HGB L1, tabel, gerbang nol | 0,510 | Label TMDB setelah cutoff; tidak dipakai pada pipeline patuh. |
| Dani final v2 lama | Fitur dan ensemble tambahan, masih memakai TMDB | sekitar 0,490 | Riwayat notebook; tidak patuh cutoff eksternal. |
| Dani v3 yang dirapikan | Model patuh dan 1-SE | sekitar 0,49 | Submission di arsip; skor dilaporkan pengguna. |
| Dani v4 patuh | Label lokal dari Wikipedia revisi pra-cutoff; level ×1,15 | 0,486 | Riwayat notebook. |
| Dani v5 patuh | Tambah libur sekolah ×1,30 | 0,483 | Riwayat notebook. |
| Dani v7 | Tambah Lebaran ×1,50 | sekitar 0,475 | [CSV v7](submission_v7_patuh_lebaran_x150.csv), 72.611 baris. |
| **Champion pengguna** | Dani v7 70% + supply trend 30% hanya D4–D7 | **0,47313** | [CSV champion](submission_supply_hybrid_d4d7_w30.csv); skor dilaporkan pengguna. |
| Dani v9 | Lebaran ×2,00 menurut peta Dani | 0,469 | Skor dan resep dilaporkan; CSV v9 tidak ada di sini. Koreksi lama “0,46” pada catatan Dani diganti menjadi **0,469**. |
| Dani h2 | Lebaran ×3,00 | 0,4597 | Skor dilaporkan; CSV h2 tidak ada di sini. |
| **Dani h5** | Lebaran ×4,00 | **0,45717** | [CSV h5](diag_h5_v9_leb400.csv) sekarang tersedia; skor tetap laporan leaderboard. |
| Dani h6b | Bentuk Lebaran harian 2025, tanpa sekolah pada hari tertentu | 0,45806 | Skor dilaporkan; lebih tinggi 0,00089 dari h5. CSV h6b tidak ada di sini. |
| Dani label-fix / seed5 | Cabang final lain, D1 60 hari dan/atau rerata seed | 0,47142 / 0,47136 | Skor dilaporkan; ini **bukan** cabang h5 dengan skor terbaik. |

Selisih skor publik champion terhadap h5 adalah **0,01596**. Karena publik kira-kira 10% test dan private 90%, selisih tersebut belum membuktikan keunggulan h5 pada private.

### Perbandingan langsung CSV yang tersedia

Audit sebelumnya menyatakan h5 belum tersedia. Keadaan folder **telah berubah**: `KNOWLEDGE/diag_h5_v9_leb400.csv` sekarang ada. Saya membaca ketiga CSV berdasarkan urutan `id` yang sama dengan `test.csv`, tanpa membuat submission baru.

| File | Baris | Total tiket prediksi | Prediksi nol |
| --- | ---: | ---: | ---: |
| Dani v7 | 72.611 | 11.845.144 | 27.961 |
| Champion supply | 72.611 | 11.883.011 | 27.262 |
| Dani h5 | 72.611 | 12.985.836 | 27.961 |

- **h5 versus v7:** tepat **2.971 baris** berubah, semuanya pada tanggal target **21–27 Maret 2026**; tidak ada satu pun perubahan di 68.194 baris sebelum 21 Maret. Semua perubahan menaikkan prediksi, total **+1.140.692 tiket**. Jumlah prediksi nol sama. Ini mendukung bahwa perbedaan kedua CSV berada pada koreksi level Lebaran. Script pembuat h5 tidak tersedia di sini, sehingga faktor mentah dan seluruh langkah internalnya belum direproduksi.
- **Champion versus v7:** 25.073 baris D4–D7 berubah, total **+37.867 tiket**; D8–D10 identik. Hanya 15,3% perubahan *absolut* tiket berada pada tanggal Lebaran; ini sifat supply blend, bukan h5.
- **h5 versus champion:** 26.163 baris berubah; selisih total **+1.102.825 tiket**. Di luar periode Lebaran, h5 sama dengan v7 sehingga selisih bersih terhadap champion **−22.289 tiket**. Pada tanggal Lebaran, h5 lebih tinggi **+1.125.114 tiket**. Angka tiket mentah tidak sama dengan perubahan MASE karena setiap galat dibagi skala D1–D3.

Tanggal Lebaran menyentuh **4.417 baris dari tujuh film**. Pada champion, 1.296 baris tersebut diprediksi nol dan totalnya 699.974 tiket. Pada h5, 2.971 prediksi positif berubah dibanding v7, sedangkan gerbang nol tetap menghasilkan nol pada sisanya. Detail paparan dan analisis tanpa label ada di [analisis keputusan sebelumnya](next_experiment_decision/FINAL_ANALYSIS.md).

## Percobaan saya: baseline dan arsip lama

Dokumen primer yang telah diarsipkan tercantum di kolom sumber sebagai path **di dalam** [ARSIP_LENGKAP_PERCOBAAN.zip](ARSIP_LENGKAP_PERCOBAAN.zip); arsip lama tersimpan lagi sebagai `KNOWLEDGE/ARSIP_PERCOBAAN.zip` di dalamnya. Ringkasan historisnya juga ada di [PENGETAHUAN.md](PENGETAHUAN.md).

| Percobaan | Hasil yang dicatat | Keputusan / sumber arsip |
| --- | --- | --- |
| Merapikan Dani v3, 18 varian | CV film baseline **0,40482**; split waktu **0,36364**; holdout yang dibuka sekali **0,27902**. Tidak satu pun dari 17 alternatif melewati syarat 2 SE dan split waktu. | Baseline dipertahankan. `hasil_dani_1se/CATATAN_PERUBAHAN.md` |
| Show/okupansi D1–D3 | Okupansi: CV biasa **0,40482 → 0,39922**, tetapi CV berbobot **0,49686 → 0,49605** (gain **0,00081 ± 0,00242**); holdout lama **0,27902 → 0,28402**. | Informasi ada, bukti penggantian lemah. `hasil_dani_fitur_d1d3/CATATAN_PERCOBAAN.md` |
| Diagnosis D10 dan akhir pekan | False zero D10 **10,1%** pada Juni dan **21,1%** pada Juli; mayoritas disebabkan gerbang nol. Koreksi positif akhir pekan Juli hanya **+0,00015 ± 0,00021** MASE biasa. | Jangan menaikkan semua D10. `percobaan_masalah_utama/HASIL_ANALISIS.md` |
| Sebelas varian gerbang nol | Ambang 0,50 unggul Juni tetapi memburuk Juli; tanpa gerbang juga memburuk. | Ambang **0,55** dipertahankan. `percobaan_masalah_utama/HASIL_GERBANG_NOL.md` |
| Pageviews kru Wikipedia pra-cutoff | CV berbobot **0,49686 → 0,50542**; CV biasa **0,40482 → 0,41719**. | Gugur. `eksternal_cutoff_2025_09_30/HASIL_UJI.md` |
| Agregat satu film lintas klaster | CV berbobot **0,49686 → 0,53550**; Juli berbobot **0,42862 → 0,43757**. | Gugur. `percobaan_fe_internal/HASIL.md` |
| D1 tanggal pertama atau ambang 25% | Pada target validasi D1 50%, tanggal pertama memperburuk CV berbobot **0,49772 → 0,53334**; 25% **0,49772 → 0,49922**, tidak konsisten waktu. | D1 50% puncak 21 hari dipertahankan. `percobaan_anchor_d1/HASIL.md` |
| Model total mingguan D4–D10 | CV berbobot **0,49686 → 0,56101**; blend 25% semua hari **0,50159**. Sedikit membantu D9–D10 tetapi merusak D4. | Gugur. `percobaan_total_mingguan/HASIL.md` |
| Blend model mingguan hanya D9–D10 | CV berbobot **0,49686 → 0,49611**, gain **0,00075 ± 0,00041**; di bawah 2 SE. | Eksploratif; tidak dipakai. `percobaan_koreksi_d9_d10/HASIL.md` |
| Hurdle dan survival hazard | CV berbobot hurdle **0,550–0,561**, survival **0,547**, baseline **0,49686**. Sekitar 9% pasangan kembali positif setelah hari nol. | Gugur. `percobaan_hurdle_survival/HASIL.md` |
| Tuning ensemble/gerbang Dani | **27 konfigurasi**, nol lolos 2 SE plus split waktu. Level ×1,15 memperburuk CV berbobot sekitar **0,00961** dan split waktu **0,01697** pada protokol ini. | Campuran 80% model/20% tabel dan gerbang 0,55 tetap. `percobaan_tuning_dani/HASIL.md` |
| Tuning HGB/XGBoost | **12 konfigurasi**, nol lolos. | Parameter Dani tetap. `percobaan_tuning_hp_dani/HASIL.md` |
| Riwayat retensi klaster | CV berbobot **0,56819 → 0,56973**; split waktu **0,45820 → 0,45693**, gain waktu kurang dari 2 SE. | Gugur. `percobaan_riwayat_klaster/HASIL.md` |
| Ablasi tiga pengali dan blend submission | v7 tanpa level/sekolah/Lebaran: **9.886.058 tiket**; v7: **11.845.144**; baseline 0,49: **9.934.352**; blend 50:50: **10.889.746**. | Ini perbandingan prediksi, **bukan** validasi MASE test. [Laporan diagnosis](diagnosis/LAPORAN.md) |

## Percobaan saya: pengujian terbaru

| Percobaan | Hasil | Keputusan dan sumber |
| --- | --- | --- |
| Lima fitur internal tanpa label Wikipedia | Baseline weighted CV **0,491914**, temporal weighted **0,412925**. Kursi/show **0,492006 / 0,407706**; tren okupansi+show **0,490578 / 0,415612**; profil suplai klaster **0,491055 / 0,416023**; genre/rating × harga **0,494598 / 0,427041**; shape pembukaan **0,492657 / 0,411202**. | Tidak ada yang memenuhi gain >2 SE CV dan temporal tidak memburuk. [Laporan internal](eksperimen_internal_2026/LAPORAN_AKHIR.md) |
| **Supply trend sebagai blend selektif** | Pada OOF sepadan, weighted CV Dani v7 **0,491313 → 0,490504**; temporal weighted **0,411498 → 0,410331**; gain CV **0,000809 ± 0,000333**. Bobot 0,40 memberi CV sedikit lebih rendah (**0,490369**), tetapi 0,30 lebih konservatif dan stabil antarhorizon. | Challenger D4–D7 bobot 0,30; public **0,47313** dilaporkan. [Laporan blend](eksperimen_supply_hybrid_2026/LAPORAN.md) |
| Rata-rata lima seed, internal-only | Weighted CV **0,491166 → 0,491158**, gain **0,000008 ± 0,000083**; temporal **0,409870 → 0,409809**. | Tidak cukup. Environment dan sumber label berbeda dari champion, sehingga angka tidak bisa langsung ditempel ke CV champion. [Hasil seed](eksperimen_seed_averaging_2026/RESULTS.md) |
| Anatomi galat baseline Dani OOF | D4–D7 menyumbang **63,7%** loss berbobot; skala 0–50 menyumbang **48,6%** loss dari **14,5%** baris; target aktual nol **32,2%** baris. Pengali diagnostik ×0,90 memberi **0,491313 → 0,484362**, terutama dari target nol. | Diagnosis, bukan kandidat test. [Anatomi](mase_error_anatomy/MASE_ERROR_ANATOMY.md) |
| Kalibrasi crossfit global/bersyarat | Global weighted CV **0,483869**, gain **0,007444 ± 0,004672**; varian TEST-LIKE **0,483647**, gain **0,007667 ± 0,004527**. Kontrol pengali acak juga membaik hampir sama; tidak ada yang >2 SE. | Tidak dipakai. [Backtest kalibrasi](mase_error_anatomy/CALIBRATION_BACKTEST.md) |
| Audit shift D1–D3 | Median skala train/test **170,3/91,7**; okupansi D2 **19,78%/9,57%**. Klasifier domain AUC **0,7895**. | Shift nyata, sebab galat tidak teridentifikasi hanya dari fitur. [Laporan domain](test_history_domain_adaptation/DOMAIN_SHIFT_REPORT.md) |
| Adaptasi domain, nearest, clustering | Importance weighting clip 3/5/10 memberi weighted CV **0,500897/0,505530/0,515028**; nearest mandiri **0,515400–0,519318**; cluster **0,557521**; koreksi residual **0,502118**, baseline **0,491313**. Blend nearest 0,10 nominal membaik tetapi gagal TEST-LIKE dan kontrol level sama baik/lebih baik. | Tidak dipakai. [Backtest domain](test_history_domain_adaptation/DOMAIN_ADAPTATION_BACKTEST.md) |
| Reverse mapping bioskop XXI | Hanya **4/121** ID test HIGH/MEDIUM; metadata menjangkau **2,46%** baris test, kapasitas kursi tepat **1,23%**. Padang ambigu; empat ID baru test UNMAPPED. | Dataset dibuat, tetapi coverage belum layak untuk model massal. [Laporan mapping](reverse_mapping_poc/REVERSE_MAPPING_REPORT.md) |
| Prior eksternal film pra-cutoff | Fitur legal terisi pada **2/211** film train dan **4/140** film test; **4,37%** baris test memperoleh minimal satu fitur. | Dataset dibuat; tidak dilatih karena cakupan terlalu kecil. [Laporan film](external_movie_strength/EXTERNAL_MOVIE_REPORT.md) |
| Fitur kalender tambahan | Weighted CV: libur+cuti **0,492107**; sekolah **0,489142**; pasca-Lebaran **0,490646**; long weekend **0,492038** vs baseline **0,491313**. Varian yang membaik CV memburuk temporal; Ramadan dan Nataru tanpa analog train. | Tidak dipakai. [Backtest kalender](external_calendar_regime/CALENDAR_BACKTEST.md) |
| Feasibility transisi libur dengan placebo | Lima blok libur train independen, **nol** mencapai syarat minimal lima film; 241 pasangan terpapar hanya dari sembilan film. | **NOT FEASIBLE**; berhenti sebelum residual dan placebo. [Laporan transisi](calendar_transition_placebo/FINAL_REPORT.md) |

## Percobaan Dani yang dicatat terpisah

Notebook Dani yang tersedia di folder ini memakai **D1 50% dari puncak dalam 21 hari**, HGB L1 untuk film lokal/impor, XGBoost loss absolut, tabel median, dan gerbang nol 0,55. Keluaran sel validasi notebook: ensemble lengkap sebelum koreksi musim **CV 0,3695; CVw-2D 0,4850; OOT 0,3301; OOTw-2D 0,4001**. Sebagai pembanding, HGB loss kuadrat mendapat CVw-2D **0,5926**, HGB L1 **0,4993**, dan ensemble tanpa gerbang **0,4899**. Notebook juga mencatat 32,2% pseudo-target bernilai nol. Angka ini berasal dari keluaran notebook tersimpan, bukan pelatihan ulang sekarang.

Peta Dani yang dikirim pengguna mendeskripsikan **cabang final lain** dengan jendela D1 **60 hari**. Notebook/codenya tidak ada di folder ini; karena itu hasil di bawah adalah **laporan Dani**, bukan reproduksi lokal:

| Percobaan Dani yang dilaporkan | Hasil/keputusan |
| --- | --- |
| D1 60 hari dibanding 21 hari pada pipeline final seed | CVw-2D **0,4690 vs 0,4840**, OOT **0,3246 vs 0,3295**; 21 hari ditolak pada pipeline final itu. Skor h5 terbaik tetap berasal dari cabang v9 yang lebih lama. |
| Rata-rata seed 0–4 pada M2/M3 | Pada pipeline final 60 hari: CV **0,3558 → 0,3552**, CVw-2D **0,4696 → 0,4690**, OOT **0,3248 → 0,3246**, OOTw-2D **0,4047 → 0,4042**. Diterima Dani secara lokal, tetapi cabang seed5 publik **0,47136**. |
| Bobot tabel per horizon; gerbang per horizon; keduanya | CVw-2D turun masing-masing ke **0,4687 / 0,4684 / 0,4676**, tetapi OOT naik ke **0,3260 / 0,3256 / 0,3264** dari **0,3248**. Ditolak. |
| Momentum D1–D3 | CVw-2D **0,4696 → 0,4693**, OOT **0,3248 → 0,3251**. Ditolak. |
| `total_show` sebagai kuantil tabel kedua | CVw-2D **0,4696 → 0,4698**, OOTw-2D **0,4047 → 0,4049**. Ditolak setelah diuji ulang pada pipeline 60 hari. |
| Label film dan metadata eksternal | Fitur TMDB, Trends, rekam jejak film terlaris, popularitas/kru diuji dan gugur; TMDB pasca-cutoff tidak patuh. Notebook patuh memakai Wikipedia revisi 30 September 2025 untuk label lokal. |
| Fitur internal lain | Retensi klaster, kompetisi rilis, tren nasional, show/okupansi/kapasitas, tanggal gajian, kuantil 0,55–0,70, model terpisah skala, pembobotan kebaruan, dan beberapa gerbang tidak memberi perbaikan CV/OOT yang konsisten. |
| Lebaran datar ×1,5 → ×2 → ×3 → ×4 | Public MASE terlapor **0,475 → 0,469 → 0,4597 → 0,45717**. Seleksi melalui leaderboard publik berisiko menyesuaikan diri ke 10% test; tidak ada analog Lebaran 2026 berlabel yang setara. |
| Bentuk harian Lebaran h6b | Public **0,45806**, lebih buruk 0,00089 daripada h5 meski total periode Lebaran dibuat setara menurut laporan. Tidak ada bukti bentuk harian membantu. |
| Indeks pasar Ramadan dari `test_history` | Dip pada 7–20 Maret dilaporkan, tetapi hanya lima hari pengamatan nonlibur dan D4–D10 Lebaran tidak terlihat. Koreksi Ramadan ×0,7 belum diuji dan tidak boleh dianggap hasil. |

## Kesimpulan yang didukung data

1. **Model median dan gerbang nol penting** untuk MASE serta target harian yang dapat menjadi nol. Mengganti dengan loss kuadrat, model total mingguan, hurdle, atau survival merusak CV pada percobaan yang tercatat.
2. **Supply trend membantu sedikit bila dibatasi D4–D7** pada pipeline OOF yang sepadan, dan submission pengguna naik dari sekitar 0,475 ke **0,47313** publik. Gain lokalnya kecil; private belum diketahui.
3. **Perbedaan h5–v7 pada CSV yang kini tersedia seluruhnya berada di Lebaran**, sementara champion berbeda dari v7 di banyak tanggal D4–D7. Ini menjelaskan *di mana prediksi berubah*, bukan membuktikan bahwa faktor ×4 akan unggul pada private atau bila diterapkan ke champion.
4. **Train tidak memiliki analog cukup untuk mengesahkan koreksi Lebaran 2026.** Audit placebo berhenti pada 0/5 blok dengan film memadai. Perbedaan skala, okupansi, dan kalender train–test juga nyata; adaptasi domain serta kalibrasi yang telah diuji belum memberi bukti transfer kuat.
5. **Data eksternal legal yang berhasil dipetakan terlalu jarang** untuk eksperimen model massal: empat ID bioskop dan empat film test memperoleh metadata dalam dua audit terarah. Kegagalan cakupan saat ini tidak membuktikan bahwa seluruh sumber potensial mustahil berguna.

Status artefak: v7, champion, dan h5 tersedia; skor leaderboard yang dikutip tetap laporan; file model/script h5, CSV v9/h6b, label test, dan skor private tidak tersedia. Tidak ada notebook, environment, model, atau submission yang dijalankan atau diubah untuk membuat rangkuman ini.
