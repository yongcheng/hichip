# Reproducibility Guide

## Environment
- Use pinned dependencies in `environment/requirements-ml.txt`.
- Record Python version and platform for each run.

## Determinism
- Fix random seeds for numpy, torch, and training frameworks.
- Save data split manifests under `data/metadata/`.

## Experiment Tracking
- Save configs, metrics, and model artifacts per run.
- Keep run IDs stable and traceable to git commit hashes.
