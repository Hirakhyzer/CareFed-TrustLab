from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, precision_score, recall_score, roc_auc_score


def classification_metrics(y_true: np.ndarray, scores: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    pred = (scores >= threshold).astype(int)
    result = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "brier": float(brier_score_loss(y_true, scores)),
    }
    try:
        result["roc_auc"] = float(roc_auc_score(y_true, scores))
    except ValueError:
        result["roc_auc"] = float("nan")
    return result


def group_audit(table: pd.DataFrame, y_true: np.ndarray, scores: np.ndarray, columns: list[str], threshold: float = 0.5) -> pd.DataFrame:
    work = table.copy().reset_index(drop=True)
    work["y_true"] = y_true; work["score"] = scores; work["prediction"] = (scores >= threshold).astype(int)
    rows = []
    for column in columns:
        for value, group in work.groupby(column, sort=True):
            rows.append({
                "attribute": column, "group": value, "n": int(len(group)),
                "prevalence": float(group.y_true.mean()),
                "positive_rate": float(group.prediction.mean()),
                "recall": float(recall_score(group.y_true, group.prediction, zero_division=0)),
                "f1": float(f1_score(group.y_true, group.prediction, zero_division=0)),
                "mean_score": float(group.score.mean()),
            })
    return pd.DataFrame(rows)


def group_gap_summary(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for attribute, group in audit.groupby("attribute"):
        rows.append({
            "attribute": attribute,
            "positive_rate_gap": float(group.positive_rate.max() - group.positive_rate.min()),
            "recall_gap": float(group.recall.max() - group.recall.min()),
            "f1_gap": float(group.f1.max() - group.f1.min()),
        })
    return pd.DataFrame(rows)
