"""Implement Generalized Robinson-Foulds distances.
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from stemmadist.utils.utils import load_tree, get_splits


def split_similarity(splits_1, splits_2, score_computer, maximize=False,
                     *args,
                     **kwargs):
    """Given two slides, define the generalized Robinson-Foulds distance
    using the similarity given as input in the score_computer function.
    """
    scores = {}
    for ix_1, split_1 in enumerate(splits_1):
        scores[ix_1] = {}
        for ix, split_2 in enumerate(splits_2):
            scores[ix_1][ix] = score_computer(split_1,
                                              split_2,
                                              *args,
                                              **kwargs)
    # This can be optimized
    scores_array = np.array(
        [[scores[i][j] for j in range(len(scores))]
         for i in range(len(scores))]
    )
    row_ind, col_ind = linear_sum_assignment(scores_array, maximize=maximize)
    return scores_array[row_ind, col_ind].sum()


def rf_generalized(tree_1_str, tree_2_str, score_computer,
                   maximize=False,
                   ignore_trivial_split=False,
                   ignore_all_trivial_splits=False,
                   *args, **kwargs):
    """Return the generalized Robinson's Foulds jaccard distance."""
    tree_1 = load_tree(tree_1_str)
    tree_2 = load_tree(tree_2_str)

    splits_1 = get_splits(tree_1,
                          ignore_trivial_split=ignore_trivial_split,
                          ignore_all_trivial_split=ignore_all_trivial_splits)
    splits_2 = get_splits(tree_2, 
                          ignore_trivial_split=ignore_trivial_split,
                          ignore_all_trivial_split=ignore_all_trivial_splits)

    return split_similarity(splits_1,
                            splits_2,
                            score_computer,
                            maximize=maximize,
                            *args,
                            **kwargs)
