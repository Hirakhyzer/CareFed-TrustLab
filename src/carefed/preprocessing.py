from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import FEATURES, patient_level_table


@dataclass
class FeatureScaler:
    mean: np.ndarray
    std: np.ndarray
    feature_names: list[str]

    @classmethod
    def fit(cls, frame: pd.DataFrame) -> "FeatureScaler":
        table = patient_level_table(frame)
        values = table[FEATURES].to_numpy(dtype=np.float32)
        return cls(
            mean=values.mean(axis=0),
            std=np.maximum(values.std(axis=0), 1e-6),
            feature_names=list(FEATURES),
        )

    def transform(self, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        table = patient_level_table(frame).reset_index(drop=True)
        values = table[self.feature_names].to_numpy(dtype=np.float32)
        x = (values - self.mean) / self.std
        y = table["deterioration_label"].to_numpy(dtype=np.float32)
        return x, y, table


def assert_patient_disjoint(*frames: pd.DataFrame) -> None:
    patient_sets = [set(frame["patient_id"].unique()) for frame in frames]
    for left in range(len(patient_sets)):
        for right in range(left + 1, len(patient_sets)):
            overlap = patient_sets[left].intersection(patient_sets[right])
            if overlap:
                raise ValueError(f"Patient leakage detected across splits: {len(overlap)} shared IDs.")


def longitudinal_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Create an interpretable patient-level summary from longitudinal records."""
    ordered = frame.sort_values(["patient_id", "time_step"])
    final = patient_level_table(ordered).set_index("patient_id")
    grouped = ordered.groupby("patient_id")[FEATURES]
    first = grouped.first().add_suffix("_first")
    last = grouped.last().add_suffix("_last")
    slope = (grouped.last() - grouped.first()).add_suffix("_delta")
    summary = pd.concat([first, last, slope], axis=1)
    static = final[["site_id", "care_setting", "age_band", "sex", "chronic_condition", "deterioration_label"]]
    return static.join(summary).reset_index()
