# Security Policy

CareFed-TrustLab is a research prototype for synthetic connected-health federated learning. It is not a production security system.

## Supported scope

Security reports are welcome for:

- Code paths that may accidentally expose local files or credentials.
- Unsafe defaults that could encourage misuse with real health data.
- Bugs in audit-ledger verification.
- Bugs that break patient-level split isolation.
- Misleading secure-aggregation or privacy claims in documentation.

## Out of scope

The following are out of scope for this prototype:

- Production clinical deployment support.
- Regulatory compliance certification.
- Full secure-MPC guarantees.
- Real patient-data processing.
- Model performance claims on real healthcare environments.

## Responsible disclosure

Please open a private report or contact the maintainer if a vulnerability could cause harmful disclosure, unsafe claims, or misleading healthcare AI behavior.

When reporting, include:

- A concise description.
- Steps to reproduce.
- Affected files or commands.
- Expected behavior.
- Actual behavior.
- Suggested mitigation, if known.

## Data safety rule

Do not attach real patient records, real credentials, or private health data to issues, pull requests, examples, screenshots, or test cases.

## Important limitation

The secure aggregation module is a teaching prototype. It should not be used as a production cryptographic system without independent protocol design, security review, implementation hardening, and deployment controls.
