"""Training pipeline for v1 XGBoost loop predictor."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from xgboost import XGBClassifier

from src.data.candidates import generate_candidate_pairs
from src.data.io import load_bin_features, load_loops_bedpe
from src.data.labels import assign_binary_labels, attach_bin_ids, build_positive_pair_set
from src.features.pairwise import build_pair_features, get_feature_matrix
from src.models.xgb_model import evaluate_binary, train_xgb


def _load_config(config_path: str | Path) -> dict[str, Any]:
    cfg_path = Path(config_path)
    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if "extends" not in cfg:
        return cfg

    base_name = cfg["extends"]
    base_path = cfg_path.parent / base_name
    with base_path.open("r", encoding="utf-8") as f:
        base_cfg = yaml.safe_load(f)

    merged = base_cfg.copy()
    for k, v in cfg.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = {**merged[k], **v}
        else:
            merged[k] = v
    return merged


def _subset_by_chrom(df, chroms: list[str]):
    return df[df["chrom"].isin(chroms)].copy()


def run_xgb_pipeline(config_path: str | Path) -> dict[str, Any]:
    cfg = _load_config(config_path)

    bin_df = load_bin_features(cfg["paths"]["bin_features_path"])
    loop_df = load_loops_bedpe(cfg["paths"]["loops_bedpe_path"])

    bins_with_id = attach_bin_ids(bin_df)
    candidates = generate_candidate_pairs(
        bins_with_id,
        distance_min_bp=int(cfg["distance_min_bp"]),
        distance_max_bp=int(cfg["distance_max_bp"]),
    )

    positives = build_positive_pair_set(loop_df, resolution_bp=int(cfg["resolution_bp"]))
    labeled = assign_binary_labels(candidates, positives)
    feat_df = build_pair_features(labeled, bins_with_id)

    train_df = _subset_by_chrom(feat_df, cfg["split"]["train_chroms"])
    val_df = _subset_by_chrom(feat_df, cfg["split"]["val_chroms"])
    test_df = _subset_by_chrom(feat_df, cfg["split"]["test_chroms"])

    x_train = get_feature_matrix(train_df).to_numpy()
    y_train = train_df["label"].to_numpy()

    x_val = get_feature_matrix(val_df).to_numpy()
    y_val = val_df["label"].to_numpy()

    x_test = get_feature_matrix(test_df).to_numpy()
    y_test = test_df["label"].to_numpy()

    model = train_xgb(x_train, y_train, params=cfg["params"])
    metrics = {
        "val": evaluate_binary(model, x_val, y_val),
        "test": evaluate_binary(model, x_test, y_test),
    }

    out_dir = Path(cfg["paths"]["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    model_path = out_dir / "xgb_model.json"
    metrics_path = out_dir / "metrics.json"
    cfg_copy_path = out_dir / "resolved_config.yaml"

    model: XGBClassifier
    model.save_model(model_path)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    with cfg_copy_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

    return {
        "metrics": metrics,
        "model_path": str(model_path),
        "metrics_path": str(metrics_path),
        "resolved_config_path": str(cfg_copy_path),
        "n_train": int(len(train_df)),
        "n_val": int(len(val_df)),
        "n_test": int(len(test_df)),
    }
