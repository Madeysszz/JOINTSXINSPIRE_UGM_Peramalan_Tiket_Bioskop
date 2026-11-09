# Challenger supply trend D4–D7

## Keputusan

Submission challenger memakai 30% prediksi varian tren okupansi/show dan 70% prediksi Dani v7 pada D4–D7. D8–D10 identik dengan v7. Baseline `submission_v7_patuh_lebaran_x150.csv` dan notebook `Inference_Terbaru_Dani.ipynb` tidak diubah. Ini kandidat eksperimen, bukan bukti bahwa skor private akan membaik.

Pengguna melaporkan skor leaderboard publik challenger **0,47313**, dibanding skor v7 sebelumnya sekitar **0,475**. Kenaikan ini konsisten dengan arah validasi lokal, tetapi leaderboard publik hanya mencakup sekitar 10% test dan tidak memastikan hasil private.

OOF dihitung ulang dengan pipeline Dani terbaru yang sama untuk baseline dan supply. Berbeda dari uji internal-only sebelumnya, kedua sisi di sini memakai label lokal dari snapshot Wikipedia revisi 30 September 2025 yang sudah ada, serta kalender dan post-processing v7. Fitur supply hanya menambah selisih `log1p` okupansi D3 terhadap rata-rata D1–D2 dan selisih `log1p` show dengan definisi yang sama. Tidak ada data eksternal baru yang diambil.

## Hasil validasi

Baseline sepadan: CV MASE 0,378009, weighted CV 0,491313, temporal MASE 0,345563, temporal weighted 0,411498. Delta positif berarti galat turun. SE berpasangan dikelompokkan menurut film.

| Variant | Horizon | Supply weight | Weighted CV | Δ CV ± SE | Temporal weighted | Δ temporal ± SE |
|---|---|---|---:|---:|---:|---:|
| D4–D7 | D4–D7 | 0,10 | 0,491107 | +0,000206 ± 0,000106 | 0,411125 | +0,000374 ± 0,000119 |
| D4–D7 | D4–D7 | 0,20 | 0,490731 | +0,000582 ± 0,000222 | 0,410542 | +0,000957 ± 0,000280 |
| **D4–D7** | **D4–D7** | **0,30** | **0,490504** | **+0,000809 ± 0,000333** | **0,410331** | **+0,001168 ± 0,000404** |
| D4–D7 | D4–D7 | 0,40 | 0,490369 | +0,000944 ± 0,000443 | 0,409897 | +0,001602 ± 0,000548 |
| D4–D7 | D4–D7 | 0,50 | 0,490519 | +0,000794 ± 0,000530 | 0,410154 | +0,001344 ± 0,000660 |
| D4–D9 | D4–D9 | 0,40 | 0,490379 | +0,000934 ± 0,000581 | 0,409633 | +0,001865 ± 0,000678 |
| Horizon-specific | D4–D9 | 0,25/0,35/0,35/0,30/0,10/0,10 | 0,490566 | +0,000747 ± 0,000376 | 0,410079 | +0,001419 ± 0,000469 |

Ordinary CV/temporal MASE dan delta lengkap ada di `hasil_blend.csv`. Rincian setiap hari dan kelompok ada di `rincian_blend.csv`.

**Terbaik menurut weighted CV:** D4–D7 bobot 0,40. **Paling robust dan dipilih:** D4–D7 bobot 0,30. Varian 0,30 mempertahankan sekitar 86% gain CV bobot 0,40, memakai bobot lebih kecil, memperbaiki CV di keempat hari D4–D7, serta memperbaiki temporal weighted. Pada bobot 0,40, D6 sedikit memburuk dalam weighted CV. Varian D4–D9 bobot 0,40 memberi temporal terbaik, tetapi D9 memburuk dalam weighted CV dan gain totalnya kurang meyakinkan dibanding SE. Horizon-specific juga tidak memberi alasan kuat untuk kompleksitas tambahan.

Untuk bobot 0,30, delta weighted CV D4, D5, D6, D7 masing-masing +0,001526, +0,002271, +0,000066, +0,001803; D8–D10 nol. Delta positif pada tiga bin skala, weekday, weekend, serta lebar rilis ≤40 dan >70 dalam CV maupun split waktu. Kuantil ke-95 galat terskala turun 0,0043 pada CV dan 0,0038 pada split waktu; ini diagnostik, bukan jaminan ekor private.

## Inference dan submission

`buat_submission.py` menghitung ulang prediksi baseline test dan memverifikasi bahwa seluruh 72.611 nilainya **identik persis** dengan v7 sebelum melatih varian supply. Fitur supply untuk test hanya memakai D1–D3 dari `test_history.csv`; kode memakai fungsi fitur yang sama untuk pseudo-train dan test. Model dilatih dari `train.csv`; `test.csv` hanya untuk urutan ID dan horizon, tanpa label D4–D10. Seed model tetap 0. Tidak ada AutoML, model pralatih, atau AI API dalam inference.

File `submission_supply_hybrid_d4d7_w30.csv` mempunyai 72.611 baris dengan urutan ID sama dengan `sample_submission.csv`, tanpa NaN atau nilai negatif. Sebanyak 25.073 baris berubah dari v7, semuanya pada D4–D7. Total prediksi 11.883.011 tiket versus 11.845.144 pada v7, selisih +37.867; D8–D10 identik.

## Batas kesimpulan

OOF film dan split waktu berasal dari April–September 2025. Split waktu pernah dipakai selama pengembangan dan bukan holdout independen; target Oktober 2025–Maret 2026 tetap tersembunyi. Public leaderboard sekitar 10% tidak dipakai memilih bobot. Perbedaan hasil dengan uji internal-only sebelumnya berasal dari baseline, label lokal, kalender, dan post-processing yang berbeda; kedua kelompok CV tidak boleh dibandingkan langsung.

Reproduksi: jalankan `buat_oof.py`, lalu `validasi_blend.py`, kemudian `buat_submission.py` dari folder `KNOWLEDGE`. Semua keluaran berada dalam folder ini.
