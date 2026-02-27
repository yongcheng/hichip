import pandas as pd

from src.data.candidates import generate_candidate_pairs
from src.data.labels import assign_binary_labels, build_positive_pair_set


def test_generate_candidate_pairs_distance_window() -> None:
    bins = pd.DataFrame(
        {
            "chrom": ["chr1", "chr1", "chr1"],
            "start": [0, 1000, 3000],
            "end": [1000, 2000, 4000],
            "atac": [1.0, 2.0, 3.0],
            "h3k27ac": [1.5, 2.5, 3.5],
            "bin_id": ["chr1:0-1000", "chr1:1000-2000", "chr1:3000-4000"],
        }
    )

    pairs = generate_candidate_pairs(bins, distance_min_bp=1500, distance_max_bp=3500)
    assert len(pairs) == 2
    assert set(pairs["distance_bp"].tolist()) == {2000, 3000}


def test_assign_binary_labels_from_loops() -> None:
    loops = pd.DataFrame(
        {
            "chrom1": ["chr1"],
            "start1": [50],
            "end1": [150],
            "chrom2": ["chr1"],
            "start2": [2050],
            "end2": [2150],
        }
    )
    positives = build_positive_pair_set(loops, resolution_bp=1000)

    candidates = pd.DataFrame(
        {
            "chrom": ["chr1", "chr1"],
            "bin_id_left": ["chr1:0-1000", "chr1:1000-2000"],
            "bin_id_right": ["chr1:2000-3000", "chr1:3000-4000"],
            "distance_bp": [2000, 2000],
        }
    )

    labeled = assign_binary_labels(candidates, positives)
    assert labeled["label"].tolist() == [1, 0]
