# Governance and Ethics

CareFed-TrustLab is a research prototype for studying privacy-preserving federated learning in connected-health scenarios. This document defines the responsible-use boundary for the repository.

## 1. Scope

The repository is intended for:

- Academic experimentation with synthetic connected-health telemetry.
- Federated learning workflow design.
- Privacy-utility and robustness studies.
- Fairness, calibration, and explainability audits.
- Reproducibility training for healthcare AI research.

The repository is not intended for:

- Clinical decision support.
- Real patient triage.
- Hospital deployment.
- Regulatory compliance claims.
- Production secure multiparty computation.
- Processing identifiable health data.

## 2. Data boundary

The default workflow uses synthetic data only. No real patient data should be committed to the repository.

Before adapting this project to real or licensed health data, researchers should confirm:

- Institutional approval and ethical review requirements.
- Legal basis for processing.
- Data-protection impact assessment needs.
- Data minimization and retention limits.
- Access-control and infrastructure requirements.
- De-identification, pseudonymization, and re-identification risk controls.
- Publication and sharing restrictions.

## 3. Model boundary

The model outputs should be interpreted as research artifacts. They should not be used to recommend treatment, rank patients, allocate care, or replace clinical judgment.

Any real-world healthcare AI system would require clinical validation, safety engineering, monitoring, documentation, human oversight, governance approval, and external evaluation.

## 4. Security boundary

The secure aggregation component is a teaching prototype. It demonstrates the idea of masked aggregation and explicitly scoped assumptions. It is not a complete secure-MPC system.

For security-sensitive use, researchers should use audited cryptographic protocols, threat-model review, secure key management, secure transport, deployment isolation, and independent security assessment.

## 5. Fairness and subgroup auditing

CareFed-TrustLab includes group-audit outputs to encourage careful reporting. Subgroup metrics should be used as diagnostic evidence, not as proof of clinical fairness.

A responsible analysis should report:

- Which groups were audited.
- Which metrics were compared.
- Whether groups were sufficiently represented.
- Whether observed disparities are stable across seeds.
- Whether gaps may be caused by synthetic generator assumptions.

## 6. Explainability boundary

Integrated Gradients feature attribution is provided to support interpretability research. Attribution scores are not causal proof. They should be treated as model-behavior signals that require domain review.

## 7. Publication checklist

Before presenting results, include:

- Synthetic-data statement.
- Random seeds and configuration files.
- Train/validation/test split description.
- Threshold-selection rule.
- Aggregation method and attack scenario.
- Privacy-noise setting and approximate privacy-budget limitation.
- Subgroup-audit limitations.
- Clinical non-deployment statement.

## 8. Academic integrity

Do not claim that synthetic results represent real hospital performance. Do not imply official institutional affiliation. Do not remove limitations when using figures, tables, or text derived from this repository.
