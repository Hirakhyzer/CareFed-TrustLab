from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = [
    "heart_rate", "oxygen_saturation", "respiratory_rate", "temperature_c",
    "systolic_bp", "activity_index", "device_signal_quality",
]

SITE_METADATA: Mapping[str, dict[str, str]] = {
    "hospital_north": {"care_setting": "hospital"},
    "hospital_south": {"care_setting": "hospital"},
    "homecare_west": {"care_setting": "home_care"},
    "homecare_east": {"care_setting": "home_care"},
}


@dataclass(frozen=True)
class SyntheticClinicalConfig:
    n_sites: int = 4
    episodes_per_site: int = 72
    sequence_length: int = 20
    frequency_minutes: int = 15
    seed: int = 42


@dataclass
class WindowSet:
    x: np.ndarray
    y: np.ndarray
    site_id: np.ndarray
    care_setting: np.ndarray
    age_group: np.ndarray
    sex_group: np.ndarray
    timestamp: np.ndarray
    episode_id: np.ndarray

    def subset(self, mask: np.ndarray) -> "WindowSet":
        return WindowSet(
            x=self.x[mask], y=self.y[mask], site_id=self.site_id[mask],
            care_setting=self.care_setting[mask], age_group=self.age_group[mask],
            sex_group=self.sex_group[mask], timestamp=self.timestamp[mask],
            episode_id=self.episode_id[mask],
        )


def _site_ids(n_sites: int) -> list[str]:
    if n_sites < 2 or n_sites > len(SITE_METADATA):
        raise ValueError(f"n_sites must be between 2 and {len(SITE_METADATA)}.")
    return list(SITE_METADATA)[:n_sites]


