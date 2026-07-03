from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ["heart_rate", "systolic_bp", "respiratory_rate", "spo2", "temperature", "glucose", "mobility_score", "adherence", "care_contact_minutes"]
GROUPS = ["age_band", "sex", "care_setting", "site_id"]

@dataclass(frozen=True)
class SyntheticClinicalConfig:
    n_patients: int = 720
    n_sites: int = 6
    time_steps: int = 12
    seed: int = 42

def site_name(index: int) -> str:
    return "home-care-node" if index == 0 else f"hospital-{index:02d}"

def generate_synthetic_clinical_telemetry(config: SyntheticClinicalConfig | None = None) -> pd.DataFrame:
    cfg = config or SyntheticClinicalConfig()
    rng = np.random.default_rng(cfg.seed)
    rows = []
    for patient_idx in range(cfg.n_patients):
        site_index = patient_idx % cfg.n_sites
        site_id = site_name(site_index)
        care_setting = "home" if site_index == 0 else "hospital"
        age_band = rng.choice(["18-44", "45-64", "65-79", "80+"], p=[0.18, 0.31, 0.32, 0.19])
        sex = rng.choice(["female", "male"], p=[0.52, 0.48])
        chronic = rng.binomial(1, {"18-44": .18, "45-64": .34, "65-79": .52, "80+": .66}[age_band])
        social_risk = rng.beta(2.0 if care_setting == "home" else 1.5, 4.5)
        base = .12 + .10 * chronic + .18 * social_risk + (.06 if age_band in {"65-79", "80+"} else 0)
        patient_id = f"P{patient_idx + 1:05d}"
        for step in range(cfg.time_steps):
            trend = base + .16 * step / max(1, cfg.time_steps - 1) + rng.normal(0, .06)
            rows.append({
                "patient_id": patient_id, "time_step": step, "site_id": site_id,
                "care_setting": care_setting, "age_band": age_band, "sex": sex,
                "chronic_condition": chronic,
                "heart_rate": 74 + 22 * trend + rng.normal(0, 6),
                "systolic_bp": 124 - 24 * trend + rng.normal(0, 8),
                "respiratory_rate": 16 + 8 * trend + rng.normal(0, 2),
                "spo2": 97 - 6.5 * trend + rng.normal(0, 1.2),
                "temperature": 36.8 + 1.2 * trend + rng.normal(0, .22),
                "glucose": 105 + 30 * chronic + 20 * trend + rng.normal(0, 13),
                "mobility_score": np.clip(1 - .48 * trend - .18 * chronic + rng.normal(0, .08), 0, 1),
                "adherence": np.clip(.92 - .28 * social_risk - .12 * trend + rng.normal(0, .06), 0, 1),
                "care_contact_minutes": max(0, rng.normal(18 if care_setting == "home" else 34, 7) + 8 * trend),
            })
    frame = pd.DataFrame(rows)
    last = frame.sort_values("time_step").groupby("patient_id").tail(1)
    risk = .025*(last.heart_rate-80) + .08*(95-last.spo2) + .02*(115-last.systolic_bp) + .55*(1-last.mobility_score) + .25*(1-last.adherence) + .18*last.chronic_condition
    labels = (risk > risk.quantile(.72)).astype(int)
    frame["deterioration_label"] = frame["patient_id"].map(dict(zip(last.patient_id, labels))).astype(int)
    return frame

def patient_level_table(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values("time_step").groupby("patient_id").tail(1).reset_index(drop=True)

def split_by_patient(frame: pd.DataFrame, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    ids = np.array(sorted(frame.patient_id.unique()))
    rng.shuffle(ids)
    n_test = int(.2 * len(ids)); n_val = int(.2 * len(ids))
    test, val, train = set(ids[:n_test]), set(ids[n_test:n_test+n_val]), set(ids[n_test+n_val:])
    return frame[frame.patient_id.isin(train)].copy(), frame[frame.patient_id.isin(val)].copy(), frame[frame.patient_id.isin(test)].copy()

def site_partitions(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {site: group.copy() for site, group in frame.groupby("site_id", sort=True)}

def save_synthetic_dataset(path: str | Path, config: SyntheticClinicalConfig | None = None) -> pd.DataFrame:
    frame = generate_synthetic_clinical_telemetry(config)
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return frame
