from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_curve


@dataclass(frozen=True)
class ThresholdSelection:
    threshold: float
    criterion: str
    validation_value: float


def select_threshold_by_f1(y_true: np.ndarray, scores: np.ndarray) -> ThresholdSelection:
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    if len(thresholds) == 0:
        return ThresholdSelection(0.5, "f1", float("nan"))
    f1 = 2 * precision[:-1] * recall[:-1] / np.maximum(precision[:-1] + recall[:-1], 1e-12)
    index = int(np.nanargmax(f1))
    return ThresholdSelection(float(thresholds[index]), "f1", float(f1[index]))


def expected_calibration_error(y_true: np.ndarray, scores: np.ndarray, bins: int = 10) -> float:
    y_true = np.asarray(y_true, dtype=float)
    scores = np.asarray(scores, dtype=float)
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for left, right in zip(edges[:-1], edges[1:]):
        mask = (scores >= left) & (scores < right if right < 1 else scores <= right)
        if not mask.any():
            continue
        ece += float(mask.mean()) * abs(float(scores[mask].mean()) - float(y_true[mask].mean()))
    return float(ece)


def curve_tables(y_true: np.ndarray, scores: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fpr, tpr, roc_threshold = roc_curve(y_true, scores)
    precision, recall, pr_threshold = precision_recall_curve(y_true, scores)
    observed, predicted = calibration_curve(y_true, scores, n_bins=10, strategy="quantile")
    roc = pd.DataFrame({"fpr": fpr, "tpr": tpr, "threshold": roc_threshold})
    pr = pd.DataFrame({"precision": precision, "recall": recall, "threshold": np.append(pr_threshold, np.nan)})
    calibration = pd.DataFrame({"mean_predicted_probability": predicted, "fraction_positive": observed})
    return roc, pr, calibration


def bootstrap_intervals(y_true: np.ndarray, scores: np.ndarray, metric, repetitions: int = 200, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    scores = np.asarray(scores)
    values = []
    for _ in range(repetitions):
        index = rng.integers(0, len(y_true), len(y_true))
        if len(np.unique(y_true[index])) < 2:
            continue
        values.append(float(metric(y_true[index], scores[index])))
    if not values:
        return float("nan"), float("nan")
    return tuple(np.quantile(values, [0.025, 0.975]).tolist())


def average_precision(y_true: np.ndarray, scores: np.ndarray) -> float:
    return float(average_precision_score(y_true, scores))
