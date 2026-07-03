from __future__ import annotations

import numpy as np
import pandas as pd
import torch

from .data import FEATURES


def integrated_gradients(model, x: np.ndarray, steps: int = 64, baseline: np.ndarray | None = None) -> np.ndarray:
    """Dependency-light Integrated Gradients for binary risk scores."""
    model.eval()
    values = torch.tensor(x, dtype=torch.float32)
    base = torch.zeros_like(values) if baseline is None else torch.tensor(baseline, dtype=torch.float32)
    total_gradients = torch.zeros_like(values)
    for alpha in torch.linspace(0, 1, steps):
        point = (base + alpha * (values - base)).detach().requires_grad_(True)
        score = torch.sigmoid(model(point)).sum()
        score.backward()
        total_gradients += point.grad.detach()
    return ((values - base) * total_gradients / steps).detach().numpy()


def feature_attribution_table(attributions: np.ndarray, feature_names: list[str] | None = None) -> pd.DataFrame:
    names = feature_names or FEATURES
    mean_abs = np.mean(np.abs(attributions), axis=0)
    signed = np.mean(attributions, axis=0)
    return pd.DataFrame({"feature": names, "mean_absolute_attribution": mean_abs, "mean_signed_attribution": signed}).sort_values("mean_absolute_attribution", ascending=False)
