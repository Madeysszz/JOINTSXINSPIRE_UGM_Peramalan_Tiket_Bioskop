import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
os.chdir(ROOT)
NOTEBOOK = json.loads((ROOT / 'Inference_Terbaru_Dani.ipynb').read_text(encoding='utf-8'))


def run_cell(i, before=None):
    source = ''.join(NOTEBOOK['cells'][i]['source'])
    if before:
        source = source.split(before)[0]
    exec(compile(source, f'notebook_cell_{i}', 'exec'), globals())


display = lambda x: None
run_cell(2)
assert (DATA / 'external/wiki_daftar_film_indonesia_2025_oldid27901699.wikitext').exists()
run_cell(4)
run_cell(7)
run_cell(9, 'import matplotlib.dates')
run_cell(12, '# pembanding:')
ncl_tr = pd.Series(1, index=range(N)).groupby(film).transform('sum').values
ncl_te = pd.Series(1, index=range(len(T))).groupby(T.index.get_level_values(0).values).transform('sum').values
run_cell(20)
run_cell(22)
run_cell(24)
run_cell(25)


def supply_trends(frame, pairs):
    values = {}
    for col in ['occupation_rate', 'total_show']:
        pivot = frame.pivot_table(index=['movie_title', 'cinema_ids'], columns='h', values=col, aggfunc='mean')
        pivot = pivot.reindex(pairs).reindex(columns=range(3)).fillna(0)
        values[col] = np.log1p(pivot[2]) - np.log1p(pivot[[0, 1]].mean(axis=1))
    return pd.DataFrame(values, index=pairs)


for target, source, pairs in [(F_tr, d[d.h < 3], U.index), (F_te, hh[hh.h < 3], pair_te)]:
    trends = supply_trends(source, pairs)
    target['occ_trend'] = trends.occupation_rate.to_numpy()
    target['show_trend'] = trends.total_show.to_numpy()
run_cell(27)


def predict(c, factor):
    raw = 0.8 * ((c['m2'] + c['m3']) / 2) + 0.2 * c['tab']
    return np.where(c['p0'] > 0.55, 0, rnd(raw * factor))


dates = np.asarray(U.d1.values, dtype='datetime64[D]')[:, None] + np.array(H, dtype='timedelta64[D]')[None, :]
school = np.isin(dates, np.arange(D_('2025-06-28'), D_('2025-07-13')))
factor = 1.15 * np.where(school & (M_tr['off'] == 0), 1.30, 1.0)


def oof():
    cv = np.zeros_like(Y)
    temporal = np.zeros_like(Y)
    raw_cv = np.zeros_like(Y)
    raw_temporal = np.zeros_like(Y)
    for k in range(5):
        a, v = fk != k, fk == k
        idx = np.where(v)[0]
        c = komponen(a, TR, idx)
        cv[v] = predict(c, factor[v])
        raw_cv[v] = predict(c, 1.0)
        print('fold', k + 1, 'selesai', flush=True)
    idx = np.where(e_akhir)[0]
    c = komponen(f_awal, TR, idx)
    temporal[e_akhir] = predict(c, factor[e_akhir])
    raw_temporal[e_akhir] = predict(c, 1.0)
    print('split waktu selesai', flush=True)
    return cv, temporal, raw_cv, raw_temporal


baseline = oof()
KOL.extend(['occ_trend', 'show_trend'])
supply = oof()
np.savez_compressed(OUT / 'oof_dani_supply.npz',
                    base_cv=baseline[0], base_time=baseline[1], base_cv_raw=baseline[2], base_time_raw=baseline[3],
                    supply_cv=supply[0], supply_time=supply[1], supply_cv_raw=supply[2], supply_time_raw=supply[3],
                    y=Y, scale=S, weight=W_NILAI, film=np.asarray(film, dtype=str),
                    time_mask=e_akhir, dow=M_tr['dow'], release_width=ncl_tr,
                    local=TR.lokal, d1=np.asarray(U.d1.values, dtype='datetime64[D]'))
print('OOF disimpan', flush=True)
