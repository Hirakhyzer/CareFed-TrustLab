from __future__ import annotations

import copy

import pandas as pd

from .data import patient_level_table, site_partitions, split_by_patient
from .evaluation import expected_calibration_error, select_threshold_by_f1
from .model import RiskModel, predict_scores, train_local
from .preprocessing import FeatureScaler, assert_patient_disjoint
from .trust import classification_metrics, group_audit, group_gap_summary
from .data import GROUPS


def run_centralized_baseline(frame: pd.DataFrame, seed: int = 42, epochs: int = 8, learning_rate: float = 0.01) -> dict:
    train, validation, test = split_by_patient(frame, seed=seed)
    assert_patient_disjoint(train, validation, test)
    scaler = FeatureScaler.fit(train)
    model = RiskModel(n_features=len(scaler.feature_names))
    train_local(model, train, scaler, epochs=epochs, lr=learning_rate)
    validation_labels, validation_scores = predict_scores(model, validation, scaler)
    threshold = select_threshold_by_f1(validation_labels, validation_scores)
    test_labels, test_scores = predict_scores(model, test, scaler)
    metrics = classification_metrics(test_labels, test_scores, threshold.threshold)
    metrics["ece"] = expected_calibration_error(test_labels, test_scores)
    table = patient_level_table(test).reset_index(drop=True)
    audit = group_audit(table, test_labels, test_scores, GROUPS, threshold.threshold)
    return {"name": "centralized", "metrics": metrics, "audit": audit, "gaps": group_gap_summary(audit)}


def run_local_site_baselines(frame: pd.DataFrame, seed: int = 42, epochs: int = 8, learning_rate: float = 0.01) -> pd.DataFrame:
    train, validation, test = split_by_patient(frame, seed=seed)
    assert_patient_disjoint(train, validation, test)
    rows = []
    for site_id, train_site in site_partitions(train).items():
        validation_site = validation[validation["site_id"] == site_id]
        test_site = test[test["site_id"] == site_id]
        if validation_site.empty or test_site.empty:
            continue
        scaler = FeatureScaler.fit(train_site)
        model = RiskModel(n_features=len(scaler.feature_names))
        train_local(model, train_site, scaler, epochs=epochs, lr=learning_rate)
        y_val, s_val = predict_scores(model, validation_site, scaler)
        threshold = select_threshold_by_f1(y_val, s_val)
        y_test, s_test = predict_scores(model, test_site, scaler)
        metric = classification_metrics(y_test, s_test, threshold.threshold)
        rows.append({"site_id": site_id, "n_train": train_site["patient_id"].nunique(), **metric})
    return pd.DataFrame(rows)
