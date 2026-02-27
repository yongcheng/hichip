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

## Input Data Contracts
1. Bin feature table (`TSV` or `CSV`)
- Required columns: `chrom,start,end,atac,h3k27ac`
- Coordinates should be fixed-width bins matching `resolution_bp` in config.

2. Loop labels (`BEDPE`-like)
- First six columns must represent:
  `chrom1,start1,end1,chrom2,start2,end2`
- Intra-chromosomal loops are used for v1.

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r environment/requirements-ml.txt
```

## Train v1 XGBoost Baseline
Update paths in `configs/base.yaml`, then run:

```bash
python scripts/train.py --config configs/train_xgb.yaml
```

Outputs are written under `paths.output_dir` (default: `outputs/xgb_baseline/`):
- `xgb_model.json`
- `metrics.json`
- `resolved_config.yaml`

## Reproducibility
See `docs/reproducibility.md` for seeds, split strategy, and versioning policy.

## License
Code license: see `LICENSE`.
