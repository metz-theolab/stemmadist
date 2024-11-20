"""Main entrance point for the stemmadist package and
computation of the similarities between trees.
"""
import click
from stemmadist.dists.signed_similarity.signed_similarity import \
    roos_similarity
from stemmadist.dists.rf.rf import rf_distance
from stemmadist.dists.rf.rf_jaccard import rf_jaccard
from stemmadist.dists.rf.matching_split import rf_matching_split
from stemmadist.dists.shared_information import matching_split_information
from stemmadist.dists.shared_information.shared_phylogenetic_information \
    import shared_phylogenetic_information
from stemmadist.dists.graphs.adjacency_matrix import adjacency_matrix_distance
from stemmadist.dists.graphs.graph_edit import graph_edit_distance


AVAILABLE_DISTANCES = {
    "rf": rf_distance,
    "rf_jaccard": rf_jaccard,
    "matching_split": rf_matching_split,
    "adjacency_matrix": adjacency_matrix_distance,
    "graph_edit_distance": graph_edit_distance,
    "signed_similarity": roos_similarity,
    ##### Deprecated #####
    # "shared_phylogenetic_information": shared_phylogenetic_information,
    # "matching_split_information": matching_split_information,
    ######################
}


def compute_distance(tree_1_str, tree_2_str, distance_name, **kwargs):
    """Compute the distance between two trees.

    Parameters:
    tree_1_str: First tree in Newick format
    tree_2_str: Second tree in Newick format
    distance_name: Name of the distance to compute
    kwargs: Additional arguments to pass to the distance function

    Returns:
    distance: Distance between the two trees
    """
    # try:
    return AVAILABLE_DISTANCES[distance_name](tree_1_str, tree_2_str, **kwargs)
    # except KeyError:
    #     raise ValueError(f"Unknown distance {distance_name}. "
    #                      f"Available distances are {list(AVAILABLE_DISTANCES.keys())}.")

@click.command()
@click.option('--distance', help='Name of the selected distance.')
@click.option('--tree1', help='First tree to compare.')
@click.option('--tree2', help='Second tree to compare.')
def compute(distance, tree1, tree2):
    """Compute a distance between two trees in Newick format."""
    print(f"Distance score {distance}: {compute_distance(tree1, tree2, distance)}")
    return compute_distance(tree1, tree2, distance)
