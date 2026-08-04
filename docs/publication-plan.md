# Publication Readiness Plan

CareFed-TrustLab can support a research paper, workshop submission, student project, or thesis chapter if results are reported with appropriate boundaries.

## 1. Possible paper framing

**Working title:**

> CareFed-TrustLab: A Reproducible Testbed for Privacy-Preserving and Trustworthy Federated Learning in Connected Healthcare

## 2. Contribution structure

A defensible publication could emphasize:

1. A synthetic multi-site connected-health testbed.
2. A leakage-aware federated learning workflow.
3. Privacy-utility experimentation with update clipping and DP-style noise.
4. Robust aggregation under malicious-client simulations.
5. Calibration, subgroup audit, and explainability outputs.
6. A hash-chained audit ledger for experiment traceability.

## 3. Suggested manuscript outline

1. Introduction
2. Background and related work
3. Synthetic connected-health scenario
4. Federated learning and privacy workflow
5. Robustness and malicious-client simulation
6. Trustworthy AI evaluation design
7. Results
8. Discussion
9. Limitations
10. Reproducibility package

## 4. Required figures

| Figure | Purpose |
|---|---|
| System architecture | Show local sites, update handling, aggregation, and audit outputs |
| Privacy-utility curve | Compare privacy noise against model utility |
| Robustness matrix | Compare aggregators under malicious-client scenarios |
| Calibration plot | Show probability reliability |
| Subgroup gap chart | Show disparity analysis |
| Audit ledger diagram | Explain traceability mechanism |

## 5. Required tables

| Table | Purpose |
|---|---|
| Dataset generator summary | Describe synthetic cohort and variables |
| Experimental settings | Document seeds, rounds, sites, models, thresholds |
| Baseline comparison | Centralized, local-only, and federated results |
| Privacy-utility results | Noise setting, approximate epsilon, metrics |
| Robust aggregation results | Aggregator × attack comparison |
| Limitations table | Clear scope and non-deployment boundaries |

## 6. High-risk claims to avoid

Do not claim:

- The system is clinically validated.
- The secure aggregation prototype is production-ready MPC.
- Synthetic results demonstrate real hospital performance.
- Group metrics prove fairness.
- Approximate epsilon is a formal privacy guarantee.
- The project is affiliated with institutions unless formal authorization exists.

## 7. Strong claims that are safe if supported by outputs

You may state, when backed by generated artifacts:

- The repository implements a reproducible synthetic testbed.
- Experiments separate training, validation, and test partitions.
- The system exports calibration and subgroup-audit artifacts.
- The ledger can verify the integrity of recorded experiment events.
- Robust aggregation can be compared under configured attack simulations.

## 8. Reviewer expectations

Reviewers may ask for:

- Stronger privacy accounting.
- External validation.
- More realistic data heterogeneity.
- Larger repeated-seed benchmarks.
- Ablations for privacy and robustness settings.
- Clear comparison with existing federated-learning baselines.

These should be treated as future-work items unless implemented and tested.
