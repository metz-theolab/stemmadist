"""Implements the matching split information score.
"""

from stemmadist.dists.rf.grf import rf_generalized
from stemmadist.dists.shared_information.\
    shared_phylogenetic_information import phylogenetic_information_content


def matching_split_information(split_1, split_2):
    """Define the matching split information score (MSI) between two splits."""
    split_1_left, split_1_right = split_1
    split_2_left, split_2_right = split_2
    return max(
        phylogenetic_information_content(
            (
                split_1_left.intersection(split_2_left),
                split_1_right.intersection(split_2_right),
            )
        ),
        phylogenetic_information_content(
            (
                split_1_left.intersection(split_2_right),
                split_1_right.intersection(split_2_left),
            )
        ),
    )


def shared_phylogenetic_information(tree_1, tree_2):
    rf_generalized(tree_1, tree_2, score_computer=matching_split_information)
