# System diagrams

## Trustworthiness evidence flow

```mermaid
flowchart TD
  C[Experiment configuration] --> D[Data generation]
  D --> S[Patient-level split]
  S --> P[Train-only preprocessing]
  P --> F[Federated training rounds]
  F --> U[Utility evaluation]
  F --> R[Robustness evaluation]
  F --> G[Group audit]
  F --> X[Integrated Gradients]
  F --> L[Hash-chained ledger]
  U --> O[CSV and figure bundle]
  R --> O
  G --> O
  X --> O
  L --> O
  O --> W[Workshop brief and paper tables]
```

## Secure aggregation teaching model

```mermaid
flowchart LR
  A[Client A update] --> A1[Add + pairwise masks]
  B[Client B update] --> B1[Add + or - pairwise masks]
  C[Client C update] --> C1[Add + or - pairwise masks]
  A1 --> S[Coordinator sum]
  B1 --> S
  C1 --> S
  S --> K[Pairwise masks cancel in aggregate]
  K --> M[Average global update]
```

## Experiment decision flow

```mermaid
flowchart LR
  Q{Research question} --> P{Privacy trade-off?}
  P -->|Yes| A[Noise sweep]
  Q --> R{Malicious client?}
  R -->|Yes| B[Robustness matrix]
  Q --> F{Group concern?}
  F -->|Yes| C[Subgroup audit]
  Q --> E{Need evidence?}
  E -->|Yes| D[Export figures, CSV, audit ledger]
```

## Output map

| Output | Audience | Main question |
| --- | --- | --- |
| `metrics.csv` | ML researcher | Does the model have useful ranking and thresholded performance? |
| `calibration.csv` | Clinical collaborator | Do probability estimates match observed outcome frequency? |
| `group_audit.csv` | Trustworthy-AI reviewer | Are there observable performance differences across groups? |
| `integrated_gradients.csv` | Domain expert | Which input signals influence model scores? |
| `audit_ledger.jsonl` | Security/reproducibility reviewer | What configuration and participants produced each round? |
| MATLAB figures | Workshop/paper audience | How do privacy, robustness, and group outcomes compare? |
