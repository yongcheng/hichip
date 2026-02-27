"""Candidate pair generation for loop prediction."""

from __future__ import annotations

import pandas as pd


def make_bin_id(chrom: pd.Series, start: pd.Series, end: pd.Series) -> pd.Series:
    return chrom.astype(str) + ":" + start.astype(str) + "-" + end.astype(str)


def generate_candidate_pairs(
    bins_df: pd.DataFrame,
    distance_min_bp: int,
    distance_max_bp: int,
) -> pd.DataFrame:
    """Generate intra-chromosomal candidate bin pairs within distance bounds."""
    required = {"chrom", "start", "end"}
    if not required.issubset(bins_df.columns):
        raise ValueError(f"bins_df missing required columns: {sorted(required)}")

    bins = bins_df.copy()
    bins = bins.sort_values(["chrom", "start", "end"]).reset_index(drop=True)
    bins["bin_id"] = make_bin_id(bins["chrom"], bins["start"], bins["end"])
    bins["mid"] = ((bins["start"] + bins["end"]) // 2).astype(int)

    pairs: list[dict[str, object]] = []
    for chrom, grp in bins.groupby("chrom", sort=False):
        mids = grp["mid"].to_numpy()
        ids = grp["bin_id"].to_numpy()

        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                dist = int(mids[j] - mids[i])
                if dist < distance_min_bp:
                    continue
                if dist > distance_max_bp:
                    break
                pairs.append(
                    {
                        "chrom": chrom,
                        "bin_id_left": ids[i],
                        "bin_id_right": ids[j],
                        "distance_bp": dist,
                    }
                )

    return pd.DataFrame(pairs)
