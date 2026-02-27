# Methodology (Draft)

## Task Definition
- V1: binary loop classification for candidate locus pairs.
- V2: contact probability/regression.

## Labeling
- Positive labels: HiChIP loop calls passing chosen significance threshold.
- Negative labels: distance-matched non-loop pairs.

## Splits
- Chromosome-based split to avoid leakage.

## Metrics
- Primary: PR-AUC
- Secondary: ROC-AUC, distance-stratified performance
