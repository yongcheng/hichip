# Data Layout and Contracts

This folder stores metadata and schema definitions. Do not commit protected raw data.

## Expected Inputs
- ATAC-seq signal tracks (bigWig)
- H3K27ac ChIP-seq signal tracks (bigWig)
- H3K27ac HiChIP loop calls (BEDPE or equivalent)
- Genome build: hg38

## Suggested Layout
- `raw/` (ignored by git): source files
- `processed/` (ignored by git): derived matrices/tables
- `metadata/`: sample sheets, biosample annotations, QC summaries

## Notes
- Document exact preprocessing and loop-calling thresholds in `docs/methodology.md`.
