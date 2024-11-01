"""Implementation of the graph edit distance algorithm.
"""

from stemmadist.utils.utils import load_tree


def graph_distance(tree_1, tree_2):
    """Compute the Graph edit distance between two trees.
    """
    if tree_1.name != tree_2.name:
        # Node substitution cost (if names differ, count half because
        # trees are traversed twice
        cost = .5
    else:
        cost = 0

    # Get children of both nodes
    children1 = tree_1.descendants
    children2 = tree_2.descendants

    # Calculate insertion or deletion costs for unbalanced children
    ins_del_cost = abs(len(children1) - len(children2))

    # Recursive structure comparison for all pairs of children
    sub_cost = 0
    for c1, c2 in zip(children1, children2):
        sub_cost += graph_distance(c1, c2)

    # Total cost includes substitution, insertion/deletion, and recursive
    # structure costs
    total_cost = cost + ins_del_cost + sub_cost
    return total_cost


def graph_edit_distance(tree_1_str, tree_2_str):
    """Compute the Graph Edit distance between two trees specified in the
    Newick format.
    """
    tree_1 = load_tree(tree_1_str)
    tree_2 = load_tree(tree_2_str)

    return graph_distance(tree_1, tree_2)
