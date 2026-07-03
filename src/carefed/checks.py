from __future__ import annotations

from .aggregation import append_audit_record
from .data import SyntheticClinicalConfig, generate_synthetic_clinical_telemetry, split_by_patient
from .federated import run_federated_experiment
from .ledger import verify


def run_smoke_checks() -> dict:
    frame = generate_synthetic_clinical_telemetry(SyntheticClinicalConfig(n_patients=120, n_sites=3, time_steps=6, seed=17))
    train, validation, test = split_by_patient(frame, seed=17)
    shared = set(train.patient_id).intersection(validation.patient_id).union(set(train.patient_id).intersection(test.patient_id))
    if shared:
        raise AssertionError("Patient split leakage")
    result = run_federated_experiment(frame, {
        "seed": 17,
        "rounds": 2,
        "local_epochs": 1,
        "privacy_enabled": False,
        "aggregation": "fedavg",
        "output_dir": "check_results",
    })
    if not 0 <= result["metrics"]["f1"] <= 1:
        raise AssertionError("Invalid F1")
    ledger = verify("check_results/audit_ledger.jsonl")
    if not ledger["valid"]:
        raise AssertionError("Audit ledger failed validation")
    return {"ok": True, "f1": result["metrics"]["f1"], "records": ledger["records"]}
