"""XGBoost model wrapper for binary loop prediction."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score
from xgboost import XGBClassifier


def train_xgb(x_train: np.ndarray, y_train: np.ndarray, params: dict[str, Any]) -> XGBClassifier:
    model = XGBClassifier(**params)
    model.fit(x_train, y_train)
    return model


def evaluate_binary(model: XGBClassifier, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    prob = model.predict_proba(x)[:, 1]
    out: dict[str, float] = {}
    out["pr_auc"] = float(average_precision_score(y, prob)) if len(set(y)) > 1 else float("nan")
    out["roc_auc"] = float(roc_auc_score(y, prob)) if len(set(y)) > 1 else float("nan")
    out["n"] = float(len(y))
    out["positives"] = float(np.sum(y))
    return out
