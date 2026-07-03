# Threat model and security boundary

## Assets to protect

- Raw site-local patient records.
- Local model updates before aggregation.
- Demographic and care-setting subgroup information.
- Experiment configuration and audit evidence.

## Actors

| Actor | Capability | Assumption in this prototype |
| --- | --- | --- |
| Hospital node | Trains on local synthetic records | Honest or optionally malicious in attack experiments |
| Home-care node | Trains on local synthetic records | Honest or optionally malicious in attack experiments |
| Coordinator | Receives client updates | Honest-but-curious for secure aggregation demonstration |
| Researcher | Configures experiments and reads aggregate output | Must not use real patient records in this repository |

## Attacks represented

| Attack | Code path | Purpose |
| --- | --- | --- |
| Label flip | `label_flip` | Simulates corrupted local labels |
| Scaled update | `scale_update` | Simulates oversized model update |
| Sign flip | `sign_flip` | Simulates adversarial gradient direction |
| Client dropout | experiment configuration extension | Simulates unavailable sites |

## Non-claims

The pairwise-mask mechanism is not a complete secure multi-party computation protocol, the epsilon value is an approximation rather than a formal accountant, and this repository does not claim compliance with health-data regulations or clinical readiness.
