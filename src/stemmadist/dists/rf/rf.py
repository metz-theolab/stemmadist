"""Compute the classical Robinson's Foulds distance.
"""

from stemmadist.utils.utils import load_tree, get_splits


def rf_distance(tree_1_str, tree_2_str):
    """Compute the Robinson's Foulds distance between two trees specified in
    the Newick format."""
    tree_1 = load_tree(tree_1_str)
    tree_2 = load_tree(tree_2_str)

    splits_1 = get_splits(tree_1)
    splits_2 = get_splits(tree_2)

    diff_splits = 0
    for split in splits_1:
        if split not in splits_2:
            diff_splits += 1
    for split in splits_2:
        if split not in splits_1:
            diff_splits += 1
    return diff_splits
