# Audit Lebaran tanpa label test

Perbandingan memakai `id` sebagai key. Setiap sumber memiliki 72.611 ID yang sama persis dengan template. Selisih positif berarti prediksi file pertama lebih tinggi. Tabel terperinci tersedia pada `PREDICTION_AUDIT_BY_ID.csv` dan `AUDIT_GROUPS.csv` untuk tanggal, horizon, film, dan `cinema_ids`.

| Perbandingan | Baris berubah | Naik / turun | Selisih bersih tiket | Selisih absolut tiket |
|---|---:|---:|---:|---:|
| h5 − v7 | 2.971 | 2.971 / 0 | +1.140.692 | 1.140.692 |
| champion − v7 | 25.073 | 13.624 / 11.449 | +37.867 | 140.873 |
| h5 − champion | 26.163 | 13.989 / 12.174 | +1.102.825 | 1.250.181 |

H5 dan v7 identik pada **68.194 baris sebelum 21 Maret 2026**. Seluruh 2.971 perubahannya pada 21–27 Maret: 4.417 baris dari tujuh film dan 116 klaster terpapar; 1.446 prediksi h5/v7 tetap nol. Volume v7 pada periode itu 684.396 tiket, champion 699.974, dan h5 1.825.088. H5 dibanding champion berbeda pula sebelum 21 Maret karena champion memakai supply blend pada D4–D7: sebelum tanggal tersebut h5 lebih rendah 22.289 tiket; sejak tanggal itu h5 lebih tinggi 1.125.114 tiket.

| Horizon | Baris h5 ≠ v7 | Tambahan tiket h5 − v7 |
|---|---:|---:|
| D4 | 541 | 304.645 |
| D5 | 528 | 183.135 |
| D6 | 470 | 203.551 |
| D7 | 447 | 127.921 |
| D8 | 401 | 143.210 |
| D9 | 308 | 100.040 |
| D10 | 276 | 78.190 |

Tambahan terbesar berasal dari *Danur: The Last Chapter* (+383.591) dan *Tunggu Aku Sukses Nanti* (+266.168). Lima dari tujuh film menyumbang 88,7% tambahan tiket h5 terhadap v7. Lima klaster terbesar menyumbang 25,0%. Ini konsentrasi **volume**, bukan konsentrasi perubahan MASE, karena label test tersembunyi dan setiap baris memiliki skala sendiri.

## Apakah CSV membuktikan faktor ×4,0?

Pada 2.971 baris Lebaran dengan prediksi v7 positif, median rasio h5/v7 tepat **2,6667**, sesuai rasio faktor 4,0/1,5. Seluruh prediksi h5 positif di periode ini kelipatan empat. Namun hanya **2.487/2.971** pasangan angka yang kompatibel dengan `round(1,5 × raw)` dan `round(4,0 × raw)` pada **satu nilai raw yang sama**; 484 tidak kompatibel bahkan setelah toleransi pembulatan. Jadi CSV mendukung koreksi Lebaran agresif dan lokasinya, tetapi tidak membuktikan bahwa skrip h5 hanya mengganti satu konstanta sebelum pembulatan. Pengalian setelah pembulatan atau langkah antara lain tetap mungkin. Kode h5 tidak tersedia untuk memastikan penyebabnya.

## Overlap faktor kalender

Kode notebook final menetapkan sekolah 21–26 Maret dan Lebaran mulai 21 Maret. Status `off` membuat pengali sekolah hanya berlaku pada **25–26 Maret**, masing-masing 631 baris; total **1.262 baris** menerima sekolah ×1,30 dan Lebaran sekaligus pada cabang kode final. Tanggal 21–22 Maret adalah akhir pekan/libur, 23–24 Maret adalah cuti bersama, sehingga pengali sekolah tidak aktif di empat hari itu. Pada 27 Maret jendela sekolah sudah selesai, tetapi pengali Lebaran tetap aktif. Ini audit logika sel 139, bukan rekonstruksi pasti skrip h5.

## Skenario sensitivitas

`LEBARAN_SCENARIOS.csv` menghitung `round(v7_final × faktor/1,5)` hanya pada 4.417 baris 21–27 Maret; nol tetap nol. Karena v7 sudah melalui gerbang dan pembulatan, simulasi ini **bukan** penggantian faktor pada output model mentah.

| Faktor asumsi | Tiket periode | Kenaikan dari v7 | Total seluruh submission jika diterapkan |
|---|---:|---:|---:|
| 1,5 | 684.396 | 0 | 11.845.144 |
| 2,0 | 912.562 | 228.166 | 12.073.310 |
| 2,5 | 1.140.626 | 456.230 | 12.301.374 |
| 3,0 | 1.368.792 | 684.396 | 12.529.540 |
| 4,0 | 1.825.022 | 1.140.626 | 12.985.770 |
| Harian menurut tanggal | 976.239 | 291.843 | 12.136.987 |

H5 aktual berjumlah **12.985.836**, atau 66 tiket lebih tinggi daripada simulasi faktor 4,0 dari output v7. Deret harian memakai tanggal kalender 21–27 Maret, bukan horizon, dan berasal dari cabang notebook final berbeda. Train April–September 2025 tidak menyediakan analog transisi Lebaran yang memadai: audit placebo lama menemukan **0 dari 5 blok** dengan sekurangnya lima film transisi. Karena itu skenario tidak diranking menurut MASE dan tidak dijadikan submission baru.
