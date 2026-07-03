from __future__ import annotations

import math
import torch


def clip_update(delta: dict[str, torch.Tensor], clip_norm: float = 1.0) -> dict[str, torch.Tensor]:
    total = torch.sqrt(sum(torch.sum(v.float() ** 2) for v in delta.values()))
    scale = min(1.0, float(clip_norm / (total + 1e-12)))
    return {k: v * scale for k, v in delta.items()}


def add_dp_noise(delta: dict[str, torch.Tensor], clip_norm: float = 1.0, noise_multiplier: float = 0.35, seed: int = 42) -> dict[str, torch.Tensor]:
    generator = torch.Generator().manual_seed(seed)
    std = clip_norm * noise_multiplier
    return {k: v + torch.normal(0.0, std, size=v.shape, generator=generator) for k, v in delta.items()}


def approximate_epsilon(rounds: int, noise_multiplier: float, delta: float = 1e-5, sample_rate: float = 1.0) -> float:
    if noise_multiplier <= 0:
        return float("inf")
    return float(sample_rate * math.sqrt(2 * rounds * math.log(1 / delta)) / noise_multiplier)
