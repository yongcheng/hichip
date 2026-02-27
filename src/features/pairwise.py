"""Pairwise feature construction from per-bin signals."""

from __future__ import annotations

import pandas as pd

from src.data.contracts import PAIR_FEATURE_COLUMNS


def build_pair_features(candidates_df: pd.DataFrame, bins_with_id_df: pd.DataFrame) -> pd.DataFrame:
    left = bins_with_id_df[["bin_id", "atac", "h3k27ac"]].rename(
        columns={"bin_id": "bin_id_left", "atac": "atac_left", "h3k27ac": "h3k27ac_left"}
    )
    right = bins_with_id_df[["bin_id", "atac", "h3k27ac"]].rename(
        columns={"bin_id": "bin_id_right", "atac": "atac_right", "h3k27ac": "h3k27ac_right"}
    )

    out = candidates_df.merge(left, on="bin_id_left", how="inner").merge(right, on="bin_id_right", how="inner")

    out["atac_mean"] = (out["atac_left"] + out["atac_right"]) / 2.0
    out["h3k27ac_mean"] = (out["h3k27ac_left"] + out["h3k27ac_right"]) / 2.0
    out["atac_product"] = out["atac_left"] * out["atac_right"]
    out["h3k27ac_product"] = out["h3k27ac_left"] * out["h3k27ac_right"]

    return out


def get_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in PAIR_FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing pairwise feature columns: {missing}")
    return df[PAIR_FEATURE_COLUMNS].copy()
