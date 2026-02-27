"""I/O utilities for loading bin features and loop labels."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.contracts import BIN_FEATURE_COLUMNS, LOOP_BEDPE_MIN_COLUMNS


def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".tsv", ".bed", ".bedpe"}:
        return pd.read_csv(path, sep="\t")
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file extension for: {path}")


def load_bin_features(path: str | Path) -> pd.DataFrame:
    """Load binned ATAC/H3K27ac features with strict required columns."""
    in_path = Path(path)
    df = _read_table(in_path)

    missing = [c for c in BIN_FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required bin feature columns: {missing}. "
            f"Expected columns include: {BIN_FEATURE_COLUMNS}"
        )

    out = df[BIN_FEATURE_COLUMNS].copy()
    out["start"] = out["start"].astype(int)
    out["end"] = out["end"].astype(int)
    out["atac"] = out["atac"].astype(float)
    out["h3k27ac"] = out["h3k27ac"].astype(float)
    return out


def load_loops_bedpe(path: str | Path) -> pd.DataFrame:
    """Load loop anchors from BEDPE-like table.

    Uses first six columns as anchor coordinates if names are absent.
    """
    in_path = Path(path)
    df = _read_table(in_path)

    if df.shape[1] < LOOP_BEDPE_MIN_COLUMNS:
        raise ValueError(
            f"BEDPE requires at least {LOOP_BEDPE_MIN_COLUMNS} columns, got {df.shape[1]}"
        )

    if {"chrom1", "start1", "end1", "chrom2", "start2", "end2"}.issubset(df.columns):
        out = df[["chrom1", "start1", "end1", "chrom2", "start2", "end2"]].copy()
    else:
        out = df.iloc[:, :6].copy()
        out.columns = ["chrom1", "start1", "end1", "chrom2", "start2", "end2"]

    out["start1"] = out["start1"].astype(int)
    out["end1"] = out["end1"].astype(int)
    out["start2"] = out["start2"].astype(int)
    out["end2"] = out["end2"].astype(int)
    return out
