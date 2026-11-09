# Pemilihan model

Semua angka di bawah memakai cache OOF v7/supply yang sama: 7.354 pasangan, tujuh horizon, 171 film; temporal subset 4.060 pasangan dari 90 film. MASE biasa mengikuti rumus kompetisi pada pseudo-target train. Weighted MASE adalah diagnostik distribusi test, bukan skor resmi. Delta positif berarti kandidat lebih baik dari champion; SE berpasangan dikelompokkan menurut film.

| Kandidat | CV MASE | Weighted CV | Delta weighted ± SE | Temporal MASE | Temporal weighted | Status |
|---|---:|---:|---:|---:|---:|---|
| Dani v7 OOF | 0,378009 | 0,491313 | −0,000809 ± 0,000333 | 0,345563 | 0,411498 | REFERENCE |
| Champion supply D4–D7 w0,30 | **0,377017** | 0,490504 | acuan | **0,344536** | 0,410331 | CHAMPION |
| Champion output ×0,85 | 0,366872 | **0,483002** | +0,007501 ± 0,004888 | 0,328216 | **0,398933** | EXPLORATORY |
| Champion output ×0,90 | 0,368112 | 0,483646 | +0,006857 ± 0,003227 | 0,331256 | 0,400730 | EXPLORATORY |
| Champion output ×0,95 | 0,371654 | 0,486368 | +0,004136 ± 0,001608 | 0,336900 | 0,404785 | EXPLORATORY |
| Champion output ×1,05 | 0,384346 | 0,496376 | −0,005872 ± 0,001617 | 0,354062 | 0,417524 | REJECT |
| Champion output ×1,10 | 0,393570 | 0,503964 | −0,013460 ± 0,003246 | 0,365355 | 0,426519 | REJECT |
| Champion output ×1,15 | 0,404093 | 0,512586 | −0,022082 ± 0,004794 | 0,377888 | 0,436643 | REJECT |

Pengali C1 di atas diterapkan **relatif terhadap output champion yang sudah digerbang dan dibulatkan**, bukan mengganti `K_LEVEL` di pipeline mentah. Ini mengubah prediksi positif saja. Pada ×0,90, gain weighted per horizon D4–D10 semuanya positif: 0,01473; 0,00890; 0,00998; 0,00706; 0,00361; 0,00173; 0,00199. Temporal weighted juga membaik 0,009601 ± 0,003476. Ada 114 film dengan kontribusi gain positif, 55 negatif, dua nol; lima film teratas menyumbang 71,1% **net gain**. MASE biasa untuk target nol turun 0,162174→0,146295, sedangkan pada target positif turun 0,478979→0,473384. Gain rata-rata ada pada ketiga bin skala dan ketiga bin lebar rilis, tetapi bin skala kecil punya lebih sedikit pasangan.

**Keputusan:** tidak ada kandidat baru berstatus `PROMOTE`. ×0,90 dan ×0,95 tampak baik pada cache yang sudah dipakai berulang kali, tetapi enam titik grid ini dilihat pada fold dan split waktu yang tidak lagi independen. Audit kalibrasi terdahulu sudah menguji pengali serupa secara crossfit: global gain 0,007444 ± 0,004672, di bawah ambang dua SE, dan kontrol pengali acak antarfilm hampir sama baik. Pemilihan ×0,90/×0,95 sekarang akan memakai ulang validasi yang sudah terbuka untuk memilih level. Konsentrasi lima film serta pergeseran train–test menambah ketidakpastian transfer. Angka CV terbaik ×0,85 sendiri hanya 1,53 SE dari champion.

`p0` OOF/test tidak disimpan, sehingga C2 tidak dapat mengubah ambang nol secara sah. Eksperimen gerbang sebelumnya tidak memberi hasil stabil. C5 horizon calibration telah diuji crossfit sebelumnya dan tidak mengalahkan global secara meyakinkan. Komponen HGB/XGBoost/tabel serta `p0` yang sepadan di OOF **dan** test tidak tersedia untuk bobot ensemble baru pada fase D. Paket `.venv_seed` dapat membaca CSV/NPZ, tetapi versi dependensinya berbeda dari run lama, snapshot label Wikipedia tidak ada, dan notebook gabungan memakai path `data/`; karena reproduksi baseline mentah tidak memenuhi syarat, fase tuning model D/E dilewati. Tidak ada model baru yang dilatih.

CSV h5 berstatus `UNVERIFIABLE` untuk promosi berbasis validasi lokal: skor publik 0,45717 dilaporkan, dan perubahan per-ID telah diaudit, tetapi tidak ada OOF h5, skrip h5, atau analog Lebaran 2026 berlabel yang memadai. Ini tidak menyatakan h5 kalah pada private. Keputusan fallback menurut protokol prompt utama adalah mempertahankan champion yang memiliki OOF sepadan dan CSV test utuh.
