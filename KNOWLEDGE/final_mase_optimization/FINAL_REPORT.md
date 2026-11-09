# Finalisasi optimasi MASE

**Verdict: NO ROBUST IMPROVEMENT — CHAMPION RETAINED.** File final yang dapat dikirim adalah [`submission_best_validated.csv`](submission_best_validated.csv), salinan byte demi byte dari champion supply D4–D7 w0,30. Skor publik champion **0,47313** dan h5 **0,45717** adalah laporan pengguna, bukan MASE test yang dihitung di sini. H5 tetap kandidat publik terbaik yang tersedia, tetapi keunggulannya pada 90% private tidak bisa dibuktikan dari label lokal.

## Audit sumber dan keputusan

- `notebook_terbaru` adalah notebook gabungan, bukan file model h5. Kode final memakai D1 60 hari; cache champion/v7 memakai D1 21 hari. Output tersimpan dalam gabungan notebook sebagian tidak sinkron dengan kode final. Detail ada di [`PIPELINE_RECONSTRUCTION.md`](PIPELINE_RECONSTRUCTION.md).
- Per ID, h5 identik dengan v7 pada 68.194 baris sebelum 21 Maret; 2.971 baris sesudahnya naik dengan total +1.140.692 tiket. Champion berbeda dari v7 pada 25.073 baris D4–D7, total bersih +37.867. Rasio h5/v7 pada prediksi Lebaran positif berpusat di 4/1,5, tetapi 484 baris tidak cocok dengan penggantian faktor pada satu prediksi mentah yang sama. Rincian ada di [`LEBARAN_SENSITIVITY.md`](LEBARAN_SENSITIVITY.md), [`PREDICTION_AUDIT_BY_ID.csv`](PREDICTION_AUDIT_BY_ID.csv), dan [`AUDIT_GROUPS.csv`](AUDIT_GROUPS.csv).
- Reproduksi **dari cache**, bukan training: Dani v7 OOF CV 0,378009 / weighted 0,491313 / temporal weighted 0,411498. Champion OOF CV **0,377017**, weighted **0,490504**, temporal MASE **0,344536**, temporal weighted **0,410331**. Gain weighted champion terhadap v7 **0,000809 ± 0,000333 SE film**.
- Kandidat baru paling rendah pada weighted CV adalah pengali output champion ×0,85: weighted **0,483002**, gain **0,007501 ± 0,004888 SE**, temporal weighted **0,398933**. Kandidat ×0,90 memberi weighted **0,483646**, gain **0,006857 ± 0,003227 SE**, temporal weighted **0,400730**. Semua `EXPLORATORY`: evaluasi memakai ulang fold/split waktu yang telah dibuka, dan backtest kalibrasi crossfit terdahulu tidak memberi gain >2 SE. Pengali lebih dari satu memperburuk CV dan temporal. Tabel lengkap di [`EXPERIMENT_RESULTS.csv`](EXPERIMENT_RESULTS.csv) dan keputusan di [`MODEL_SELECTION.md`](MODEL_SELECTION.md).
- Ambang nol tidak dituning karena cache tidak memuat probabilitas `p0`. Bobot ensemble baru dan model tuning tidak dijalankan karena komponen OOF/test dan reproduksi training yang sepadan tidak tersedia. `.venv_seed` lolos import Python 3.11.15, NumPy 2.4.6, pandas 2.2.3, scikit-learn 1.7.2, XGBoost 3.2.0 untuk audit CSV/NPZ. Tidak ada environment atau paket baru.
- Kalender notebook final memberi overlap pengali sekolah dan Lebaran pada 1.262 baris 25–26 Maret. Pada h5, 1.446 dari 4.417 prediksi periode Lebaran nol. Skenario faktor 1,5–4,0 dan faktor harian hanya menunjukkan perubahan volume tanpa label; tidak ada submission skenario. Audit placebo lama menemukan 0/5 blok libur train dengan cukup film transisi.

## Pemeriksaan submission final

| Pemeriksaan | Hasil |
|---|---|
| File | `KNOWLEDGE/final_mase_optimization/submission_best_validated.csv` |
| Schema | Tepat `id,total_ticket`, sama dengan template |
| Baris / pasangan | 72.611 / 10.373; tujuh horizon D4–D10 per pasangan |
| ID | Unik, tidak ada yang hilang/ekstra, urutan dan nilai sama dengan `sample_submission.csv` serta `test.csv` |
| Prediksi | Bilangan bulat, finite, tanpa NaN/negatif |
| Nol / minimum / maksimum | 27.262 / 0 / 42.124 |
| Total tiket | 11.883.011 |
| SHA-256 sumber champion | `452a89f37b73b1520068e645fcddd0bd413f49ad5828afa95e3351e6b2dd0c48` |
| SHA-256 salinan final | `452a89f37b73b1520068e645fcddd0bd413f49ad5828afa95e3351e6b2dd0c48` |

Sumber h5 memiliki SHA-256 `a5425ea7ea48827a7a57abed3b09381452d6ab0374747cbd4c0a84dd63f7b929` dan sumber v7 `d682c4434dcd23557c4d22da12052c03fe472e808aebc6a5c5abca57dc3ccc5c`. Validasi dan hash lengkap ada di [`SOURCE_CHECKS.csv`](SOURCE_CHECKS.csv). Test hanya dipakai untuk metadata ID/tanggal dan `test_history.csv` untuk D1; label D4–D10 test tidak tersedia dan tidak dipakai. Tidak ada file sumber, ZIP, baseline, atau submission lama yang diubah. Seluruh artefak baru berada dalam folder ini.

Jika keputusan pengiriman didasarkan hanya pada skor publik terlapor, h5 memiliki angka lebih rendah dan file aslinya tetap tersedia di `../diag_h5_v9_leb400.csv`. Pilihan protokol eksperimen ini adalah champion karena bukti OOF/temporal yang sepadan dan tidak ada kandidat baru yang lolos gerbang promosi. Kedua pilihan memiliki ketidakpastian private; tidak ada klaim MASE test lokal.
