# Reproducibility Playbook

This playbook defines how to run and report CareFed-TrustLab experiments in a way that another researcher can inspect and repeat.

## 1. Minimum experiment record

Every run should record:

| Item | Example |
|---|---|
| Experiment name | `secure_fedavg_baseline` |
| Synthetic data seed | `42` |
| Number of patients | `720` |
| Number of sites | `6` |
| Number of rounds | `4` |
| Aggregation | `secure_fedavg` |
| Privacy setting | clipping + noise multiplier |
| Attack setting | none, label flip, sign flip, scaled update |
| Split rule | patient-level chronological or patient-level random, as configured |
| Threshold rule | selected on validation only |
| Hardware/software | OS, Python version, major packages |

## 2. Recommended run order

1. Generate or confirm the synthetic cohort.
2. Freeze the experiment configuration.
3. Run centralized and local-only baselines.
4. Run the federated baseline.
5. Run privacy-utility sweeps.
6. Run robustness tests.
7. Run subgroup audits.
8. Export figures and CSV outputs.
9. Verify the audit ledger.
10. Write a limitation statement before interpreting the results.

## 3. Leakage checks

Before reporting test metrics, confirm:

- The same synthetic patient does not appear in multiple partitions.
- Scalers and preprocessing objects are fitted only on training patients.
- Thresholds are selected only on validation data.
- Test data are not used for model choice or hyperparameter tuning.

## 4. Metric bundle

A complete result bundle should include:

- `metrics.csv`
- `roc.csv`
- `precision_recall.csv`
- `calibration.csv`
- `group_audit.csv`
- `group_gap_summary.csv`
- `integrated_gradients.csv`
- `audit_ledger.jsonl`
- Generated figures
- Configuration file or CLI command

## 5. Repeated-seed reporting

For research claims, single-run metrics should be treated as preliminary. Stronger reporting should use repeated seeds and show mean, standard deviation, and confidence intervals where possible.

Suggested table:

| Model | Aggregation | Attack | Mean F1 | Std F1 | Mean ROC-AUC | Mean ECE |
|---|---|---|---:|---:|---:|---:|
| Federated | FedAvg | None | TBD | TBD | TBD | TBD |
| Federated | Median | Sign flip | TBD | TBD | TBD | TBD |

## 6. Ledger verification

The audit ledger should be checked after every experiment. A valid ledger does not prove clinical safety or cryptographic security, but it supports traceability by confirming that the recorded chain has not been modified after generation.

## 7. Suggested manuscript paragraph

> We evaluated CareFed-TrustLab on synthetic connected-health telemetry only. Patient-level train, validation, and test partitions were separated before preprocessing. Feature scaling was fitted only on training data. Alert thresholds were selected on validation outputs and fixed before held-out testing. Results therefore describe the configured synthetic generator and should not be interpreted as real-world clinical performance.
