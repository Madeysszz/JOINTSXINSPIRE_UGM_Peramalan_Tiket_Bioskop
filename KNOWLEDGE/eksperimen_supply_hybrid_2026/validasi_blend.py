from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path(__file__).resolve().parent
z = np.load(OUT / 'oof_dani_supply.npz')
y, scale, weight, film = z['y'], z['scale'], z['weight'], z['film']
time_mask = z['time_mask']
all_mask = np.ones(len(y), bool)
base_cv, supply_cv = z['base_cv'], z['supply_cv']
base_time, supply_time = z['base_time'], z['supply_time']


def blend(base, supply, weights):
    w = np.asarray(weights)[None, :]
    return np.floor((1 - w) * base + w * supply + .5)


def score(pred, base, mask, cell_mask=None):
    if cell_mask is None:
        cell_mask = np.ones_like(y, bool)
    selected = mask[:, None] & cell_mask
    err = np.abs(y - pred) / np.maximum(scale[:, None], 1)
    ref = np.abs(y - base) / np.maximum(scale[:, None], 1)
    row_weight = np.broadcast_to(weight[:, None], y.shape)
    return err[selected].mean(), np.average(err[selected], weights=row_weight[selected]), np.average(ref[selected] - err[selected], weights=row_weight[selected])


def paired_se(pred, base, mask):
    improvement = (np.abs(y - base) - np.abs(y - pred)) / np.maximum(scale[:, None], 1)
    f = pd.DataFrame({'film': film[mask], 'wv': improvement[mask].mean(axis=1) * weight[mask], 'w': weight[mask]})
    group = f.groupby('film')[['wv', 'w']].sum()
    delta = group.wv.sum() / group.w.sum()
    influence = (group.wv - delta * group.w) / group.w.sum()
    return np.sqrt(len(group) / (len(group) - 1) * (influence ** 2).sum())


def evaluate(name, weights):
    cv = blend(base_cv, supply_cv, weights)
    temporal = blend(base_time, supply_time, weights)
    ordinary_cv, weighted_cv, delta_cv = score(cv, base_cv, all_mask)
    ordinary_time, weighted_time, delta_time = score(temporal, base_time, time_mask)
    row = dict(variant=name, horizon='D4-D' + str(max(i + 4 for i, v in enumerate(weights) if v > 0)),
               supply_weight='/'.join(f'{v:.2f}' for v in weights),
               cv_mase=ordinary_cv, weighted_cv=weighted_cv, delta_cv=delta_cv,
               paired_se_cv=paired_se(cv, base_cv, all_mask),
               temporal_mase=ordinary_time, temporal_weighted=weighted_time,
               delta_temporal=delta_time, paired_se_temporal=paired_se(temporal, base_time, time_mask))
    detail = []
    for split, pred, base, mask in [('CV', cv, base_cv, all_mask), ('temporal', temporal, base_time, time_mask)]:
        groups = {'all': np.ones(len(y), bool), 'scale_<=20': scale <= 20,
                  'scale_21_100': (scale > 20) & (scale <= 100), 'scale_>100': scale > 100,
                  'release_<=40': z['release_width'] <= 40, 'release_>70': z['release_width'] > 70}
        for group_name, group_mask in groups.items():
            selected = mask & group_mask
            if selected.any():
                for horizon in range(7):
                    cell = np.zeros_like(y, bool)
                    cell[:, horizon] = True
                    ordinary, weighted, delta = score(pred, base, selected, cell)
                    detail.append(dict(variant=name, split=split, group=group_name, horizon=horizon + 4,
                                       n_pairs=int(selected.sum()), mase=ordinary, weighted_mase=weighted, delta=delta))
        for group_name, group_cell in [('weekday', z['dow'] < 5), ('weekend', z['dow'] >= 5)]:
            ordinary, weighted, delta = score(pred, base, mask, group_cell)
            detail.append(dict(variant=name, split=split, group=group_name, horizon=0,
                               n_pairs=int((mask[:, None] & group_cell).sum()), mase=ordinary,
                               weighted_mase=weighted, delta=delta))
        err_base = (np.abs(y[mask] - base[mask]) / np.maximum(scale[mask, None], 1)).ravel()
        err_pred = (np.abs(y[mask] - pred[mask]) / np.maximum(scale[mask, None], 1)).ravel()
        row['tail_p95_' + split] = np.quantile(err_pred, .95) - np.quantile(err_base, .95)
    return row, detail


baseline_cv = score(base_cv, base_cv, all_mask)
baseline_time = score(base_time, base_time, time_mask)
variants = [(f'D4-D7 w={w:.2f}', [w] * 4 + [0] * 3) for w in [.10, .20, .30, .40, .50]]
stage = [evaluate(name, weights) for name, weights in variants]
best_row = min(stage, key=lambda result: result[0]['weighted_cv'])[0]
chosen_w = float(best_row['variant'].split('=')[1])
variants.append((f'D4-D9 w={chosen_w:.2f}', [chosen_w] * 6 + [0]))
variants.append(('Horizon-specific', [.25, .35, .35, .30, .10, .10, 0]))
results = stage + [evaluate(*variant) for variant in variants[5:]]
summary = pd.DataFrame([row for row, _ in results])
summary.to_csv(OUT / 'hasil_blend.csv', index=False)
pd.DataFrame([row for _, details in results for row in details]).to_csv(OUT / 'rincian_blend.csv', index=False)
print('baseline CV ordinary/weighted', baseline_cv[:2])
print('baseline temporal ordinary/weighted', baseline_time[:2])
print(summary[['variant', 'weighted_cv', 'delta_cv', 'paired_se_cv',
               'temporal_weighted', 'delta_temporal', 'paired_se_temporal',
               'tail_p95_CV', 'tail_p95_temporal']].to_string(index=False))
