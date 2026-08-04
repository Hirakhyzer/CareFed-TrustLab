# Contributing

Thank you for considering a contribution to CareFed-TrustLab.

This repository is a research prototype. Contributions should preserve its central values: privacy awareness, reproducibility, transparent limitations, and responsible healthcare AI framing.

## Useful contributions

Good contributions include:

- Improved synthetic data-generation controls.
- Additional federated-learning baselines.
- Better robust-aggregation tests.
- Privacy-accounting improvements.
- Calibration and subgroup-audit enhancements.
- Reproducibility documentation.
- More tests for leakage prevention and ledger verification.
- Clearer figures, diagrams, and teaching material.

## Contribution principles

Before opening a pull request, check that the change:

1. Does not add real patient data.
2. Does not create clinical deployment claims.
3. Keeps train, validation, and test boundaries clear.
4. Documents configuration, seed, and evaluation assumptions.
5. Adds or updates tests when behavior changes.
6. Keeps privacy and secure-aggregation claims scoped accurately.

## Development setup

```bash
python -m pip install --upgrade pip
python -m pip install numpy pandas scikit-learn scipy torch matplotlib PyYAML pytest jupyter
export PYTHONPATH=src
```

Windows:

```bat
set PYTHONPATH=src
```

Run checks:

```bash
pytest
python -c "from carefed.checks import run_smoke_checks; print(run_smoke_checks())"
```

## Pull request checklist

- [ ] The change is documented.
- [ ] Tests or smoke checks pass.
- [ ] No real health data are included.
- [ ] Any new result is clearly labeled synthetic or experimental.
- [ ] Any security/privacy claim is scoped and not overstated.
- [ ] Any new figure/table can be reproduced from code or documented input.

## Academic integrity

Do not remove limitation statements. Do not represent synthetic results as real hospital performance. Do not imply institutional endorsement unless formal authorization exists.
