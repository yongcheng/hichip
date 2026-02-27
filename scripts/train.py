"""Training CLI for 3D genome loop prediction."""

from __future__ import annotations

import argparse
import json

from src.train.pipeline import run_xgb_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Train v1 binary loop predictor")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    result = run_xgb_pipeline(args.config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
