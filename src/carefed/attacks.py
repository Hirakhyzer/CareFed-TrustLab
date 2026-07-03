from __future__ import annotations

import torch


def label_flip_frame(frame, fraction: float = 0.25, seed: int = 42):
    attacked = frame.copy()
    patients = attacked["patient_id"].drop_duplicates().sample(frac=fraction, random_state=seed)
    mask = attacked["patient_id"].isin(set(patients))
    attacked.loc[mask, "deterioration_label"] = 1 - attacked.loc[mask, "deterioration_label"]
    return attacked


def scale_update(update: dict[str, torch.Tensor], factor: float = 4.0) -> dict[str, torch.Tensor]:
    return {key: value * factor for key, value in update.items()}


def sign_flip_update(update: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {key: -value for key, value in update.items()}