def generate_synthetic_clinical_telemetry(config: SyntheticClinicalConfig | None = None) -> pd.DataFrame:
    """Generate fully synthetic connected-health telemetry for research methods.

    This dataset is not patient data, not clinically validated, and is unsuitable
    for medical decisions. Labels are simulated future-event proxies only.
    """
    config = config or SyntheticClinicalConfig()
    if config.episodes_per_site < 12 or config.sequence_length < 14:
        raise ValueError("Use at least 12 episodes per site and 14 observations per episode.")
    rng = np.random.default_rng(config.seed)
    records: list[dict[str, object]] = []
    start = pd.Timestamp("2026-01-01 00:00:00")

    for site_index, site_id in enumerate(_site_ids(config.n_sites)):
        setting = SITE_METADATA[site_id]["care_setting"]
        site_shift = (site_index - 1.5) * 0.18
        setting_shift = 0.35 if setting == "home_care" else 0.0
        for episode_index in range(config.episodes_per_site):
            episode_id = f"{site_id}-episode-{episode_index:03d}"
            patient_id = f"synthetic-{site_index + 1:02d}-{episode_index:03d}"
            episode_start = start + pd.Timedelta(hours=episode_index * 3 + site_index)
            age_group = str(rng.choice(["adult", "older_adult", "senior"], p=[0.34, 0.40, 0.26]))
            sex_group = str(rng.choice(["female", "male", "other"], p=[0.48, 0.48, 0.04]))
            age_shift = {"adult": 0.0, "older_adult": 0.24, "senior": 0.48}[age_group]
            event_probability = 0.16 + 0.05 * (setting == "home_care") + 0.07 * (age_group == "senior")
            event = bool(rng.random() < event_probability)
            onset = int(rng.integers(config.sequence_length // 2, config.sequence_length - 3)) if event else -1
            baseline = {
                "heart_rate": 72 + rng.normal(0, 4) + 2.0 * age_shift + site_shift,
                "oxygen_saturation": 97.0 + rng.normal(0, 0.7) - 0.25 * age_shift,
                "respiratory_rate": 15.5 + rng.normal(0, 1.1) + 0.3 * age_shift,
                "temperature_c": 36.8 + rng.normal(0, 0.18),
                "systolic_bp": 121 + rng.normal(0, 8) + 5 * age_shift,
                "activity_index": 0.70 + rng.normal(0, 0.06) - 0.07 * age_shift - setting_shift * 0.05,
                "device_signal_quality": 0.93 + rng.normal(0, 0.025) - setting_shift * 0.02,
            }
            for step in range(config.sequence_length):
                timestamp = episode_start + pd.Timedelta(minutes=config.frequency_minutes * step)
                ramp = 0.0 if onset < 0 or step < onset else (step - onset + 1) / max(1, config.sequence_length - onset)
                records.append({
                    "timestamp": timestamp, "episode_start": episode_start, "episode_id": episode_id,
                    "patient_id_synthetic": patient_id, "site_id": site_id, "care_setting": setting,
                    "age_group": age_group, "sex_group": sex_group, "step": step,
                    "proxy_deterioration_label": int(onset >= 0 and step >= onset), "event_onset_step": onset,
                    "heart_rate": baseline["heart_rate"] + rng.normal(0, 3.2) + 28 * ramp,
                    "oxygen_saturation": baseline["oxygen_saturation"] + rng.normal(0, 0.65) - 5.4 * ramp,
                    "respiratory_rate": baseline["respiratory_rate"] + rng.normal(0, 1.0) + 8.0 * ramp,
                    "temperature_c": baseline["temperature_c"] + rng.normal(0, 0.12) + 1.0 * ramp,
                    "systolic_bp": baseline["systolic_bp"] + rng.normal(0, 6.0) - 23 * ramp,
                    "activity_index": baseline["activity_index"] + rng.normal(0, 0.045) - 0.42 * ramp,
                    "device_signal_quality": baseline["device_signal_quality"] + rng.normal(0, 0.018) - 0.10 * ramp,
                })
    frame = pd.DataFrame.from_records(records)
    frame["oxygen_saturation"] = frame["oxygen_saturation"].clip(70, 100)
    frame["activity_index"] = frame["activity_index"].clip(0, 1)
    frame["device_signal_quality"] = frame["device_signal_quality"].clip(0.4, 1)
    return frame.sort_values(["episode_start", "site_id", "step"]).reset_index(drop=True)


def validate_synthetic_frame(frame: pd.DataFrame) -> None:
    required = set(FEATURE_COLUMNS + ["timestamp", "episode_start", "episode_id", "site_id", "care_setting", "age_group", "sex_group", "proxy_deterioration_label"])
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if frame[FEATURE_COLUMNS].isna().any().any():
        raise ValueError("Feature values cannot be missing.")
    if not set(frame["proxy_deterioration_label"].unique()).issubset({0, 1}):
        raise ValueError("proxy_deterioration_label must be binary.")


def split_episodes_chronologically(frame: pd.DataFrame, train_fraction: float = 0.60, validation_fraction: float = 0.20) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split complete episodes by time; no episode may span multiple partitions."""
    validate_synthetic_frame(frame)
    if not (0 < train_fraction < 1 and 0 < validation_fraction < 1 and train_fraction + validation_fraction < 1):
        raise ValueError("Fractions must be positive and leave a test interval.")
    episodes = frame[["episode_id", "episode_start"]].drop_duplicates().sort_values("episode_start")
    train_end, validation_end = int(len(episodes) * train_fraction), int(len(episodes) * (train_fraction + validation_fraction))
    ids = [set(episodes.iloc[:train_end].episode_id), set(episodes.iloc[train_end:validation_end].episode_id), set(episodes.iloc[validation_end:].episode_id)]
    return (
        frame[frame.episode_id.isin(ids[0])].copy(),
        frame[frame.episode_id.isin(ids[1])].copy(),
        frame[frame.episode_id.isin(ids[2])].copy(),
    )


def make_prediction_windows(frame: pd.DataFrame, window_size: int = 12, horizon: int = 3) -> WindowSet:
    """Create windows labelled by a simulated event in the future prediction horizon."""
    validate_synthetic_frame(frame)
    if window_size < 4 or horizon < 1:
        raise ValueError("window_size must be >= 4 and horizon must be >= 1.")
    windows: list[np.ndarray] = []
    labels: list[int] = []
    metadata = {key: [] for key in ["site_id", "care_setting", "age_group", "sex_group", "timestamp", "episode_id"]}
    for episode_id, group in frame.sort_values(["episode_id", "timestamp"]).groupby("episode_id", sort=True):
        group = group.reset_index(drop=True)
        values = group[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
        target = group.proxy_deterioration_label.to_numpy(dtype=np.int64)
        for end in range(window_size - 1, len(group) - horizon):
            windows.append(values[end - window_size + 1 : end + 1])
            labels.append(int(target[end + 1 : end + horizon + 1].max()))
            row = group.iloc[end]
            metadata["site_id"].append(row.site_id)
            metadata["care_setting"].append(row.care_setting)
            metadata["age_group"].append(row.age_group)
            metadata["sex_group"].append(row.sex_group)
            metadata["timestamp"].append(row.timestamp)
            metadata["episode_id"].append(episode_id)
    if not windows:
        raise ValueError("Not enough observations to form windows.")
    return WindowSet(
        x=np.stack(windows).astype(np.float32), y=np.asarray(labels, dtype=np.int64),
        site_id=np.asarray(metadata["site_id"], dtype=str), care_setting=np.asarray(metadata["care_setting"], dtype=str),
        age_group=np.asarray(metadata["age_group"], dtype=str), sex_group=np.asarray(metadata["sex_group"], dtype=str),
        timestamp=np.asarray(metadata["timestamp"]), episode_id=np.asarray(metadata["episode_id"], dtype=str),
    )


def fit_train_scaler(train: WindowSet) -> StandardScaler:
    if len(train.x) == 0:
        raise ValueError("Cannot fit a scaler without training windows.")
    return StandardScaler().fit(train.x.reshape(-1, train.x.shape[-1]))


def transform_windows(dataset: WindowSet, scaler: StandardScaler) -> WindowSet:
    shape = dataset.x.shape
    x = scaler.transform(dataset.x.reshape(-1, shape[-1])).reshape(shape).astype(np.float32)
    return WindowSet(x=x, y=dataset.y.copy(), site_id=dataset.site_id.copy(), care_setting=dataset.care_setting.copy(), age_group=dataset.age_group.copy(), sex_group=dataset.sex_group.copy(), timestamp=dataset.timestamp.copy(), episode_id=dataset.episode_id.copy())


def partition_by_site(dataset: WindowSet) -> dict[str, WindowSet]:
    return {site: dataset.subset(dataset.site_id == site) for site in sorted(np.unique(dataset.site_id))}
