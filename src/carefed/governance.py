from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

import pandas as pd


@dataclass(frozen=True)
class DataUseDeclaration:
    dataset_name: str
    contains_real_patient_data: bool
    intended_use: str
    prohibited_uses: list[str]
    retention_note: str
    sharing_boundary: str


def default_data_use_declaration() -> DataUseDeclaration:
    return DataUseDeclaration(
        dataset_name="synthetic_connected_health",
        contains_real_patient_data=False,
        intended_use="Method development, reproducible evaluation, teaching, and research prototyping.",
        prohibited_uses=["Clinical deployment", "Patient care decisions", "Performance claims on real populations"],
        retention_note="Generated artifacts should be versioned or deleted according to the experiment plan.",
        sharing_boundary="Only synthetic data and aggregate experiment outputs are expected in this repository.",
    )


def validate_export_table(table: pd.DataFrame, allowed_columns: set[str]) -> None:
    disallowed = set(table.columns).difference(allowed_columns)
    if disallowed:
        raise ValueError(f"Export contains disallowed columns: {sorted(disallowed)}")


def write_governance_record(path: str | Path, declaration: DataUseDeclaration | None = None) -> None:
    payload = asdict(declaration or default_data_use_declaration())
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
