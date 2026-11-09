# Audit artefak dan keputusan eksperimen lanjutan

## Keputusan singkat

**AUDIT ONLY — tidak ada varian baru yang dapat diuji secara tepat dari artefak saat ini.** CSV v7, champion, dan h5 tersedia dan valid secara struktur. Cache OOF yang cocok untuk v7 dan supply blend juga tersedia, tetapi tidak ada OOF h5. CSV v9, label-fix, h6b, serta script pembuat h5 tidak ditemukan di folder atau dua lapis arsip. Notebook v7 memerlukan snapshot Wikipedia yang tidak tersedia, dan `.venv_seed` memakai versi pandas/scikit-learn berbeda dari lingkungan notebook lama. Saya tidak melatih model, menjalankan inference, membuat submission, atau mengubah artefak asli.

## 1. Inventaris yang benar-benar ada

| Artefak | Lokasi saat audit | Kegunaan / batas |
| --- | --- | --- |
| Tujuh CSV kompetisi | `KNOWLEDGE/dataset/` | `train.csv`, `test_history.csv`, `test.csv`, template, film, libur, dan harga ada. `test.csv` tidak mempunyai label D4–D10. |
| v7 ×1,5, champion supply, h5 ×4 | Root `KNOWLEDGE/`; salinan identik dalam `working/` | Ketiga vektor prediksi dapat dibandingkan per ID. Skor publik tetap angka **yang dilaporkan**, bukan hasil hitung lokal. |
| `Inference_Terbaru_Dani.ipynb` | Root dan salinan `working/` | Notebook yang tersedia memakai jendela D1 21 hari dan koreksi Lebaran ×1,5; bukan script h5 maupun notebook final 60 hari yang disebut dalam laporan Dani. |
| `oof_dani_supply.npz` | `ARSIP_LENGKAP_PERCOBAAN.zip` dan salinan `working/` | Array baseline dan supply untuk 7.354 pasangan × 7 horizon, label dan skala train, serta split waktu. OOF champion dapat dihitung sebagai blend 30% D4–D7. |
| `buat_oof.py`, `validasi_blend.py`, `buat_submission.py` | Dalam ZIP, folder `eksperimen_supply_hybrid_2026/` | Script pipeline supply yang sudah ada; tidak dijalankan ulang. |
| Cache/CSV eksperimen lain | ZIP baru dan `ARSIP_PERCOBAAN.zip` yang tersimpan di dalamnya | Ada cache internal, kalender, seed, dan OOF tuning lama. Protokolnya tidak identik dengan h5; angka tidak boleh digabung sebagai validasi h5. |
| v9, label-fix, h6b, v5 mentah, script/OOF h5 | Tidak ditemukan di root, `dataset/`, atau kedua lapis ZIP | Eksperimen A dan perbandingan CV h5 tidak dapat dilakukan secara tepat. |
| Snapshot `wiki_daftar_film_indonesia_2025_oldid27901699.wikitext` | Tidak ditemukan di `dataset/` maupun kedua lapis ZIP | Notebook v7 membacanya untuk label lokal; baseline tidak dapat direproduksi penuh dari berkas proyek saat ini. |

`.venv_seed` berhasil mengimpor NumPy 2.4.6, pandas 2.2.3, scikit-learn 1.7.2, dan XGBoost 3.2.0. Output notebook lama mencatat pandas sekitar 3.0.5 dan scikit-learn 1.9.1. Impor yang berhasil **tidak** membuktikan kesamaan prediksi. Environment lama yang terblokir sudah dihapus pada pembersihan sebelumnya; tidak dibuat penggantinya.

## 2. Kunci baseline dan pemeriksaan submission

`test.csv` dan `sample_submission.csv` masing-masing memiliki 72.611 baris; tanggal target tersedia dari **4 Oktober 2025 sampai 27 Maret 2026**. Pada ketiga CSV, urutan seluruh ID identik dengan template dan test, ID unik, seluruh prediksi bilangan bulat nonnegatif, tanpa NaN.

