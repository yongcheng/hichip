# 3D Genome Loop Prediction from Epigenomic Signals

Predict 3D chromatin interactions (v1: binary loop prediction) using ATAC-seq and H3K27ac ChIP-seq, trained with H3K27ac HiChIP-derived loop labels.

## Project Scope
- Genome build: hg38
- Inputs: ATAC-seq, H3K27ac ChIP-seq
- Training labels: H3K27ac HiChIP loops
- V1 task: binary loop classification
- V2 task: contact probability prediction

## Repository Layout
- `configs/`: experiment configs
- `data/`: data specification and metadata (no raw data committed)
- `src/`: reusable code for data, features, models, training
- `scripts/`: command-line entrypoints
- `tests/`: unit/integration tests
- `docs/`: methods and reproducibility notes
- `environment/`: pinned dependencies

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r environment/requirements-ml.txt
```

## Reproducibility
See `docs/reproducibility.md` for seeds, split strategy, and versioning policy.

## License
Code license: see `LICENSE`.
