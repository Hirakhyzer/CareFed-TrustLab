from __future__ import annotations

import hashlib
import json
from pathlib import Path

import torch


def fedavg(updates: list[dict[str, torch.Tensor]], weights: list[float] | None = None) -> dict[str, torch.Tensor]:
    if not updates:
        raise ValueError("At least one update is required.")
    if weights is None:
        weights = [1.0 / len(updates)] * len(updates)
    total = sum(weights)
    weights = [w / total for w in weights]
    return {key: sum(w * update[key] for update, w in zip(updates, weights)) for key in updates[0]}


def coordinate_median(updates: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    return {key: torch.stack([u[key] for u in updates]).median(dim=0).values for key in updates[0]}


def trimmed_mean(updates: list[dict[str, torch.Tensor]], trim_ratio: float = 0.2) -> dict[str, torch.Tensor]:
    n = len(updates)
    trim = int(n * trim_ratio)
    result = {}
    for key in updates[0]:
        stacked = torch.stack([u[key] for u in updates])
        sorted_values, _ = torch.sort(stacked, dim=0)
        kept = sorted_values[trim:n-trim] if trim and n > 2 * trim else sorted_values
        result[key] = kept.mean(dim=0)
    return result


def make_pairwise_mask(shape: torch.Size, seed: str) -> torch.Tensor:
    digest = hashlib.sha256(seed.encode()).digest()
    int_seed = int.from_bytes(digest[:8], "big") % (2**31)
    generator = torch.Generator().manual_seed(int_seed)
    return torch.normal(0.0, 0.01, size=shape, generator=generator)


def secure_aggregate(updates: list[dict[str, torch.Tensor]], client_ids: list[str]) -> dict[str, torch.Tensor]:
    """Toy secure aggregation simulation for an honest-but-curious coordinator.

    Pairwise masks cancel in the sum. This is a teaching prototype, not a complete MPC implementation.
    """
    masked = [{key: value.clone() for key, value in update.items()} for update in updates]
    for i, left in enumerate(client_ids):
        for j, right in enumerate(client_ids):
            if i >= j:
                continue
            seed = f"{left}|{right}"
            for key in updates[0]:
                mask = make_pairwise_mask(updates[0][key].shape, seed + key)
                masked[i][key] += mask
                masked[j][key] -= mask
    return fedavg(masked)


def hash_payload(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def append_audit_record(path: str | Path, record: dict) -> dict:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    previous_hash = None
    if path.exists():
        lines = [line for line in path.read_text().splitlines() if line.strip()]
        if lines:
            previous_hash = json.loads(lines[-1])["record_hash"]
    enriched = {**record, "previous_hash": previous_hash}
    enriched["record_hash"] = hash_payload(enriched)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(enriched, sort_keys=True) + "\n")
    return enriched
