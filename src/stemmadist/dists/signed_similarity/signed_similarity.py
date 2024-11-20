
"""Implement the signed similarity metric between two trees,
as suggested by Roos et al.
"""

import itertools
from stemmadist.utils.utils import load_tree, assign_node_names


def build_node_paths(tree, path=None, paths=None):
    """
    Recursively build the paths to each node in the tree.
    """
    if paths is None:
        paths = {}
    if path is None:
        path = []

    if tree.name:
        paths[tree.name] = path + [tree.name]

    # Order the children by name to ensure consistent paths
    # Computation
    for child in sorted(tree.descendants, key=lambda x: x.name):
        build_node_paths(child, path + [tree.name], paths)
    return paths

def calculate_distance(paths, node1, node2):
    """
    Compute the distances in terms of edges between two nodes.
    """
    path1 = paths.get(node1, [])
    path2 = paths.get(node2, [])

    # Find the nearest common ancestor
    common_ancestor = None
    for u, v in zip(path1, path2):
        if u == v:
            common_ancestor = u
        else:
            break

    # Compute the distance as the sum of the distances to the common ancestor
    # Total path - path to reach ancestor - 1
    # (to avoid counting the common ancestor twice)
    distance = (len(path1) - path1.index(common_ancestor) - 1) + (
        len(path2) - path2.index(common_ancestor) - 1
    )
    return distance

def compute_u(tree_paths_tree1, tree_paths_tree2, A, B, C):
    """
    Compute the u value for a triplet of nodes taken from tree 1 and tree 2.
    """
    d_tree1_AB = calculate_distance(tree_paths_tree1, A, B)
    d_tree1_AC = calculate_distance(tree_paths_tree1, A, C)
    d_tree2_AB = calculate_distance(tree_paths_tree2, A, B)
    d_tree2_AC = calculate_distance(tree_paths_tree2, A, C)

    sign_test = int(d_tree1_AB - d_tree1_AC > 0) - \
        int(d_tree1_AB - d_tree1_AC < 0)
    sign_ref = int(d_tree2_AB - d_tree2_AC > 0) - \
        int(d_tree2_AB - d_tree2_AC < 0)
    u_value = 1 - 0.5 * abs(sign_test - sign_ref)
    return u_value

def compute_roos_similarity(tree_1, tree_2):
    """Compute the Roos similarity between two trees."""
    # Assign unique names to unnamed nodes
    assign_node_names(tree_1)
    assign_node_names(tree_2)
    
    # Compute the paths for every node in the tree
    tree_paths_1 = build_node_paths(tree_1)
    tree_paths_2 = build_node_paths(tree_2)
    
    # List the common nodes in the tree
    common_nodes = sorted(
        set(tree_paths_1.keys()).intersection(tree_paths_2.keys())
    )

    # Compute for each triplet the u value
    S = 0
    for A, B, C in itertools.combinations(common_nodes, 3):
        S += compute_u(tree_paths_1, tree_paths_2, A, B, C)

    # Adjust the score for identical trees to zero
    # Perfect score is the case were each triplet has a u value of 1
    max_score = len(list(itertools.combinations(common_nodes, 3)))
    similarity_score = S/max_score  
    # Average and substract from 1 to obtain a similarity score

    return similarity_score

def roos_similarity(tree_1_str, tree_2_str):
    """
    Compute the Roos similarity between two trees.
    """
    # Loads trees from strings
    tree_1 = load_tree(tree_1_str)
    tree_2 = load_tree(tree_2_str)

    return compute_roos_similarity(tree_1, tree_2)

