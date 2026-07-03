from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_roc_figure(roc: pd.DataFrame, destination: str | Path, title: str = "ROC curve") -> None:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 5))
    axis.plot(roc["fpr"], roc["tpr"], label="Federated model")
    axis.plot([0, 1], [0, 1], linestyle="--", label="Chance")
    axis.set(xlabel="False positive rate", ylabel="True positive rate", title=title, xlim=(0, 1), ylim=(0, 1))
    axis.legend()
    figure.tight_layout()
    figure.savefig(destination, dpi=220)
    plt.close(figure)


def save_calibration_figure(calibration: pd.DataFrame, destination: str | Path) -> None:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 5))
    axis.plot(calibration["mean_predicted_probability"], calibration["fraction_positive"], marker="o", label="Model")
    axis.plot([0, 1], [0, 1], linestyle="--", label="Perfect calibration")
    axis.set(xlabel="Mean predicted probability", ylabel="Observed frequency", title="Calibration curve", xlim=(0, 1), ylim=(0, 1))
    axis.legend()
    figure.tight_layout()
    figure.savefig(destination, dpi=220)
    plt.close(figure)


def save_group_gap_figure(gaps: pd.DataFrame, destination: str | Path) -> None:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    plot = gaps.set_index("attribute")[["positive_rate_gap", "recall_gap", "f1_gap"]]
    figure, axis = plt.subplots(figsize=(8, 4.8))
    plot.plot(kind="bar", ax=axis)
    axis.set(xlabel="Audit attribute", ylabel="Maximum observed gap", title="Trustworthiness subgroup gaps", ylim=(0, 1))
    figure.tight_layout()
    figure.savefig(destination, dpi=220)
    plt.close(figure)


def save_privacy_utility_figure(summary: pd.DataFrame, destination: str | Path) -> None:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6.5, 4.8))
    axis.plot(summary["epsilon"], summary["f1"], marker="o")
    axis.set(xlabel="Approximate privacy budget epsilon", ylabel="F1 score", title="Privacy-utility trade-off")
    figure.tight_layout()
    figure.savefig(destination, dpi=220)
    plt.close(figure)
