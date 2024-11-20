"""Tests that the graphs distance behaves as expected.
"""
import unittest
from stemmadist.dists.graphs.graph_edit import graph_edit_distance
from stemmadist.dists.graphs.adjacency_matrix import \
    build_edges_from_tree, create_adjacency_matrix, \
    compute_distance_adjacency_matrix, adjacency_matrix_distance
from stemmadist.utils.utils import load_tree


class TestGraphEditDistance(unittest.TestCase):
    """Tests that the graph edit distance behaves as expected.
    """
    def setUp(self):
        """Tests that the graph edit distance behaves as expected.
        """
        # Tree strings as class attributes
        self.tree_1_str = "((A,B)X,(C,D)Y)Z;"
        self.tree_2_str = "((A,C)X,(B,D)Y)Z;"
        self.tree_3_str = "(((A,B)X,C)Y,D)Z;"
        self.tree_4_str = "((A,B)X,(C,E)Y)Z;"        

    def test_graph_distance_identical_trees(self):
        """Test that identical trees have zero distance."""
        self.assertEqual(graph_edit_distance(self.tree_1_str,
                                             self.tree_1_str), 0)

    def test_graph_distance_single_substitution(self):
        """Test with a single substitution (A vs C in position)."""
        distance = graph_edit_distance(self.tree_1_str,
                                       self.tree_2_str)
        self.assertEqual(distance, 1)  # One substitution expected

    def test_graph_distance_different_structure(self):
        """Test with a structurally different tree."""
        distance = graph_edit_distance(self.tree_1_str,
                                       self.tree_3_str)
        self.assertGreater(distance, 1)  # More than one substitution/insertion

    def test_graph_distance_node_insertion_deletion(self):
        """Test where one tree has an extra or missing node."""
        distance = graph_edit_distance(self.tree_1_str,
                                  self.tree_3_str)
        expected_min_distance = 2
        self.assertGreaterEqual(distance, expected_min_distance)


class TestAdjacencyMatrix(unittest.TestCase):
    """Tests that the adjacency matrix distance is properly computed.
    """
    def setUp(self):
        """Set up the trees for testing.
        """
        # Tree strings as class attributes
        self.tree_1_str = "((A,B)X,(C,D)Y)Z;"
        self.tree_2_str = "((A,C)X,(B,D)Y)Z;"
        self.tree_3_str = "(((A,B)X,C)Y,D)Z;"
        self.tree_4_str = "((A,B)X,(C,E)Y)Z;"

        # Load trees
        self.tree_1 = load_tree(self.tree_1_str)
        self.tree_2 = load_tree(self.tree_2_str)

    def test_build_edges(self):
        """Tests that the edges are correctly built."""
        self.assertEqual(
            build_edges_from_tree(self.tree_1, node_ids={}),
            [('Z', 'X'), ('X', 'A'), ('X', 'B'), ('Z', 'Y'),
             ('Y', 'C'), ('Y', 'D')]
        )

    def test_build_adjacency_matrix(self):
        """Tests that the adjacency matrix is correctly built."""
        nodes, matrix = create_adjacency_matrix(self.tree_1)
        self.assertEqual(matrix.shape, (7, 7))
        # Check that node Z is connected to X and Y
        index_z = nodes.index('Z')
        index_x = nodes.index('X')
        index_y = nodes.index('Y')


        self.assertEqual(matrix[index_z, index_x], 1)
        self.assertEqual(matrix[index_z, index_y], 1)

    def test_compute_distance_adjacency_matrix(self):
        """Tests that the distance between two adjacency
        matrices is correct."""
        _, matrix_1 = create_adjacency_matrix(self.tree_1)
        _, matrix_2 = create_adjacency_matrix(self.tree_2)
        distance = compute_distance_adjacency_matrix(matrix_1, matrix_2)
        self.assertAlmostEqual(distance, 0.40, 2)

    def test_adjacency_matrix_distance_function(self):
        """Tests the adjacency matrix distance function with tree strings."""
        distance = adjacency_matrix_distance(self.tree_1_str, self.tree_2_str)
        self.assertAlmostEqual(distance, 0.40, 2)

    def test_adjacency_matrix_distance_function_self(self):
        """Tests the adjacency matrix distance function on the same tree.
        """
        distance = adjacency_matrix_distance(self.tree_1_str, self.tree_1_str)
        self.assertEqual(distance, 0)


if __name__ == "__main__":
    unittest.main()
