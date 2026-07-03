from __future__ import annotations

import argparse
from pathlib import Path

from .data import SyntheticClinicalConfig, generate_synthetic_clinical_telemetry
from .experiments import export_experiment_bundle
from .federated import run_federated_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CareFed-TrustLab synthetic research prototype.")
    parser.add_argument("--patients", type=int, default=720)
    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--aggregation", default="secure_fedavg", choices=["fedavg", "secure_fedavg", "median", "trimmed_mean"])
    parser.add_argument("--attack", default="none", choices=["none", "label_flip", "sign_flip", "scale_update"])
    parser.add_argument("--noise", type=float, default=0.35)
    parser.add_argument("--no-privacy", action="store_true")
    parser.add_argument("--output", default="results/run")
    args = parser.parse_args()

    frame = generate_synthetic_clinical_telemetry(SyntheticClinicalConfig(n_patients=args.patients, n_sites=args.sites))
    result = run_federated_experiment(frame, {
        "rounds": args.rounds,
        "aggregation": args.aggregation,
        "attack": args.attack,
        "privacy_enabled": not args.no_privacy,
        "noise_multiplier": args.noise,
        "output_dir": args.output,
    })
    export_experiment_bundle(result, args.output)
    print(result["metrics"])
    print(f"Approximate epsilon: {result['epsilon']}")
    print(f"Saved research bundle to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
