from __future__ import annotations

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from .preprocessing import FeatureScaler


class RiskModel(nn.Module):
    def __init__(self, n_features: int, hidden: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.ReLU(),
            nn.Dropout(0.05),
            nn.Linear(hidden, hidden // 2),
            nn.ReLU(),
            nn.Linear(hidden // 2, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


def frame_to_xy(frame: pd.DataFrame, scaler: FeatureScaler) -> tuple[np.ndarray, np.ndarray]:
    x, y, _ = scaler.transform(frame)
    return x, y


def train_local(
    model: nn.Module,
    frame: pd.DataFrame,
    scaler: FeatureScaler,
    epochs: int = 1,
    lr: float = 0.01,
    batch_size: int = 32,
) -> nn.Module:
    x, y = frame_to_xy(frame, scaler)
    loader = DataLoader(TensorDataset(torch.tensor(x), torch.tensor(y)), batch_size=batch_size, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        for xb, yb in loader:
            optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(model(xb), yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()
    return model


def predict_scores(model: nn.Module, frame: pd.DataFrame, scaler: FeatureScaler) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    x, y = frame_to_xy(frame, scaler)
    with torch.no_grad():
        scores = torch.sigmoid(model(torch.tensor(x))).numpy()
    return y.astype(int), scores


def clone_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {key: value.detach().clone() for key, value in model.state_dict().items()}


def state_delta(before: dict[str, torch.Tensor], after: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {key: after[key].detach().clone() - before[key].detach().clone() for key in before}


def apply_delta(state: dict[str, torch.Tensor], delta: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {key: state[key] + delta[key] for key in state}
