# Synthetic data boundary

This directory is reserved for generated synthetic research data and result-free sample schemas.

## Dataset produced by the generator

The `carefed.data.generate_synthetic_clinical_telemetry` function creates a multi-site longitudinal table with hospital and home-care nodes. It includes simulated vital-sign-style values, mobility, adherence, care-contact signals, demographic attributes, and a synthetic deterioration label.

No real patient data, hospital data, clinical records, or protected health information are included in this repository.

## Data dictionary

| Column | Type | Meaning |
| --- | --- | --- |
| `patient_id` | string | Synthetic patient identifier |
| `time_step` | integer | Simulated observation step |
| `site_id` | categorical | Simulated hospital or home-care node |
| `care_setting` | categorical | Home or hospital setting |
| `age_band`, `sex` | categorical | Synthetic audit attributes |
| `heart_rate`, `systolic_bp`, `respiratory_rate`, `spo2`, `temperature`, `glucose` | float | Simulated physiological signals |
| `mobility_score`, `adherence`, `care_contact_minutes` | float | Simulated contextual signals |
| `deterioration_label` | binary | Simulated research outcome |

Generated CSV files should not be committed by default unless they are intentionally versioned as a small non-sensitive example.
