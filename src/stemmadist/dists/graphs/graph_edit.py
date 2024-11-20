"""Implementation of the graph edit distance algorithm.
"""

from stemmadist.utils.utils import load_tree
import networkx as nx


def newick_to_networkx(newick_str):
    """Parse a Newick string and store it into NetworkX.
    """
    # Parse the Newick tree
    tree = load_tree(newick_str)

    # Initialize an empty directed NetworkX graph
    G = nx.DiGraph()
    unique_id = 0  # Counter for unnamed internal nodes

    # Recursive function to add nodes and edges to the graph
    def add_edges(node, parent=None):
        nonlocal unique_id
        current_node = node.name if node.name else f"internal_{unique_id}"
        if not node.name:
            unique_id += 1

        # Add the current node
        G.add_node(current_node, label=node.name)
        # Internal nodes without names get a unique ID
        if parent is not None:
            G.add_edge(parent, current_node)

        # Recursively add children
        for child in node.descendants:
            add_edges(child, current_node)

    # Start building the graph from the root of the tree
    add_edges(tree)
    return G


def label_based_cost(u, v):
    """Compute cost from switching labels.
    """
    # Retrieve labels and compare
    label_u = u.get("label", "")
    label_v = v.get("label", "")
    return 0 if label_u == label_v else 1/2


def node_deletion_cost(node):
    """Compute cost of deleting a node.
    """
    return 1


def node_insertion_cost(node):
    """Compute cost of inserting a node.
    """
    return 1


def graph_edit_distance(tree_1_str, tree_2_str):
    """Compute the Graph Edit distance between two trees specified in the
    Newick format.
    """
    tree_1 = newick_to_networkx(tree_1_str)
    tree_2 = newick_to_networkx(tree_2_str)

    return nx.graph_edit_distance(
        tree_1,
        tree_2,
        node_subst_cost=label_based_cost,
        node_del_cost=node_deletion_cost,
        node_ins_cost=node_insertion_cost,
    )
