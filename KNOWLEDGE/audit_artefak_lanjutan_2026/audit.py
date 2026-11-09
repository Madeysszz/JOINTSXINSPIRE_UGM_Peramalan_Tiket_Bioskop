import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
WORK = Path(__file__).resolve().parent / "working"

sample = pd.read_csv(ROOT / "dataset/sample_submission.csv")
test = pd.read_csv(ROOT / "dataset/test.csv", parse_dates=["date_show"])
submissions = {
    name: pd.read_csv(WORK / filename)
    for name, filename in {
        "v7": "submission_v7_patuh_lebaran_x150.csv",
        "champion": "submission_supply_hybrid_d4d7_w30.csv",
        "h5": "diag_h5_v9_leb400.csv",
    }.items()
}

result = {"test_dates": [str(test.date_show.min().date()), str(test.date_show.max().date())]}
for name, submission in submissions.items():
    values = submission.total_ticket
    result[name] = {
        "rows": len(submission),
        "id_order_matches_sample": submission.id.equals(sample.id),
        "id_order_matches_test": submission.id.equals(test.id),
        "unique_ids": submission.id.nunique(),
        "missing": int(submission.isna().sum().sum()),
        "negative": int((values < 0).sum()),
        "fractional": int((values % 1 != 0).sum()),
        "zero": int((values == 0).sum()),
        "min": int(values.min()),
        "max": int(values.max()),
        "total": int(values.sum()),
    }

eid = test.date_show >= "2026-03-21"
for left, right in (("h5", "v7"), ("champion", "v7"), ("h5", "champion")):
    difference = submissions[left].total_ticket - submissions[right].total_ticket
    result[f"{left}_minus_{right}"] = {
        "changed": int((difference != 0).sum()),
        "absolute_tickets": int(difference.abs().sum()),
        "net_tickets": int(difference.sum()),
        "changed_before_eid": int((difference[~eid] != 0).sum()),
        "changed_eid": int((difference[eid] != 0).sum()),
        "net_before_eid": int(difference[~eid].sum()),
        "net_eid": int(difference[eid].sum()),
    }

cache = np.load(WORK / "oof_dani_supply.npz", allow_pickle=False)
base = cache["base_cv"]
supply = cache["supply_cv"]
champion = base.copy()
champion[:, :4] = np.floor(0.7 * base[:, :4] + 0.3 * supply[:, :4] + 0.5)
y = cache["y"]
scale = cache["scale"][:, None]
weight = cache["weight"][:, None]
loss_base = abs(y - base) / scale
loss_champion = abs(y - champion) / scale


def mase(loss, weights, mask=None):
    if mask is None:
        mask = np.ones(loss.shape[0], dtype=bool)
    return float(np.sum(loss[mask] * weights[mask]) / np.sum(np.broadcast_to(weights[mask], loss[mask].shape)))


time = cache["time_mask"]
base_time = cache["base_time"][time]
supply_time = cache["supply_time"][time]
champion_time = base_time.copy()
champion_time[:, :4] = np.floor(0.7 * base_time[:, :4] + 0.3 * supply_time[:, :4] + 0.5)
loss_base_time = abs(y[time] - base_time) / scale[time]
loss_champion_time = abs(y[time] - champion_time) / scale[time]

film = cache["film"]
pair_gain = np.sum((loss_base - loss_champion) * weight, axis=1)
pair_weight = np.full(len(film), 7) * weight[:, 0]
delta = pair_gain.sum() / pair_weight.sum()
film_gain = pd.DataFrame({"film": film, "gain": pair_gain, "weight": pair_weight}).groupby("film").sum()
influence = film_gain.gain - delta * film_gain.weight
groups = len(film_gain)
paired_se = float(np.sqrt(groups / (groups - 1) * np.square(influence).sum()) / pair_weight.sum())
time_film = film[time]
time_pair_gain = np.sum((loss_base_time - loss_champion_time) * weight[time], axis=1)
time_pair_weight = np.full(len(time_film), 7) * weight[time, 0]
time_delta = time_pair_gain.sum() / time_pair_weight.sum()
time_group = pd.DataFrame({"film": time_film, "gain": time_pair_gain, "weight": time_pair_weight}).groupby("film").sum()
time_influence = time_group.gain - time_delta * time_group.weight
time_se = float(np.sqrt(len(time_group) / (len(time_group) - 1) * np.square(time_influence).sum()) / time_pair_weight.sum())

weighted_loss = loss_champion * weight
loss_by_film = pd.DataFrame({"film": np.repeat(film, 7), "loss": weighted_loss.ravel()}).groupby("film").loss.sum().sort_values(ascending=False)
result["oof"] = {
    "pairs": len(film),
    "films": groups,
    "ordinary_base": mase(loss_base, np.ones_like(weight)),
    "ordinary_champion": mase(loss_champion, np.ones_like(weight)),
    "weighted_base": mase(loss_base, weight),
    "weighted_champion": mase(loss_champion, weight),
    "weighted_gain": float(delta),
    "paired_se_film": paired_se,
    "temporal_pairs": int(time.sum()),
    "temporal_films": len(time_group),
    "temporal_ordinary_base": mase(loss_base_time, np.ones_like(weight[time])),
    "temporal_ordinary_champion": mase(loss_champion_time, np.ones_like(weight[time])),
    "temporal_weighted_base": mase(loss_base_time, weight[time]),
    "temporal_weighted_champion": mase(loss_champion_time, weight[time]),
    "temporal_weighted_gain": float(time_delta),
    "temporal_paired_se_film": time_se,
    "horizon_weighted_champion": [mase(loss_champion[:, i : i + 1], weight) for i in range(7)],
    "horizon_weighted_gain": [mase(loss_base[:, i : i + 1], weight) - mase(loss_champion[:, i : i + 1], weight) for i in range(7)],
    "loss_share_d4_d7": float(weighted_loss[:, :4].sum() / weighted_loss.sum()),
    "loss_share_scale_le_50": float(weighted_loss[cache["scale"] <= 50].sum() / weighted_loss.sum()),
    "pairs_scale_le_50": int((cache["scale"] <= 50).sum()),
    "weighted_mase_scale_le_50": mase(loss_champion, weight, cache["scale"] <= 50),
    "weighted_mase_scale_gt_50": mase(loss_champion, weight, cache["scale"] > 50),
    "loss_share_actual_zero": float(weighted_loss[y == 0].sum() / weighted_loss.sum()),
    "actual_zero_fraction": float((y == 0).mean()),
    "weighted_mase_actual_zero": float(weighted_loss[y == 0].sum() / np.broadcast_to(weight, y.shape)[y == 0].sum()),
    "weighted_mase_actual_positive": float(weighted_loss[y > 0].sum() / np.broadcast_to(weight, y.shape)[y > 0].sum()),
    "loss_share_top_5_films": float(loss_by_film.head(5).sum() / weighted_loss.sum()),
    "top_5_film_loss_share": {name: float(value / weighted_loss.sum()) for name, value in loss_by_film.head(5).items()},
}

print(json.dumps(result, indent=2))
