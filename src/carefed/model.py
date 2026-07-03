from __future__ import annotations

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from .data import FEATURES, patient_level_table

class RiskModel(nn.Module):
    def __init__(self, n_features: int, hidden: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_features, hidden), nn.ReLU(), nn.Linear(hidden, 1))
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)

def frame_to_xy(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    table = patient_level_table(frame)
    x = table[FEATURES].to_numpy(dtype=np.float32)
    x = (x - x.mean(axis=0, keepdims=True)) / np.maximum(x.std(axis=0, keepdims=True), 1e-6)
    y = table["deterioration_label"].to_numpy(dtype=np.float32)
    return x, y

def train_local(model: nn.Module, frame: pd.DataFrame, epochs: int = 1, lr: float = 0.01) -> nn.Module:
    x, y = frame_to_xy(frame)
    loader = DataLoader(TensorDataset(torch.tensor(x), torch.tensor(y)), batch_size=32, shuffle=True)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        for xb, yb in loader:
            opt.zero_grad(set_to_none=True)
            loss = loss_fn(model(xb), yb)
            loss.backward(); opt.step()
    return model

def predict_scores(model: nn.Module, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    model.eval(); x, y = frame_to_xy(frame)
    with torch.no_grad():
        scores = torch.sigmoid(model(torch.tensor(x))).numpy()
    return y.astype(int), scores

def clone_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {k: v.detach().clone() for k, v in model.state_dict().items()}

def state_delta(before: dict[str, torch.Tensor], after: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {k: after[k].detach().clone() - before[k].detach().clone() for k in before}

def apply_delta(state: dict[str, torch.Tensor], delta: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {k: state[k] + delta[k] for k in state}