| File | Public MASE yang dilaporkan | Baris | Nol | Rentang tiket | Total tiket prediksi |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dani v7 ×1,5 | sekitar 0,475 | 72.611 | 27.961 | 0–41.615 | 11.845.144 |
| Champion supply D4–D7 | 0,47313 | 72.611 | 27.262 | 0–42.124 | 11.883.011 |
| Dani h5 ×4,0 | 0,45717 | 72.611 | 27.961 | 0–41.615 | 12.985.836 |

Selisih **h5 − v7** ada pada **2.971 baris**, semuanya bertanggal target mulai **21 Maret 2026**; 68.194 baris sebelum tanggal itu identik. Semua perubahan yang ada menaikkan tiket, total **+1.140.692**. Jumlah prediksi nol tetap sama. Ini bukti kuat pada tingkat **vektor output** bahwa h5 mempertahankan v7 di luar periode Lebaran. Tanpa script h5 dan prediksi mentah, kesamaan seluruh langkah model serta faktor tepat sebelum pembulatan belum dibuktikan.

Selisih **champion − v7** mengenai 25.073 baris, seluruhnya D4–D7, dengan total +37.867 tiket. Di luar Lebaran, 23.042 baris berubah. Selisih **h5 − champion** mengenai 26.163 baris dan total +1.102.825 tiket: −22.289 di luar Lebaran dan +1.125.114 pada tanggal Lebaran. Jumlah tiket berbeda **bukan** ukuran perbaikan MASE; `y_true` test tersembunyi.

## 3. OOF yang cocok dan area galat

Cache yang tersedia menggabungkan `floor(0,7 × base_cv + 0,3 × supply_cv + 0,5)` hanya untuk D4–D7; D8–D10 memakai `base_cv`. Rumus ini mereproduksi angka laporan supply. Label berasal dari pseudo-target train yang mencakup hari tanpa transaksi sebagai nol; cache dan script menyatakan pemisahan per film. Audit ini tidak membangun ulang pseudo-target atau melatih fold baru.

| Prediksi OOF | CV MASE biasa | CV berbobot | Temporal MASE | Temporal berbobot | Gain berbobot vs v7 ± paired SE per film |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dani v7 pada cache | 0,378009 | 0,491313 | 0,345563 | 0,411498 | — |
| Champion supply | **0,377017** | **0,490504** | **0,344536** | **0,410331** | CV **+0,000809 ± 0,000333**; temporal **+0,001168 ± 0,000404** |
| Dani h5 | Tidak tersedia | Tidak tersedia | Tidak tersedia | Tidak tersedia | Tidak dapat dihitung dari cache ini |

Temporal berisi 4.060 pasangan dari 90 film; seluruh CV berisi 7.354 pasangan dari 171 film. Split waktu ini telah dipakai dalam eksperimen sebelumnya dan bukan holdout baru. Faktor Lebaran pada h5 mengenai target Maret 2026, sedangkan pseudo-target OOF berakhir September 2025; bahkan andaikata model h5 di luar kalender sama, cache ini tidak dapat menguji manfaat ×4 pada Lebaran.

Pada champion OOF, **D4–D7 menyumbang 63,6% loss berbobot**, dan pasangan skala D1–D3 **≤50 menyumbang 48,6% loss dari 1.068/7.354 pasangan (14,5%)**. Weighted MASE kelompok skala ≤50 adalah 0,7478, dibanding 0,3702 pada skala >50. Target aktual nol berjumlah 32,2% sel tetapi menyumbang 12,5% loss berbobot; loss lebih banyak berasal dari target positif. Lima film dengan loss terbesar menyumbang **35,3%** loss berbobot. Ini membantu menentukan area diagnosis, tetapi belum membenarkan model baru tanpa validasi yang sepadan.

Gain weighted CV champion per horizon: D4 **+0,001526**, D5 **+0,002271**, D6 **+0,000066**, D7 **+0,001803**; D8–D10 nol secara konstruksi. Varian supply tren penuh pernah memburuk pada split waktu; sebab itu blend selektif tetap lebih masuk akal daripada mengganti seluruh baseline.

## 4. Status kandidat biaya rendah

