"""Implement the adjacency matrix metric between two graphs."""

import numpy as np
from stemmadist.utils.utils import load_tree


def build_edges_from_tree(node, node_ids):
    """
    Recursively build edges from the tree structure.
    """
    edges = []
    # Assign an ID to the node if it doesn't have a name
    if node.name:
        node_id = node.name
    else:
        node_id = f"Node{len(node_ids)}"
        node_ids[node] = node_id

    for child in node.descendants:
        # Assign an ID to the child if it doesn't have a name
        if child.name:
            child_id = child.name
        else:
            child_id = f"Node{len(node_ids)}"
            node_ids[child] = child_id

        edges.append((node_id, child_id))  # Add edge
        edges.extend(build_edges_from_tree(
            child, node_ids))  # Recurse for child
    return edges


def create_adjacency_matrix(tree):
    """Create an adjacency matrix from a tree."""
    node_ids = {}
    # Build edges from the tree
    edges = build_edges_from_tree(tree, node_ids)

    # Extract unique nodes and sort
    nodes = sorted(set([edge[0] for edge in edges] + [edge[1]
                   for edge in edges]))

    # Create a mapping from node IDs to indices
    node_indices = {node_id: idx for idx, node_id in enumerate(nodes)}

    # Initialize the adjacency matrix
    n = len(nodes)
    matrix = np.zeros((n, n), dtype=int)

    # Fill the adjacency matrix
    for edge in edges:
        i = node_indices[edge[0]]
        j = node_indices[edge[1]]
        matrix[i, j] = 1  # Mark as connected
        matrix[j, i] = 1  # Assuming undirected graph

    return nodes, matrix


def compute_distance_adjacency_matrix(matrix_1, matrix_2, degree=2):
    """Compute the distance between two adjacency matrices."""
    # Ensure the matrices are the same size
    size = max(matrix_1.shape[0], matrix_2.shape[0])
    padded_matrix_1 = np.zeros((size, size), dtype=int)
    padded_matrix_2 = np.zeros((size, size), dtype=int)
    padded_matrix_1[:matrix_1.shape[0], :matrix_1.shape[1]] = matrix_1
    padded_matrix_2[:matrix_2.shape[0], :matrix_2.shape[1]] = matrix_2

    # Compute the distance
    return ((padded_matrix_1 - padded_matrix_2) ** degree).mean() ** (1 / degree)


def adjacency_matrix_distance(tree_1_str, tree_2_str):
    """Compute the distance between two trees using adjacency matrices."""
    # Load the trees from the Newick strings
    tree_1 = load_tree(tree_1_str)
    tree_2 = load_tree(tree_2_str)

    # Create adjacency matrices from the trees
    _, matrix_1 = create_adjacency_matrix(tree_1)
    _, matrix_2 = create_adjacency_matrix(tree_2)

    # Compute the distance between the adjacency matrices
    distance = compute_distance_adjacency_matrix(matrix_1, matrix_2)
    return distance
