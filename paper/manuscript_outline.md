# CareFed-TrustLab manuscript outline

## Proposed title

**Auditable Privacy-Preserving Federated Learning for Connected Healthcare: A Trustworthiness Evaluation Framework**

## Abstract checklist

- State the distributed healthcare motivation.
- Describe the synthetic-data boundary.
- Name federated, privacy, robust aggregation, audit, and fairness components.
- Report the evaluation protocol, not only the best score.
- State limitations clearly.

## 1. Introduction

Explain why connected healthcare needs collaboration across hospitals and home-care settings, and why raw-data exchange is difficult. State that utility alone is insufficient without privacy, robustness, group performance, calibration, explainability, and auditability.

## 2. Research questions

| ID | Question |
| --- | --- |
| RQ1 | How does federated utility compare with pooled centralized and local-only baselines? |
| RQ2 | What privacy-utility relationship appears as update noise changes? |
| RQ3 | Which aggregation rule is most resilient to simulated malicious clients? |
| RQ4 | How do site, care setting, age band, and sex affect subgroup performance? |
| RQ5 | What evidence is sufficient for a reproducible and auditable experiment record? |

## 3. Method

Describe the synthetic generator, patient-level splitting, training-only scaling, validation thresholding, local model, aggregation, pairwise-mask demonstration, attack simulation, group audit, Integrated Gradients, and audit ledger.

## 4. Results

Include utility table, calibration curve, ROC/PR curves, privacy-utility plot, robustness matrix, group audit table, explanation ranking, and ledger verification result.

## 5. Limitations and ethics

No real clinical data, no clinical validation, toy secure aggregation, approximate privacy accounting, possible synthetic-data bias, and no deployment claim.

## 6. Reproducibility appendix

Record commit hash, configuration, random seeds, Python and PyTorch versions, hardware, CSV exports, figures, and audit ledger hash chain.
