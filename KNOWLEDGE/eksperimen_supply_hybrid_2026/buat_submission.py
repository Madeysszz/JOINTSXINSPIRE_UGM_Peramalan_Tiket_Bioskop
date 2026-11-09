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
run_cell(38)


def predict(c):
    raw = 0.8 * ((c['m2'] + c['m3']) / 2) + 0.2 * c['tab']
    return np.where(c['p0'] > 0.55, 0, rnd(raw * K_LEVEL * faktor_sek * faktor_leb))


base = predict(komponen(np.ones(N, bool), TE, np.arange(len(St))))
v7 = pd.read_csv(ROOT / 'submission_v7_patuh_lebaran_x150.csv')
assert np.array_equal(te.id.to_numpy(), v7.id.to_numpy())
assert np.array_equal(base[ip, hj].astype(int), v7.total_ticket.to_numpy()), 'baseline tidak cocok dengan v7'
print('baseline cocok persis dengan v7', flush=True)

KOL.extend(['occ_trend', 'show_trend'])
supply = predict(komponen(np.ones(N, bool), TE, np.arange(len(St))))
weights = np.array([.30, .30, .30, .30, 0, 0, 0])
hybrid = np.floor((1 - weights) * base + weights * supply + .5).astype(int)
submission = pd.DataFrame({'id': te.id.to_numpy(), 'total_ticket': hybrid[ip, hj]})
assert len(submission) == len(sample) == 72611
assert np.array_equal(submission.id.to_numpy(), sample.id.to_numpy())
assert submission.total_ticket.notna().all() and (submission.total_ticket >= 0).all()
assert np.array_equal(submission.total_ticket.to_numpy()[hj >= 4], v7.total_ticket.to_numpy()[hj >= 4])
path = OUT / 'submission_supply_hybrid_d4d7_w30.csv'
submission.to_csv(path, index=False)
print('submission', path, 'rows', len(submission), 'changed', int((submission.total_ticket != v7.total_ticket).sum()),
      'total', int(submission.total_ticket.sum()), flush=True)
