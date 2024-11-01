"""Define the Matching Split comparison metric for the Generalized
Robinson-Foulds distance.
"""
from stemmadist.dists.rf.grf import rf_generalized
from itertools import permutations


def matching_split(split_1, split_2):
    """Compute the matching split score between two splits of possibly different sizes."""
    # Pad the smaller split with empty sets to make the sizes equal
    max_len = max(len(split_1), len(split_2))
    split_1_padded = split_1 + (set(),) * (max_len - len(split_1))
    split_2_padded = split_2 + (set(),) * (max_len - len(split_2))

    # Calculate the minimum matching score by testing all possible set pairings
    min_match_score = float('inf')

    for perm in permutations(split_2_padded):
        match_score = 0

        for a, b in zip(split_1_padded, perm):
            if a and b:  # Both sets are non-empty
                diff = len(a - b) + len(b - a)
                match_score += diff
            else:  # One of the sets is empty
                diff = len(a) + len(b)  # Add the size of the non-empty set
                match_score += diff

        if match_score < min_match_score:
            min_match_score = match_score

    # The final score is the total elements minus the minimum matching score
    return min_match_score/2


def rf_matching_split(tree_1_str, tree_2_str):
    """Return the generalized Robinson's Foulds jaccard distance."""
    return rf_generalized(tree_1_str, tree_2_str, matching_split,
                          ignore_trivial_split=True)





# def matching_split(split_1, split_2):
#     """Compute the score between two splits."""
#     # split_1_left, split_1_right = split_1
#     # split_2_left, split_2_right = split_2

#     # len_tree = get_unique_values_splits([split_1], [split_2])
#     # return len_tree - max(
#     #     len(split_1_left.intersection(split_2_left))
#     #     + len(split_1_right.intersection(split_2_right)),
#     #     len(split_1_left.intersection(split_2_right))
#     #     + len(split_1_right.intersection(split_2_left)),
#     # )
