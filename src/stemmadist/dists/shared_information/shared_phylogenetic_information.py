"""Implement the shared phylogenetic information score between two trees.
"""

import math
from stemmadist.dists.rf.grf import rf_generalized
from stemmadist.utils.utils import get_unique_values_splits, \
    are_splits_incompatible


def double_factorial(n):
    """Define the double factorial."""
    if n <= 0:
        return 1
    return math.prod(range(n, 0, -2))


def P_Phy(split):
    """Compute the probability of apparition of a split."""
    split_1_left, split_1_right = split

    X_len = get_unique_values_splits(split_1_left, split_1_right)

    numerator = (double_factorial(2 * len(split_1_left) - 3) *
                 double_factorial(2 * len(split_1_right) - 3))

    denominator = double_factorial(2 * X_len - 5)

    return numerator / denominator


def phylogenetic_information_content(split):
    """Compute the phylogenetic information content."""
    return -math.log(P_Phy(split))


def probability_splits(split_1, split_2):
    """Compute the probability of apparition of two splits.
    """
    split_1_left, split_1_right = split_1
    split_2_left, _ = split_2
    X_len = get_unique_values_splits([split_1], [split_2])

    numerator = (double_factorial(2 * (len(split_1_right) + 1) - 5) *
                 double_factorial(2 * (len(split_2_left) + 1) - 5) *
                 double_factorial(2 * (len(split_1_left) - len(split_2_left)
                                       + 2) - 5))

    denominator = double_factorial(2 * X_len - 5)

    return -math.log(numerator / denominator)


def shared_phylogenetic_information_score(split_1, split_2):
    """Compute the shared phylogenetic information of two splits.
    """
    if are_splits_incompatible(split_1, split_2):
        return 0
    return phylogenetic_information_content(split_1) + \
        phylogenetic_information_content(split_2) - \
        probability_splits(split_1, split_2)


def shared_phylogenetic_information(tree_1, tree_2):
    return rf_generalized(
        tree_1,
        tree_2,
        score_computer=shared_phylogenetic_information_score)
