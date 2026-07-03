from __future__ import annotations

import copy
from pathlib import Path

import pandas as pd
import torch

from .aggregation import append_audit_record, coordinate_median, fedavg, secure_aggregate, trimmed_mean
from .attacks import label_flip_frame, scale_update, sign_flip_update
from .data import GROUPS, patient_level_table, site_partitions, split_by_patient
from .evaluation import curve_tables, expected_calibration_error, select_threshold_by_f1
from .model import RiskModel, apply_delta, clone_state, predict_scores, state_delta, train_local
from .preprocessing import FeatureScaler, assert_patient_disjoint
from .privacy import add_dp_noise, approximate_epsilon, clip_update
from .trust import classification_metrics, group_audit, group_gap_summary


def choose_aggregator(name: str, updates: list[dict[str, torch.Tensor]], client_ids: list[str]) -> dict[str, torch.Tensor]:
    if name == "median":
        return coordinate_median(updates)
    if name == "trimmed_mean":
        return trimmed_mean(updates)
    if name == "secure_fedavg":
        return secure_aggregate(updates, client_ids)
    return fedavg(updates)


def run_federated_experiment(frame: pd.DataFrame, config: dict) -> dict:
    """Run a reproducible federated-learning experiment with explicit safeguards.

    The scaler is fitted on the training partition only. The alert threshold is
    selected on validation data and applied once to the held-out test partition.
    """
    train, validation, test = split_by_patient(frame, seed=int(config.get("seed", 42)))
    assert_patient_disjoint(train, validation, test)
    scaler = FeatureScaler.fit(train)
    train_sites = site_partitions(train)
    global_model = RiskModel(n_features=len(scaler.feature_names))
    output_dir = Path(config.get("output_dir", "results"))
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_path = output_dir / "audit_ledger.jsonl"
    rounds = int(config.get("rounds", 4))
    local_epochs = int(config.get("local_epochs", 2))
    learning_rate = float(config.get("learning_rate", 0.01))
    aggregation = config.get("aggregation", "fedavg")
    privacy_enabled = bool(config.get("privacy_enabled", True))
    attack = config.get("attack", "none")
    clip_norm = float(config.get("clip_norm", 1.0))
    noise_multiplier = float(config.get("noise_multiplier", 0.35))

    for round_id in range(1, rounds + 1):
        base_state = clone_state(global_model)
        updates: list[dict[str, torch.Tensor]] = []
        client_ids: list[str] = []
        client_sizes: list[float] = []
        for index, (site_id, site_frame) in enumerate(train_sites.items()):
            local_frame = label_flip_frame(site_frame, seed=round_id) if attack == "label_flip" and index == 0 else site_frame
            local = copy.deepcopy(global_model)
            train_local(local, local_frame, scaler, epochs=local_epochs, lr=learning_rate)
            delta = state_delta(base_state, clone_state(local))
            if attack == "scale_update" and index == 0:
                delta = scale_update(delta, 4.0)
            if attack == "sign_flip" and index == 0:
                delta = sign_flip_update(delta)
            if privacy_enabled:
                delta = clip_update(delta, clip_norm=clip_norm)
                delta = add_dp_noise(delta, clip_norm=clip_norm, noise_multiplier=noise_multiplier, seed=round_id * 100 + index)
            updates.append(delta)
            client_ids.append(site_id)
            client_sizes.append(float(site_frame["patient_id"].nunique()))
        if aggregation == "fedavg":
            merged = fedavg(updates, client_sizes)
        else:
            merged = choose_aggregator(aggregation, updates, client_ids)
        global_model.load_state_dict(apply_delta(base_state, merged))
        append_audit_record(audit_path, {
            "round": round_id,
            "clients": client_ids,
            "client_sizes": client_sizes,
            "aggregation": aggregation,
            "privacy_enabled": privacy_enabled,
            "clip_norm": clip_norm if privacy_enabled else None,
            "noise_multiplier": noise_multiplier if privacy_enabled else None,
            "attack": attack,
            "seed": config.get("seed", 42),
        })

    validation_labels, validation_scores = predict_scores(global_model, validation, scaler)
    threshold = select_threshold_by_f1(validation_labels, validation_scores)
    test_labels, test_scores = predict_scores(global_model, test, scaler)
    metrics = classification_metrics(test_labels, test_scores, threshold.threshold)
    metrics.update({
        "threshold": threshold.threshold,
        "validation_f1_at_threshold": threshold.validation_value,
        "ece": expected_calibration_error(test_labels, test_scores),
    })
    table = patient_level_table(test).reset_index(drop=True)
    audit = group_audit(table, test_labels, test_scores, GROUPS, threshold.threshold)
    gaps = group_gap_summary(audit)
    roc, pr, calibration = curve_tables(test_labels, test_scores)
    epsilon = approximate_epsilon(rounds, noise_multiplier) if privacy_enabled else float("inf")
    return {
        "model": global_model,
        "scaler": scaler,
        "metrics": metrics,
        "audit": audit,
        "gaps": gaps,
        "epsilon": epsilon,
        "threshold": threshold,
        "test_table": table,
        "scores": test_scores,
        "labels": test_labels,
        "roc": roc,
        "pr": pr,
        "calibration": calibration,
    }
