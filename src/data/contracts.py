"""Data contract constants for v1 loop prediction."""

BIN_FEATURE_COLUMNS = ["chrom", "start", "end", "atac", "h3k27ac"]
LOOP_BEDPE_MIN_COLUMNS = 6

PAIR_FEATURE_COLUMNS = [
    "distance_bp",
    "atac_left",
    "h3k27ac_left",
    "atac_right",
    "h3k27ac_right",
    "atac_mean",
    "h3k27ac_mean",
    "atac_product",
    "h3k27ac_product",
]
