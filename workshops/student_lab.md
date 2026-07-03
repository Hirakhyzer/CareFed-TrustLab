# Student lab: trustworthy federated healthcare learning

## Learning outcomes

By the end of this lab, students should be able to:

1. Explain why site-local data and federated training are different from pooling data.
2. Run a baseline federated experiment and inspect its audit ledger.
3. Compare FedAvg with coordinate median under a sign-flip update attack.
4. Create a privacy-utility table by varying the noise multiplier.
5. Interpret a subgroup recall gap without making unsupported fairness claims.
6. Explain why this prototype is not a clinical decision system.

## Suggested 90-minute sequence

| Time | Activity | Output |
| --- | --- | --- |
| 0–15 min | Inspect synthetic schema and data boundary | Data-governance note |
| 15–35 min | Run a baseline federated configuration | Metrics and ROC plot |
| 35–50 min | Enable a simulated malicious update | Robustness observation |
| 50–65 min | Compare robust aggregation | Comparison table |
| 65–80 min | Run subgroup audit | Gap interpretation |
| 80–90 min | Review ledger and limitations | Short reflection |

## Assessment questions

- Why is selecting a test threshold after viewing test scores a methodological problem?
- What does the pairwise-mask prototype hide, and what does it not protect against?
- When might a group gap be caused by small sample size rather than model behavior?
- Which output would you include in a workshop briefing for clinicians and security researchers?