| Kandidat dari instruksi | Artefak yang diperlukan | Hasil audit dan keputusan |
| --- | --- | --- |
| A. Blend v9 dengan label-fix di luar Lebaran; Lebaran h5 ×4 | CSV v9 dan label-fix yang sepadan, plus aturan pembuatnya | Kedua CSV tidak ada. Tidak dibuat blend rekaan dari h5/v7 karena itu bukan pasangan yang diminta. **Belum dapat diuji.** |
| B. K_LEVEL 1,15 → 1,0 pada h5; Lebaran tetap ×4 | Prediksi mentah atau script h5, snapshot label lokal, environment yang mereproduksi baseline | h5 hanya CSV akhir. Membagi tiket akhir dengan 1,15 tidak mereproduksi pembulatan dan zero gate notebook. Snapshot serta environment sepadan tidak ada. **Belum dapat diuji.** |
| C. Hapus sekolah ×1,30 pada 25–26 Maret saja | Prediksi mentah h5 dan mask sekolah/off yang sama dengan pembuat h5 | CSV akhir tidak cukup untuk membalik pengali dan pembulatan secara eksak. Sekitar 709 baris yang disebut catatan tetap angka laporan, belum dihitung ulang sebagai efek MASE. **Belum dapat diuji.** |
| D. Ramadan ×0,7 | Aturan cohort terkunci, validasi berlabel yang relevan, dan jatah leaderboard | Bukti pasar dalam laporan hanya beberapa hari, sedangkan label D4–D10 test tidak ada. Tidak dipilih sebagai eksperimen spekulatif. **Tidak dijalankan.** |
| Satu model baru / blend OOF baru | Pipeline baseline lengkap, environment kompatibel, film-disjoint dan temporal OOF yang sama | Cache lama hanya memuat model yang sudah diuji. Snapshot Wikipedia hilang dan versi lingkungan tidak cocok; membuat model baru sekarang akan memutus perbandingan baseline. **Tidak dijalankan.** |

Tidak ada varian yang memperoleh angka MASE validasi baru. Mengubah faktor dari skor publik h5 saja akan memilih pada kira-kira 10% test, sedangkan 90% private tetap tersembunyi. Perubahan bentuk harian h6b dilaporkan mendapat 0,45806, lebih tinggi dari h5 0,45717, tetapi CSV dan protokolnya tidak ada di proyek ini.

## 5. Kandidat sementara dan langkah berikut

**Kandidat final sementara yang didukung validasi lokal adalah champion supply `submission_supply_hybrid_d4d7_w30.csv`.** Gain OOF terhadap v7 positif pada CV film dan split waktu, dengan paired SE yang dihitung dari film yang sama. h5 tetap **pemimpin skor publik terlapor**, tetapi koreksi Lebaran ×4 dipilih lewat beberapa probe leaderboard dan tidak memiliki analog validasi Lebaran 2026 yang memadai. Saya tidak menyimpulkan champion akan mengalahkan h5 pada private; keputusan akhir tetap berketidakpastian.

Langkah berdampak terbesar sebelum membuka eksperimen adalah memperoleh **CSV v9 dan label-fix beserta script/snapshot pembuat h5**, lalu mengaudit kesamaan pipeline dan mereproduksi satu baseline secara persis pada environment yang memang kompatibel. Sesudah itu kandidat A dapat diperiksa tanpa melatih model. Jika berkas itu tidak tersedia, berhenti pada dua submission yang ada dan jangan menyimpulkan gain dari volume prediksi.

## Artefak dan reproduksi audit

- `working/`: salinan identik berdasarkan SHA-256 untuk tiga CSV dan notebook asli, ditambah salinan cache OOF dari ZIP. File asli tetap utuh.
- `audit.py`: membaca salinan, template/test, dan cache; mencetak audit CSV, perbedaan prediksi, MASE OOF, paired SE, serta sumber loss. Jalankan dari direktori `final_joints_v2` dengan `.venv_seed\Scripts\python.exe KNOWLEDGE\audit_artefak_lanjutan_2026\audit.py`.
- `FINAL_REPORT.md`: keputusan ini. Skor publik bersumber dari laporan pengguna dan tidak dihitung oleh `audit.py`.

Tidak ada prediksi submission baru, model, dependency, environment, atau data eksternal baru yang dibuat atau diubah.
