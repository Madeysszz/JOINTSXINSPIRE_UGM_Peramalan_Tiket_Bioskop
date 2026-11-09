from hashlib import sha256
from io import BytesIO
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
DATA = ROOT / "dataset"
NAMES = {
    "v7": "submission_v7_patuh_lebaran_x150.csv",
    "champion": "submission_supply_hybrid_d4d7_w30.csv",
    "h5": "diag_h5_v9_leb400.csv",
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def score(y, pred, scale, weight=None):
    loss = np.abs(y - pred) / np.maximum(scale[:, None], 1)
    if weight is None:
        return float(loss.mean())
    return float(np.average(loss.mean(axis=1), weights=weight))


def film_se(y, baseline, candidate, scale, film, weight=None):
    delta = (np.abs(y - baseline) - np.abs(y - candidate)) / np.maximum(scale[:, None], 1)
    delta = delta.mean(axis=1)
    w = np.ones(len(delta)) if weight is None else weight
    estimate = np.average(delta, weights=w)
    table = pd.DataFrame({"film": film, "d": delta * w, "w": w}).groupby("film").sum()
    influence = (table.d - estimate * table.w) / w.sum()
    n = len(table)
    return float(estimate), float(np.sqrt(n / (n - 1) * np.sum(influence**2)))


def main():
    test = pd.read_csv(DATA / "test.csv", dtype={"id": "int64", "cinema_ids": str})
    sample = pd.read_csv(DATA / "sample_submission.csv")
    history = pd.read_csv(DATA / "test_history.csv", usecols=["movie_title", "cinema_ids", "date_show"], dtype={"cinema_ids": str})
    assert len(test) == len(sample) == 72611
    assert test.id.is_unique and sample.id.is_unique
    assert test.id.equals(sample.id)
    assert test.groupby(["movie_title", "cinema_ids"]).size().eq(7).all()
    d1 = pd.to_datetime(history.groupby("movie_title").date_show.min())
    test["date_show"] = pd.to_datetime(test.date_show)
    test["horizon"] = (test.date_show - test.movie_title.map(d1)).dt.days + 1
    assert test.horizon.between(4, 10).all()

    audit = test[["id", "movie_title", "cinema_ids", "city_name", "date_show", "horizon"]].copy()
    checks = []
    for name, filename in NAMES.items():
        path = ROOT / filename
        frame = pd.read_csv(path)
        assert frame.columns.tolist() == sample.columns.tolist()
        assert len(frame) == 72611 and frame.id.is_unique
        assert frame.id.equals(sample.id)
        values = frame.total_ticket.to_numpy()
        assert np.isfinite(values).all() and (values >= 0).all()
        assert (values == np.floor(values)).all()
        audit[name] = frame.set_index("id").loc[audit.id, "total_ticket"].to_numpy(dtype=np.int64)
        checks.append({"name": name, "rows": len(frame), "zeros": int((values == 0).sum()),
                       "min": int(values.min()), "max": int(values.max()), "sum": int(values.sum()), "sha256": sha(path)})
    pd.DataFrame(checks).to_csv(OUT / "SOURCE_CHECKS.csv", index=False)

    start = pd.Timestamp("2026-03-21")
    audit["period"] = np.where(audit.date_show >= start, "from_2026-03-21", "before_2026-03-21")
    for pair in ("h5", "v7"), ("champion", "v7"), ("h5", "champion"):
        a, b = pair
        audit[f"delta_{a}_{b}"] = audit[a] - audit[b]
    audit.to_csv(OUT / "PREDICTION_AUDIT_BY_ID.csv", index=False)

    rows = []
    for field in ("period", "date_show", "horizon", "movie_title", "cinema_ids"):
        for group, sub in audit.groupby(field, sort=True):
            for a, b in (("h5", "v7"), ("champion", "v7"), ("h5", "champion")):
                d = sub[a] - sub[b]
                rows.append({"group_field": field, "group_value": str(group), "comparison": f"{a}-{b}",
                             "rows": len(sub), "changed": int((d != 0).sum()), "raised": int((d > 0).sum()),
                             "lowered": int((d < 0).sum()), "net_tickets": int(d.sum()),
                             "absolute_tickets": int(d.abs().sum()), "base_tickets": int(sub[b].sum()),
                             "comparison_tickets": int(sub[a].sum())})
    pd.DataFrame(rows).to_csv(OUT / "AUDIT_GROUPS.csv", index=False)

    eid = audit[audit.date_show >= start]
    positive = eid.v7 > 0
    ratio = eid.loc[positive, "h5"] / eid.loc[positive, "v7"]
    p = eid.loc[positive, "v7"].to_numpy()
    q = eid.loc[positive, "h5"].to_numpy()
    overlap = np.maximum((p - .5) / 1.5, (q - .5) / 4) < np.minimum((p + .5) / 1.5, (q + .5) / 4)
    pd.DataFrame([{"eid_rows": len(eid), "eid_films": eid.movie_title.nunique(),
                   "eid_cinemas": eid.cinema_ids.nunique(), "h5_v7_positive_rows": int(positive.sum()),
                   "h5_v7_ratio_median": float(ratio.median()), "h5_v7_ratio_q25": float(ratio.quantile(.25)),
                   "h5_v7_ratio_q75": float(ratio.quantile(.75)),
                   "rounding_interval_compatible": int(overlap.sum()),
                   "rounding_interval_incompatible": int((~overlap).sum())}]).to_csv(OUT / "RATIO_DIAGNOSTIC.csv", index=False)

    sensitivity = []
    for factor in (1.5, 2.0, 2.5, 3.0, 4.0):
        values = np.floor(eid.v7.to_numpy() * factor / 1.5 + .5).astype(np.int64)
        sensitivity.append({"assumed_leb_factor": factor, "eid_rows": len(values),
                            "eid_zeros": int((values == 0).sum()), "eid_tickets": int(values.sum()),
                            "uplift_vs_v7_eid": int(values.sum() - eid.v7.sum()),
                            "total_submission_tickets": int(audit.v7.sum() - eid.v7.sum() + values.sum())})
    day = (eid.date_show - start).dt.days.to_numpy()
    daily = np.array([2.45, 2.21, 2.04, 2.45, 1.82, 1.75, 1.60])
    values = np.floor(eid.v7.to_numpy() * daily[day] / 1.5 + .5).astype(np.int64)
    sensitivity.append({"assumed_leb_factor": "daily", "eid_rows": len(values),
                        "eid_zeros": int((values == 0).sum()), "eid_tickets": int(values.sum()),
                        "uplift_vs_v7_eid": int(values.sum() - eid.v7.sum()),
                        "total_submission_tickets": int(audit.v7.sum() - eid.v7.sum() + values.sum())})
    pd.DataFrame(sensitivity).to_csv(OUT / "LEBARAN_SCENARIOS.csv", index=False)

    archive = ROOT / "ARSIP_LENGKAP_PERCOBAAN.zip"
    with ZipFile(archive) as z:
        data = z.read("KNOWLEDGE/eksperimen_supply_hybrid_2026/oof_dani_supply.npz")
    with np.load(BytesIO(data), allow_pickle=False) as cached:
        arrays = {key: cached[key] for key in cached.files}
    base = arrays["base_cv"]
    supply = arrays["supply_cv"]
    champion = base.copy()
    champion[:, :4] = np.floor(.7 * base[:, :4] + .3 * supply[:, :4] + .5)
    base_t = arrays["base_time"]
    supply_t = arrays["supply_time"]
    champion_t = base_t.copy()
    champion_t[:, :4] = np.floor(.7 * base_t[:, :4] + .3 * supply_t[:, :4] + .5)
    mask = arrays["time_mask"]
    y, scale, weight, film = (arrays[k] for k in ("y", "scale", "weight", "film"))
    candidates = [("Dani v7 OOF", base, base_t, "REFERENCE"),
                  ("Champion supply D4-D7 w0.30", champion, champion_t, "CHAMPION")]
    for multiplier in (.85, .90, .95, 1.0, 1.05, 1.10, 1.15):
        if multiplier == 1:
            continue
        candidates.append((f"Champion output x{multiplier:.2f}",
                           np.floor(champion * multiplier + .5),
                           np.floor(champion_t * multiplier + .5),
                           "EXPLORATORY" if multiplier < 1 else "REJECT"))
    result = []
    for name, pred, pred_t, status in candidates:
        delta, se = film_se(y, champion, pred, scale, film, weight)
        tdelta, tse = film_se(y[mask], champion_t[mask], pred_t[mask], scale[mask], film[mask], weight[mask])
        result.append({"candidate": name, "cv_mase": score(y, pred, scale),
                       "weighted_cv_mase": score(y, pred, scale, weight),
                       "weighted_delta_vs_champion": delta, "paired_se_film": se,
                       "temporal_mase": score(y[mask], pred_t[mask], scale[mask]),
                       "temporal_weighted_mase": score(y[mask], pred_t[mask], scale[mask], weight[mask]),
                       "temporal_weighted_delta": tdelta, "temporal_paired_se_film": tse,
                       "positive_target_mase": float((np.abs(y[y > 0] - pred[y > 0]) /
                                                      np.broadcast_to(np.maximum(scale[:, None], 1), y.shape)[y > 0]).mean()),
                       "zero_target_mase": float((pred[y == 0] /
                                                  np.broadcast_to(np.maximum(scale[:, None], 1), y.shape)[y == 0]).mean()),
                       "status": status})
    pd.DataFrame(result).to_csv(OUT / "EXPERIMENT_RESULTS.csv", index=False)

    source = ROOT / NAMES["champion"]
    target = OUT / "submission_best_validated.csv"
    copyfile(source, target)
    assert sha(source) == sha(target)
    print(pd.DataFrame(checks).to_string(index=False))
    print("\nRATIO", float(ratio.median()), int(overlap.sum()), int((~overlap).sum()))
    print("\nCV", pd.DataFrame(result).to_string(index=False))
    print("\nCHAMPION_SHA", sha(target))


if __name__ == "__main__":
    main()
