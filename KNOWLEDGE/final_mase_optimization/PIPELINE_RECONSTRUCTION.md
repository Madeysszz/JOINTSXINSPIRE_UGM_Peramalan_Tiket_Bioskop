# Rekonstruksi pipeline Dani

Sumber kode utama: `../notebook_terbaru` (JSON notebook tanpa ekstensi, 164 sel). Sel 0–99 berisi riset, 100–144 notebook final, dan 145–163 salinan skrip. `../Inference_Terbaru_Dani.ipynb` adalah cabang v7 yang lebih lama. Output notebook gabungan tidak semuanya dihitung ulang setelah kode final berubah; angka validasi pada sel 131 dan teks skor pada sel 143 tidak boleh dianggap hasil pasti dari kode D1 60 hari pada sel 110.

```text
train.csv -> D1 film: 50% puncak jumlah klaster dalam 60 hari pertama
          -> pasangan aktif pada D3, D4–D10 kosong diisi nol
          -> fitur D1–D3 + kalender target + harga relatif + label film lokal
          -> HGB lokal/impor, XGBoost L1, tabel median, classifier nol
          -> 0,4 HGB + 0,4 XGBoost + 0,2 tabel
          -> p0 > 0,55: nol; lainnya: faktor level × sekolah × Lebaran
          -> floor(prediksi + 0,5), minimum nol -> id test -> CSV
```

## Detail yang dapat diverifikasi dari kode

- D1 test adalah tanggal minimum per film pada `test_history.csv`; D1–D3 adalah tiga tanggal kalender. D1 pseudo-train pada sel 110 adalah hari pertama jumlah klaster aktif mencapai 50% puncak selama 60 hari sejak transaksi pertama. Film yang terlihat pada 1 April atau D10-nya lewat 30 September dikeluarkan. Pasangan harus punya transaksi D3. Target D4–D10 yang tidak memiliki baris transaksi diisi nol.
- Skala MASE adalah `max(mean(total_ticket D1:D3), 1)`. Target regresi adalah tiket dibagi skala. CV memakai lima fold terpisah per film, seed 0; split waktu berdasarkan D1 sebelum/sesudah 1 Juli. Bobot latih mengikuti distribusi skala test; bobot evaluasi diagnostik memakai skala × lebar rilis.
- Fitur pasangan: `log10(skala)`, rasio tiket D1/D2/D3 terhadap skala, jumlah hari aktif, pola mulai tayang, label lokal, hari D1, serta status libur D1–D3. Fitur target: horizon, hari pekan, status libur, harga relatif, jumlah hari libur kumulatif, dan jarak sejak libur. Median table memakai lima bin skala dengan pengenceran sel hari pekan. Pola baru aktif D2/D3 memakai tiket D3 sebagai acuan tabel.
- HGB memakai `loss='absolute_error'`, `max_iter=250`, `learning_rate=0.05`, `random_state=0`, dan cabang film lokal/impor. XGBoost memakai `reg:absoluteerror`, 600 pohon, depth 7, learning rate 0,03, seed 0. Classifier HGB memberi `p0`; ambang `p0 > 0.55` mengunci nol.
- Pada sel final, `K_LEVEL=1.15`, `K_SEKOLAH=1.30`, `K_LEBARAN=2.00`. Sekolah berlaku 20 Desember–3 Januari dan 21–26 Maret, hanya saat `off==0`; Lebaran berlaku pada tanggal target mulai 21 Maret. Faktor dikalikan pada ensemble setelah komponen model/tabel dibulatkan, lalu hasil akhir dibulatkan sekali. Gerbang nol diterapkan sebelum hasil akhir; perkalian tidak menghidupkan prediksi nol.
- Skrip `submit_seed5.py` dalam lampiran memuat faktor Lebaran harian `[2.45, 2.21, 2.04, 2.45, 1.82, 1.75, 1.60]` menurut **tanggal 21–27 Maret**, bukan horizon D4–D10. Enam nilai pertama berasal dari indeks historis, nilai ketujuh ekstrapolasi. Ini cabang skrip seed5, bukan bukti implementasi CSV h5.
- Output submission pada sel 141 adalah `data/submission_juri_final.csv` dengan kolom `id,total_ticket`. Gabungan notebook tidak aman dijalankan `Run All`: sel lampiran menjalankan skrip tambahan, path `data/` tidak cocok dengan `KNOWLEDGE/dataset/`, dan snapshot Wikipedia revisi yang diperlukan tidak ada pada folder dataset saat audit ini.

## Batas reproduksi

Cache `oof_dani_supply.npz` berasal dari pipeline v7 dengan D1 **21 hari** dan model supply. Ia cukup untuk mereproduksi OOF champion dan menguji pascaproses output akhir, tetapi tidak sepadan dengan OOF notebook final D1 60 hari. Cache hanya menyimpan prediksi akhir dan versi tanpa faktor, bukan probabilitas `p0` maupun seluruh komponen HGB/XGBoost/tabel. CSV h5 tersedia, tetapi skrip pembuat h5 tidak tersedia. Tidak ada klaim bahwa model final Dani 60 hari atau h5 telah dilatih ulang di sini.
