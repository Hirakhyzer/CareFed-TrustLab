from __future__ import annotations

import copy
from pathlib import Path

import pandas as pd
import torch

from .aggregation import append_audit_record, coordinate_median, fedavg, secure_aggregate, trimmed_mean
from .attacks import label_flip_frame, scale_update, sign_flip_update
from .data import GROUPS, patient_level_table, site_partitions, split_by_patient
from .model import RiskModel, apply_delta, clone_state, predict_scores, state_delta, train_local
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
    train, validation, test = split_by_patient(frame, seed=int(config.get("seed", 42)))
    train_sites = site_partitions(train)
    global_model = RiskModel(n_features=9)
    audit_path = Path(config.get("output_dir", "results")) / "audit_ledger.jsonl"
    rounds = int(config.get("rounds", 4))
    local_epochs = int(config.get("local_epochs", 2))
    lr = float(config.get("learning_rate", 0.01))
    aggregation = config.get("aggregation", "fedavg")
    privacy_enabled = bool(config.get("privacy_enabled", True))
    attack = config.get("attack", "none")

    for round_id in range(1, rounds + 1):
        base_state = clone_state(global_model)
        updates = []
        client_ids = []
        for idx, (site_id, site_frame) in enumerate(train_sites.items()):
            local_frame = label_flip_frame(site_frame, seed=round_id) if attack == "label_flip" and idx == 0 else site_frame
            local = copy.deepcopy(global_model)
            train_local(local, local_frame, epochs=local_epochs, lr=lr)
            delta = state_delta(base_state, clone_state(local))
            if attack == "scale_update" and idx == 0:
                delta = scale_update(delta, 4.0)
            if attack == "sign_flip" and idx == 0:
                delta = sign_flip_update(delta)
            if privacy_enabled:
                delta = add_dp_noise(clip_update(delta), seed=round_id + idx)
            updates.append(delta); client_ids.append(site_id)
        merged = choose_aggregator(aggregation, updates, client_ids)
        global_model.load_state_dict(apply_delta(base_state, merged))
        append_audit_record(audit_path, {"round": round_id, "clients": client_ids, "aggregation": aggregation, "privacy": privacy_enabled, "attack": attack})

    y_true, scores = predict_scores(global_model, test)
    metrics = classification_metrics(y_true, scores)
    table = patient_level_table(test).reset_index(drop=True)
    audit = group_audit(table, y_true, scores, GROUPS)
    gaps = group_gap_summary(audit)
    epsilon = approximate_epsilon(rounds, float(config.get("noise_multiplier", 0.35))) if privacy_enabled else float("inf")
    return {"model": global_model, "metrics": metrics, "audit": audit, "gaps": gaps, "epsilon": epsilon, "test_table": table, "scores": scores, "labels": y_true}
