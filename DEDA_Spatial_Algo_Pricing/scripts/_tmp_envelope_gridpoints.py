"""Compute per-envelope action-grid-point coverage for a strategic run.

Reconstructs the EXACT masked feasible price-point count each store faced, using
the same asymmetric-band + 2-point snap-and-widen logic as
hotelling.envelope.masking._allowed_grid_indices_asym (incl. optional tier floor).

Run:  conda activate py314 && python scripts/_tmp_envelope_gridpoints.py <RUN_DIR>
Writes: <RUN_DIR>/_envelope_gridpoint_stats.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd


def allowed_count_asym(grid: np.ndarray, centre: float, dp_minus: float, dp_plus: float) -> int:
    m = int(grid.shape[0])
    lo, hi = centre - dp_minus, centre + dp_plus
    idx = np.nonzero((grid >= lo) & (grid <= hi))[0]
    if idx.size >= 2:
        return int(idx.size)
    # snap-and-widen guarantees exactly 2 (degenerate m==1 -> 1)
    return 1 if m == 1 else 2


def main() -> None:
    run_dir = Path(sys.argv[1])
    env = pd.read_parquet(run_dir / "envelopes.parquet")
    grid = np.load(run_dir / "price_grid.npy")
    step = float(np.median(np.diff(grid)))

    cols = list(env.columns)
    # locate band columns robustly
    def pick(*cands):
        for c in cands:
            if c in env.columns:
                return c
        return None
    c_pbar = pick("p_bar", "pbar")
    c_dpm = pick("dp_minus", "dpm")
    c_dpp = pick("dp_plus", "dpp")
    c_dp = pick("delta_p", "dp")
    c_eps = pick("epsilon", "eps")
    c_epoch = pick("epoch")
    c_chain = pick("chain", "chain_id", "brand")

    # resolve widths: prefer asymmetric; fall back to symmetric delta_p
    def widths(row):
        dpm = row[c_dpm] if c_dpm and row[c_dpm] is not None and row[c_dpm] > 0 else None
        dpp = row[c_dpp] if c_dpp and row[c_dpp] is not None and row[c_dpp] > 0 else None
        if dpm is None or dpp is None:
            d = row[c_dp] if c_dp else np.nan
            dpm = dpm if dpm is not None else d
            dpp = dpp if dpp is not None else d
        return float(dpm), float(dpp)

    counts, euro_span, raw_ge2 = [], [], []
    for _, row in env.iterrows():
        dpm, dpp = widths(row)
        pbar = float(row[c_pbar])
        n = allowed_count_asym(grid, pbar, dpm, dpp)
        counts.append(n)
        euro_span.append(dpm + dpp)
        # how many grid pts the RAW euro band covered, before snap-and-widen
        lo, hi = pbar - dpm, pbar + dpp
        raw_ge2.append(int(np.count_nonzero((grid >= lo) & (grid <= hi))))

    counts = np.asarray(counts)
    raw = np.asarray(raw_ge2)
    euro = np.asarray(euro_span)

    def dist(a):
        vals, cnts = np.unique(a, return_counts=True)
        return {int(v): int(c) for v, c in zip(vals, cnts)}

    out = {
        "run": run_dir.name,
        "n_envelopes": int(len(env)),
        "grid_m": int(grid.shape[0]),
        "grid_step_eur": round(step, 4),
        "columns": cols,
        # masked (what stores actually faced, >=2 guaranteed)
        "masked_points_mean": round(float(counts.mean()), 4),
        "masked_points_median": float(np.median(counts)),
        "masked_points_min": int(counts.min()),
        "masked_points_max": int(counts.max()),
        "masked_points_dist": dist(counts),
        # raw euro-band coverage (before snap-and-widen) — reveals sub-2 bands
        "raw_points_mean": round(float(raw.mean()), 4),
        "raw_points_dist": dist(raw),
        "frac_bands_below_2_raw": round(float((raw < 2).mean()), 4),
        # euro span
        "euro_span_mean": round(float(euro.mean()), 4),
        "euro_span_median": round(float(np.median(euro)), 4),
        "euro_span_in_grid_steps_mean": round(float((euro / step).mean()), 4),
    }
    (run_dir / "_envelope_gridpoint_stats.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
