from __future__ import annotations

import numpy as np
import pandas as pd


def apply_site_shift(frame: pd.DataFrame, seed: int = 42, magnitude: float = 0.12) -> pd.DataFrame:
    """Create controlled non-IID site variation for robustness experiments."""
    rng = np.random.default_rng(seed)
    shifted = frame.copy()
    sites = sorted(shifted["site_id"].unique())
    for index, site in enumerate(sites):
        mask = shifted["site_id"] == site
        direction = -1 if index % 2 else 1
        shifted.loc[mask, "heart_rate"] += direction * magnitude * 18
        shifted.loc[mask, "systolic_bp"] -= direction * magnitude * 12
        shifted.loc[mask, "care_contact_minutes"] *= 1 + direction * magnitude * 0.4
        if site == "home-care-node":
            shifted.loc[mask, "medication_adherence"] = np.clip(
                shifted.loc[mask, "adherence"] - magnitude * 0.12, 0, 1
            )
            shifted.loc[mask, "adherence"] = shifted.loc[mask, "medication_adherence"]
    return shifted


def site_distribution_report(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values("time_step").groupby("site_id").agg(
        patients=("patient_id", "nunique"),
        observations=("patient_id", "size"),
        prevalence=("deterioration_label", "mean"),
        average_heart_rate=("heart_rate", "mean"),
        average_spo2=("spo2", "mean"),
    ).reset_index()
