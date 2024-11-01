"""Set of utilities functions for graph manipulation.
"""

from functools import reduce
from newick import loads


def load_tree(newick_str):
    """Load the first tree of the newick string.
    Careful, if there are several trees, only the first one is loaded.
    """
    return loads(newick_str)[0]


def get_nodes(node):
    """Get the nodes under a leaf."""
    if node.is_leaf:
        return {node.name}

    leaves = set()

    for child in node.descendants:
        leaves.update(get_nodes(child))
    if node.name:
        leaves.add(node.name)
    return leaves


def get_splits(node, 
               ignore_all_trivial_split=True,
               ignore_trivial_split=False):
    """
    Get the splits recursively at each node.
    """
    splits = []

    if node.is_leaf:
        return splits

    current_leaves = []
    for descendant in node.descendants:
        current_leaves.append(get_nodes(descendant))
        splits += get_splits(descendant)
    # Check if only individual leaves have been captured by the split
    # and ignore if specified
    if ignore_all_trivial_split and \
        all(len(elem) == 1 for elem in current_leaves):
        return splits
    # Check if one individual leave has been captured by the split
    # and remove if specified
    if ignore_trivial_split:
        current_leaves = [elem for elem in current_leaves if len(elem) > 1]

    splits.append(tuple(current_leaves))

    return splits


def get_unique_values_splits(splits_1, splits_2):
    """
    Get the number of distinct leaves in two lists of splits,
    where each split can contain a different number of subsets.
    """
    # Combine all subsets from both lists of splits into a single list of sets
    all_sets = [subset for split in (splits_1 + splits_2) for subset in split]
    
    # Use reduce to apply union across all sets to find unique elements
    unique_values = reduce(set.union, all_sets, set())
    
    return len(unique_values)


def are_splits_incompatible(split_1, split_2):
    """
    Determines if two splits are incompatible.
    A split is represented as a tuple of two sets, where each set is a group
    of taxa.
    For example, split1 = ({'A', 'B'}, {'C', 'D'})
    represents the split {A, B} | {C, D}.
    """

    # Unpack the splits
    split_1_left, split_1_right = split_1
    split_2_left, split_2_right = split_2

    # Check for incompatibility: There should not be overlap between 
    # a group in one split
    # and both groups in the other split.

    # Group 1 of split 1 should not overlap with both groups of split 2
    if split_1_left & split_2_left and split_1_left & split_2_right:
        return True
    # Group 2 of split 1 should not overlap with both groups of split 2
    if split_1_right & split_2_left and split_1_right & split_2_right:
        return True

    # If no conflicts were found, the splits are compatible
    return False


def assign_node_names(tree, counter=1):
    """
    Assign unique names to unnamed nodes in the tree.
    """
    if not tree.name:
        tree.name = f"HN{counter}"
        counter += 1
    for child in tree.descendants:
        counter = assign_node_names(child, counter)
    return counter