"""Label construction by mapping loops onto bin pairs."""

from __future__ import annotations

import pandas as pd

from src.data.candidates import make_bin_id


def _binize_anchor(chrom: str, start: int, end: int, resolution_bp: int) -> str:
    mid = (start + end) // 2
    bstart = (mid // resolution_bp) * resolution_bp
    bend = bstart + resolution_bp
    return f"{chrom}:{bstart}-{bend}"


def build_positive_pair_set(loops_df: pd.DataFrame, resolution_bp: int) -> set[tuple[str, str, str]]:
    """Build canonical positive pair keys as (chrom, left_bin_id, right_bin_id)."""
    positives: set[tuple[str, str, str]] = set()
    for row in loops_df.itertuples(index=False):
        if row.chrom1 != row.chrom2:
            continue

        a = _binize_anchor(row.chrom1, int(row.start1), int(row.end1), resolution_bp)
        b = _binize_anchor(row.chrom2, int(row.start2), int(row.end2), resolution_bp)
        left, right = sorted([a, b])
        positives.add((row.chrom1, left, right))
    return positives


def assign_binary_labels(candidates_df: pd.DataFrame, positive_set: set[tuple[str, str, str]]) -> pd.DataFrame:
    """Assign binary y labels to candidate pairs."""
    out = candidates_df.copy()
    keys = zip(out["chrom"], out["bin_id_left"], out["bin_id_right"])
    out["label"] = [1 if k in positive_set else 0 for k in keys]
    return out


def attach_bin_ids(bin_df: pd.DataFrame) -> pd.DataFrame:
    out = bin_df.copy()
    out["bin_id"] = make_bin_id(out["chrom"], out["start"], out["end"])
    return out
