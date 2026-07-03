# Experiment design

## Primary comparison

Compare centralized pooled learning, standard federated averaging, privacy-preserving federated averaging, and robust aggregation under identical patient-level splits.

## Required safeguards

1. Split by patient before fitting any scaler.
2. Fit the feature scaler only on the training partition.
3. Select the operating threshold only on validation data.
4. Report final results once on the held-out test partition.
5. Repeat every configuration across at least five random seeds.
6. Preserve config, seed, code commit, result CSVs, and audit ledger.

## Experiment matrix

| Study | Variable | Suggested values | Main outputs |
| --- | --- | --- | --- |
| Privacy utility | noise multiplier | 0, 0.1, 0.25, 0.35, 0.5, 0.75 | F1, AUC, Brier, ECE, epsilon |
| Robustness | attack | none, label flip, sign flip, scaled update | F1 drop, recall drop, subgroup gaps |
| Aggregation | aggregator | fedavg, secure_fedavg, median, trimmed mean | utility and attack resilience |
| Heterogeneity | site mix | balanced, home-care heavy, hospital heavy | site-level performance |
| Fairness | audit group | age, sex, care setting, site | recall, F1, positive-rate gaps |
| Scalability | number of sites | 3, 6, 12 | round time, utility, ledger size |

## Expected outputs

```text
results/<experiment>/
  metrics.csv
  group_audit.csv
  group_gap_summary.csv
  roc.csv
  precision_recall.csv
  calibration.csv
  roc_curve.png
  calibration_curve.png
  group_gaps.png
  audit_ledger.jsonl
```

## Statistical analysis

Use repeated seed metrics, report mean and standard deviation, then apply a paired nonparametric comparison such as a Friedman test with post-hoc correction when comparing more than two aggregation strategies.
