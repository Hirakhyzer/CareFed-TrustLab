from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pandas as pd

from .federated import run_federated_experiment
from .visuals import save_calibration_figure, save_group_gap_figure, save_roc_figure


def privacy_utility_sweep(frame, base_config: dict, noise_multipliers: list[float]) -> pd.DataFrame:
    rows = []
    for noise in noise_multipliers:
        config = deepcopy(base_config)
        config["privacy_enabled"] = True
        config["noise_multiplier"] = float(noise)
        config["output_dir"] = str(Path(base_config.get("output_dir", "results")) / f"dp_noise_{noise:.2f}")
        result = run_federated_experiment(frame, config)
        rows.append({"noise_multiplier": noise, "epsilon": result["epsilon"], **result["metrics"]})
    return pd.DataFrame(rows)


def robustness_matrix(frame, base_config: dict, aggregators: list[str], attacks: list[str]) -> pd.DataFrame:
    rows = []
    for aggregator in aggregators:
        for attack in attacks:
            config = deepcopy(base_config)
            config["aggregation"] = aggregator
            config["attack"] = attack
            config["output_dir"] = str(Path(base_config.get("output_dir", "results")) / f"{aggregator}_{attack}")
            result = run_federated_experiment(frame, config)
            rows.append({"aggregation": aggregator, "attack": attack, "epsilon": result["epsilon"], **result["metrics"]})
    return pd.DataFrame(rows)


def export_experiment_bundle(result: dict, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([result["metrics"]]).to_csv(output_dir / "metrics.csv", index=False)
    result["audit"].to_csv(output_dir / "group_audit.csv", index=False)
    result["gaps"].to_csv(output_dir / "group_gap_summary.csv", index=False)
    result["explanations"].to_csv(output_dir / "integrated_gradients.csv", index=False)
    result["roc"].to_csv(output_dir / "roc.csv", index=False)
    result["pr"].to_csv(output_dir / "precision_recall.csv", index=False)
    result["calibration"].to_csv(output_dir / "calibration.csv", index=False)
    save_roc_figure(result["roc"], output_dir / "roc_curve.png")
    save_calibration_figure(result["calibration"], output_dir / "calibration_curve.png")
    save_group_gap_figure(result["gaps"], output_dir / "group_gaps.png")
