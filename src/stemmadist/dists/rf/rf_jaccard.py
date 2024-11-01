"""Implementation of the generalized Robinsons-Foulds metric
Jaccard-Robinson-Foulds (JRF).
If order=1, this is the same as the Nye similarity.
"""

from stemmadist.dists.rf.grf import rf_generalized


def compute_intersection_proportion(set_1, set_2, order=1):
    """
    Compute the proportion of the intersection of two sets.

    Parameters:
    set_1: First set
    set_2: Second set

    Returns:
    proportion: Proportion of the intersection
    """
    intersection = set_1.intersection(set_2)
    union = set_1.union(set_2)

    if order == 1:
        # Computation for the Nye similarity
        return len(intersection) / len(union)
    else:
        # Computation for the Böcker similarity
        return 2 - 2 * (len(intersection) / len(union)) ** order


def jaccard_similarity(split_1, split_2, order=1):
    """Compute the score between two splits."""
    split_1_left, split_1_right = split_1
    split_2_left, split_2_right = split_2
    return max(
        min(
            compute_intersection_proportion(split_1_left,
                                            split_2_left,
                                            order=order),
            compute_intersection_proportion(split_1_right,
                                            split_2_right,
                                            order=order),
        ),
        min(
            compute_intersection_proportion(split_1_left,
                                            split_2_right,
                                            order=order),
            compute_intersection_proportion(split_1_right,
                                            split_2_left,
                                            order=order),
        ),
    )


def rf_jaccard(tree_1_str, tree_2_str, order=1):
    """Return the generalized Robinson's Foulds jaccard distance."""
    return rf_generalized(tree_1_str,
                          tree_2_str,
                          jaccard_similarity,
                          maximize=True,
                          order=order)
