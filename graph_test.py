#!python

from graph import Graph, Vertex
import unittest
# Python 2 and 3 compatibility: unittest module renamed this assertion method
if not hasattr(unittest.TestCase, 'assertCountEqual'):
    unittest.TestCase.assertCountEqual = unittest.TestCase.assertItemsEqual


class VertexTest(unittest.TestCase):

    def test_init(self):
        id = "A"
        v = Vertex(id)
        assert v.id == id
        self.assertDictEqual(v.neighbors, {})

    def test_add_neighbor(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        # Test default weight variable
        v1.add_neighbor(v2)
        self.assertDictEqual(v1.neighbors, {v2: 1})
        # Error should be raised if v2 is added again
        with self.assertRaises(KeyError):
            v1.add_neighbor(v2)
        # Test passed in weight variable
        v3 = Vertex(3)
        v1.add_neighbor(v3, 3)
        self.assertDictEqual(v1.neighbors, {v2: 1, v3: 3})
        # Error should be raised if v3 is added again
        with self.assertRaises(KeyError):
            v1.add_neighbor(v3, 3)
        # Test recursive adding
        v2.add_neighbor(v1)
        self.assertDictEqual(v2.neighbors, {v1: 1})
        v3.add_neighbor(v1)
        self.assertDictEqual(v3.neighbors, {v1: 1})

    def test_get_neighbors(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        # Test getting neighbors
        v1.add_neighbor(v2)
        v1.add_neighbor(v3)
        self.assertCountEqual(v1.get_neighbors(), [v2, v3])
        v2.add_neighbor(v1, 2)
        v2.add_neighbor(v3, 2)
        self.assertCountEqual(v2.get_neighbors(), [v1, v3])
        v3.add_neighbor(v1, 3)
        v3.add_neighbor(v2, 3)
        self.assertCountEqual(v3.get_neighbors(), [v1, v2])

    def test_get_id(self):
        # Test alphabetical ids
        v_a = Vertex("A")
        assert v_a.get_id() == "A"
        v_b = Vertex("B")
        assert v_b.get_id() == "B"
        v_c = Vertex("C")
        assert v_c.get_id() == "C"
        # Test numerical ids
        v1 = Vertex(1)
        assert v1.get_id() == 1
        v2 = Vertex(2)
        assert v2.get_id() == 2
        v3 = Vertex(3)
        assert v3.get_id() == 3

    def test_get_edge_weight(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        # Test default weight variable
        v2.add_neighbor(v1)
        assert v2.get_edge_weight(v1) == 1
        # Test passed in weight variable
        v2.add_neighbor(v3, 3)
        assert v2.get_edge_weight(v3) == 3


class GraphTest(unittest.TestCase):

    def test_init(self):
        g = Graph()
        self.assertDictEqual(g.vert_list, {})
        assert g.num_vertices == 0

    def test_num_vertices(self):
        g = Graph()

        # Test num_vertices increase when a vertex is added
        assert g.num_vertices == 0
        g.add_vertex('A')
        assert g.num_vertices == 1
        g.add_vertex('B')
        assert g.num_vertices == 2
        g.add_vertex('C')
        assert g.num_vertices == 3

        # Test num_vertices +1 increase when edge is added with new vertex
        g.add_edge('A', 'B')
        assert g.num_vertices == 3
        g.add_edge('B', 'C')
        assert g.num_vertices == 3
        g.add_edge('C', 'D')
        assert g.num_vertices == 4

        # Test num_vertices +2 increase when edge added with two new vertices
        g.add_edge('E', 'F')
        assert g.num_vertices == 6

        # Error should be raised when a vertex, that already exists, is added
        # Test num_vertices not changing when error is raised
        with self.assertRaises(KeyError):
            g.add_vertex('B')  # Vertex already exists
        assert g.num_vertices == 6
        with self.assertRaises(KeyError):
            g.add_vertex('D')  # Vertex already exists
        assert g.num_vertices == 6

    def test_add_vertex(self):
        g = Graph()

        # Graph should have newly added vertex
        assert g.num_vertices == 0
        v_a = g.add_vertex('A')
        assert g.num_vertices == 1
        assert g.get_vertex('A') == v_a
        v_b = g.add_vertex('B')
        assert g.num_vertices == 2
        assert g.get_vertex('B') == v_b
        v_c = g.add_vertex('C')
        assert g.num_vertices == 3
        assert g.get_vertex('C') == v_c

        # Error should be raised when a vertex, that already exists, is added
        with self.assertRaises(KeyError):
            g.add_vertex('A')  # Vertex already exists
        with self.assertRaises(KeyError):
            g.add_vertex('B')  # Vertex already exists
        with self.assertRaises(KeyError):
            g.add_vertex('C')  # Vertex already exists

    def test_get_vertex(self):
        g = Graph()

        # Error should be raised when getting a vertex that does not exist
        with self.assertRaises(KeyError):
            g.get_vertex(1)  # Vertex does not exist
        with self.assertRaises(KeyError):
            g.get_vertex(2)  # Vertex does not exist
        with self.assertRaises(KeyError):
            g.get_vertex(3)  # Vertex does not exist

        # Graph should be able to get existing vertices
        v1 = g.add_vertex(1)
        assert g.get_vertex(1) == v1
        v2 = g.add_vertex(2)
        assert g.get_vertex(2) == v2
        v3 = g.add_vertex(3)
        assert g.get_vertex(3) == v3

    def test_add_edge(self):
        g = Graph()

        # Start with graph that already has vertices in it
        v_a = g.add_vertex('A')
        assert g.get_vertex('A') == v_a
        v_b = g.add_vertex('B')
        assert g.get_vertex('B') == v_b
        v_c = g.add_vertex('C')
        assert g.get_vertex('C') == v_c
        assert g.num_vertices == 3

        # When edge is added with existing vertices,
        # second vertex should be a neighbor of first vertex
        g.add_edge('A', 'B')
        self.assertCountEqual(v_a.get_neighbors(), [v_b])
        self.assertCountEqual(v_b.get_neighbors(), [])
        g.add_edge('A', 'C')
        self.assertCountEqual(v_a.get_neighbors(), [v_b, v_c])
        self.assertCountEqual(v_c.get_neighbors(), [])
        g.add_edge('B', 'C')
        self.assertCountEqual(v_b.get_neighbors(), [v_c])
        self.assertCountEqual(v_c.get_neighbors(), [])

        # When edge added with nonexistent vertices, add nonexistent vertices
        # Then, second vertex should be a neighbor of first vertex
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        g.add_edge('B', 'D')
        self.assertCountEqual(v_b.get_neighbors(), [v_c, v_d])
        self.assertCountEqual(v_d.get_neighbors(), [])
        g.add_edge('E', 'F')
        self.assertCountEqual(v_e.get_neighbors(), [v_f])
        self.assertCountEqual(v_f.get_neighbors(), [])

        # When duplicate edge is added, KeyError should be raised
        with self.assertRaises(KeyError):
            g.add_edge('A', 'C')
        self.assertCountEqual(v_a.get_neighbors(), [v_b, v_c])
        self.assertCountEqual(v_c.get_neighbors(), [])
        with self.assertRaises(KeyError):
            g.add_edge('E', 'F')
        self.assertCountEqual(v_e.get_neighbors(), [v_f])
        self.assertCountEqual(v_f.get_neighbors(), [])

        # Test that edge has weight
        assert v_a.get_edge_weight(v_b) == 1
        assert v_e.get_edge_weight(v_f) == 1
        v_g = g.add_vertex('G')
        v_h = g.add_vertex('H')
        g.add_edge('G', 'H', 5)
        assert v_g.get_edge_weight(v_h) == 5

    def test_get_vertices(self):
        # Test getting alphabetical vertices
        g_letters = Graph()
        v_a = g_letters.add_vertex('A')
        v_b = g_letters.add_vertex('B')
        v_c = g_letters.add_vertex('C')
        self.assertCountEqual(g_letters.get_vertices(), [v_a, v_b, v_c])

        # Test getting numberical vertices
        g_numbers = Graph()
        v1 = g_numbers.add_vertex(1)
        v2 = g_numbers.add_vertex(2)
        v3 = g_numbers.add_vertex(3)
        self.assertCountEqual(g_numbers.get_vertices(), [v1, v2, v3])

    def test_breadth_first_search(self):
        # Create graph with 4 levels
        g = Graph()
        # Add vertices that can be seen at mulitple levels
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        v_g = g.add_vertex('G')
        v_h = g.add_vertex('H')
        v_i = g.add_vertex('I')
        v_j = g.add_vertex('J')
        # Create edges
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "A")
        g.add_edge("B", "E")
        g.add_edge("C", "D")
        g.add_edge("D", "F")
        g.add_edge("E", "H")
        g.add_edge("F", "G")
        g.add_edge("G", "H")
        g.add_edge("H", "I")
        g.add_edge("H", "J")
        g.add_edge("H", "G")
        g.add_edge("J", "B")

        # Get all vertices accessible at level 0
        level_0 = g.breadth_first_search(v_a, 0, only_new=True)
        self.assertCountEqual(level_0, [v_a])
        # Get all vertices accessible at level 1
        level_1 = g.breadth_first_search(v_a, 1, only_new=False)
        self.assertCountEqual(level_1, [v_b, v_c])
        # Get all vertices accessible at level 2
        level_2 = g.breadth_first_search(v_a, 2, only_new=False)
        self.assertCountEqual(level_2, [v_a, v_d, v_e])
        # Get all vertices accessible at level 3
        level_3 = g.breadth_first_search(v_a, 3, only_new=False)
        self.assertCountEqual(level_3, [v_b, v_c, v_f, v_h])
        # Get all vertices accessible at level 4
        level_4 = g.breadth_first_search(v_a, 4, only_new=False)
        self.assertCountEqual(level_4, [v_a, v_d, v_e, v_g, v_i, v_j])
        # Get all vertices accessible at level 5
        level_5 = g.breadth_first_search(v_a, 5, only_new=False)
        self.assertCountEqual(level_5, [v_b, v_c, v_f, v_h])

        # Get new vertices accessible at level 1
        new_level_1 = g.breadth_first_search(v_a, 1)
        self.assertCountEqual(new_level_1, [v_b, v_c])
        # Get new vertices accessible at level 2
        new_level_2 = g.breadth_first_search(v_a, 2)
        self.assertCountEqual(new_level_2, [v_d, v_e])
        # Get new vertices accessible at level 3
        new_level_3 = g.breadth_first_search(v_a, 3)
        self.assertCountEqual(new_level_3, [v_f, v_h])
        # Get new vertices accessible at level 4
        new_level_4 = g.breadth_first_search(v_a, 4)
        self.assertCountEqual(new_level_4, [v_g, v_i, v_j])
        # No new vertices accessible at level 5
        new_level_5 = g.breadth_first_search(v_a, 5)
        self.assertCountEqual(new_level_5, [])

        # Test starting from vertex "g"
        # Get all vertices accessible at level 1
        g_level_1 = g.breadth_first_search(v_g, 1, only_new=False)
        self.assertCountEqual(g_level_1, [v_h])
        # Get new vertices accessible at level 2
        g_new_level_2 = g.breadth_first_search(v_g, 2)
        self.assertCountEqual(g_new_level_2, [v_i, v_j])
        # Get all vertices accessible at level 3
        g_level_3 = g.breadth_first_search(v_g, 3, only_new=False)
        self.assertCountEqual(g_level_3, [v_b, v_h])
        # Get new vertices accessible at level 4
        g_new_level_4 = g.breadth_first_search(v_g, 4)
        self.assertCountEqual(g_new_level_4, [v_a, v_e])
        # Get new vertices accessible at level 5
        g_new_level_5 = g.breadth_first_search(v_g, 5)
        self.assertCountEqual(g_new_level_5, [v_c])
        # Get new vertices accessible at level 6
        g_new_level_6 = g.breadth_first_search(v_g, 6)
        self.assertCountEqual(g_new_level_6, [v_d])
        # Get new vertices accessible at level 7
        g_new_level_7 = g.breadth_first_search(v_g, 7)
        self.assertCountEqual(g_new_level_7, [v_f])
        # No new vertices accessible at level 8
        g_new_level_8 = g.breadth_first_search(v_g, 8)
        self.assertCountEqual(g_new_level_8, [])

        # Error should be raised if passing key rather than vertex object
        with self.assertRaises(TypeError):
            g.breadth_first_search("A", 1, only_new=False)
        with self.assertRaises(TypeError):
            g.breadth_first_search("G", 2)
        # Error should be raised when vertex not in graph
        v_y = Vertex("Y")
        with self.assertRaises(ValueError):
            g.breadth_first_search(v_y, 2, only_new=False)
        v_z = Vertex("Z")
        with self.assertRaises(ValueError):
            g.breadth_first_search(v_z, 1)

    def test_find_shortest_path(self):
        # Create graph with 4 levels
        g = Graph()
        # Create and get references to vertices
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        v_g = g.add_vertex('G')
        v_h = g.add_vertex('H')
        v_i = g.add_vertex('I')
        v_j = g.add_vertex('J')
        # Create edges
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "A")
        g.add_edge("B", "E")
        g.add_edge("C", "D")
        g.add_edge("D", "F")
        g.add_edge("E", "H")
        g.add_edge("F", "G")
        g.add_edge("G", "H")
        g.add_edge("H", "I")
        g.add_edge("H", "J")
        g.add_edge("H", "G")
        g.add_edge("J", "B")
        # Add vertices that cannot be reached by other vertices
        g.add_vertex('X')
        g.add_edge("Y", "Z")

        # Find shortest path 2 edges away
        path_2 = g.find_shortest_path("A", "E")
        self.assertEqual(path_2, [v_a, v_b, v_e])  # Order matters
        # Find shortest path 4 edges away
        path_4 = g.find_shortest_path("A", "I")
        self.assertEqual(path_4, [v_a, v_b, v_e, v_h, v_i])  # Order matters
        # Find shortest path 7 edges away
        path_7 = g.find_shortest_path("G", "F")
        true_path_7 = [v_g, v_h, v_j, v_b, v_a, v_c, v_d, v_f]  # Order matters
        self.assertEqual(path_7, true_path_7)

        # There is no shortest path between unconnected vertices in same graph
        no_path_1 = g.find_shortest_path("G", "X")
        self.assertEqual(no_path_1, None)
        no_path_2 = g.find_shortest_path("X", "Z")
        self.assertEqual(no_path_2, None)
        # There is no way to traverse to the same vertex
        no_path = g.find_shortest_path("A", "A")
        self.assertEqual(no_path, None)

        # No path to vertex that does not have an edge directed into it
        g.directed = True
        # Added directed edge from 0 to A
        g.add_edge(0, "A")
        # Try to get 0 from A
        no_directed_path = g.find_shortest_path("A", 0)
        self.assertEqual(no_directed_path, None)

        # Error should be raised when vertex not in graph
        with self.assertRaises(KeyError):
            g.find_shortest_path("A", 1)
        with self.assertRaises(KeyError):
            g.find_shortest_path("T", "A")

    def test_depth_first_search(self):
        # Create graph
        g = Graph()
        # Create and get references to vertices
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        v_g = g.add_vertex('G')
        v_h = g.add_vertex('H')
        v_i = g.add_vertex('I')
        v_j = g.add_vertex('J')
        # Create edges
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "A")
        g.add_edge("B", "E")
        g.add_edge("C", "D")
        g.add_edge("D", "F")
        g.add_edge("E", "H")
        g.add_edge("F", "G")
        g.add_edge("G", "H")
        g.add_edge("H", "I")
        g.add_edge("H", "J")
        g.add_edge("H", "G")
        g.add_edge("J", "B")

        # Depth first search starting at vertex A, prioritizing smaller values
        g.depth_first_search(v_a, least_first=True)
        self.assertEqual(v_a.parent, False)
        self.assertEqual(v_b.parent, v_a)
        self.assertEqual(v_e.parent, v_b)
        self.assertEqual(v_h.parent, v_e)
        self.assertEqual(v_g.parent, v_h)
        self.assertEqual(v_i.parent, v_h)
        self.assertEqual(v_j.parent, v_h)
        self.assertEqual(v_c.parent, v_a)
        self.assertEqual(v_d.parent, v_c)
        self.assertEqual(v_f.parent, v_d)

        # Add vertices that cannot be reached by other vertices
        v_s = g.add_vertex('S')
        v_t = g.add_vertex('T')

        # Depth first search starting at vertex A, prioritizing smaller values
        g.depth_first_search(v_h, least_first=True)
        self.assertEqual(v_h.parent, False)
        self.assertEqual(v_g.parent, v_h)
        self.assertEqual(v_i.parent, v_h)
        self.assertEqual(v_j.parent, v_h)
        self.assertEqual(v_b.parent, v_j)
        self.assertEqual(v_a.parent, v_b)
        self.assertEqual(v_c.parent, v_a)
        self.assertEqual(v_d.parent, v_c)
        self.assertEqual(v_f.parent, v_d)
        self.assertEqual(v_e.parent, v_b)
        self.assertEqual(v_e.parent, v_b)
        self.assertEqual(v_e.parent, v_b)

        # Vertex S and T cannot be reached
        self.assertEqual(v_s.parent, None)
        self.assertEqual(v_t.parent, None)

        # Error should be raised if passing key rather than vertex object
        with self.assertRaises(TypeError):
            g.depth_first_search("A", least_first=True)
        with self.assertRaises(TypeError):
            g.depth_first_search("G")
        # Error should be raised when vertex not in graph
        v_y = Vertex("Y")
        with self.assertRaises(ValueError):
            g.depth_first_search(v_y, least_first=True)
        v_z = Vertex("Z")
        with self.assertRaises(ValueError):
            g.depth_first_search(v_z)

    def test_find_path(self):
        # Create graph
        g = Graph()
        # Create and get references to vertices
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        v_g = g.add_vertex('G')
        v_h = g.add_vertex('H')
        v_i = g.add_vertex('I')
        v_j = g.add_vertex('J')
        # Create edges
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "A")
        g.add_edge("B", "E")
        g.add_edge("C", "D")
        g.add_edge("D", "F")
        g.add_edge("E", "H")
        g.add_edge("F", "G")
        g.add_edge("G", "H")
        g.add_edge("H", "I")
        g.add_edge("H", "J")
        g.add_edge("H", "G")
        g.add_edge("J", "B")

        # Test 5 different possible paths that include all vertices
        # Since find_path uses dfs visiting in sorted order, order is the same
        path_1 = g.find_path("A", "G")
        path_1_expected = [v_a, v_b, v_e, v_h, v_g]
        self.assertEqual(path_1, path_1_expected)  # Order matters
        path_2 = g.find_path("D", "J")
        path_2_expected = [v_d, v_f, v_g, v_h, v_j]
        self.assertEqual(path_2, path_2_expected)  # Order matters
        path_3 = g.find_path("B", "J")
        path_3_expected = [v_b, v_a, v_c, v_d, v_f, v_g, v_h, v_j]
        self.assertEqual(path_3, path_3_expected)  # Order matters
        path_4 = g.find_path("J", "H")
        path_4_expected = [v_j, v_b, v_a, v_c, v_d, v_f, v_g, v_h]
        self.assertEqual(path_4, path_4_expected)  # Order matters
        # Even if edge added from J to H, dfs prioritizes sorted order
        g.add_edge("J", "H")
        path_5 = g.find_path("J", "H")
        path_5_expected = [v_j, v_b, v_a, v_c, v_d, v_f, v_g, v_h]
        self.assertEqual(path_5, path_5_expected)  # Order matters
        # Show that shortest path is from vertex J to vertex H
        shortest_path_5 = g.find_shortest_path("J", "H")
        expected_shortest_path_5 = [v_j, v_h]  # Order matters
        self.assertEqual(shortest_path_5, expected_shortest_path_5)

        # Add vertices that cannot be reached by other vertices
        g.add_vertex('S')
        g.add_vertex('T')
        # Vertex S and T cannot be reached
        self.assertEqual(g.find_path("A", "S"), None)
        self.assertEqual(g.find_path("T", "A"), None)

        # Graph is directed, and vertex I does not direct anywhere
        self.assertEqual(g.find_path("I", "H"), None)
        # You can still get to vertex I from another vertex
        self.assertEqual(g.find_path("H", "I"), [v_h, v_i])

        # Error should be raised if passing vertex object rather than key
        with self.assertRaises(TypeError):
            g.find_path(v_a, "H")
        with self.assertRaises(TypeError):
            g.find_path("G", v_b)
        # Error should be raised when vertex id / key not in graph
        with self.assertRaises(KeyError):
            g.find_path("A", "Y")
        with self.assertRaises(KeyError):
            g.find_path("Z", "A")

    def test_find_maximal_clique(self):
        # Create graph unweighted, undirected graph
        g = Graph(weighted=False, directed=False)

        # A clique of 1
        v_a = g.add_vertex('A')
        maximal_clique_1 = g.find_maximal_clique(v_a)
        expected_maximal_clique_1 = [v_a]
        self.assertCountEqual(maximal_clique_1, expected_maximal_clique_1)
        # A clique of 2
        v_b = g.add_vertex('B')
        g.add_edge("A", "B")
        maximal_clique_2 = g.find_maximal_clique(v_a)
        expected_maximal_clique_2 = [v_a, v_b]
        self.assertCountEqual(maximal_clique_2, expected_maximal_clique_2)
        # Not a clique of 3
        v_c = g.add_vertex('C')
        not_clique_3 = g.find_maximal_clique(v_a)
        expected_not_clique_3 = [v_a, v_b]
        self.assertCountEqual(not_clique_3, expected_not_clique_3)
        # Now it is a clique of 3
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        maximal_clique_3 = g.find_maximal_clique(v_a)
        expected_maximal_clique_3 = [v_a, v_b, v_c]
        self.assertCountEqual(maximal_clique_3, expected_maximal_clique_3)
        # Not clique of 7
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        v_f = g.add_vertex('F')
        v_g = g.add_vertex('G')
        g.add_edge("A", "D")
        g.add_edge("A", "E")
        g.add_edge("A", "F")
        g.add_edge("A", "G")
        g.add_edge("B", "D")
        g.add_edge("B", "E")
        g.add_edge("B", "F")
        g.add_edge("B", "G")
        g.add_edge("C", "D")
        g.add_edge("C", "E")
        g.add_edge("C", "F")
        g.add_edge("C", "G")
        g.add_edge("D", "E")
        g.add_edge("D", "F")
        g.add_edge("D", "G")
        g.add_edge("E", "F")
        g.add_edge("E", "G")
        # But it is a clique of 6
        maximal_clique_6 = g.find_maximal_clique(v_a)
        expected_maximal_clique_6 = [v_a, v_b, v_c, v_d, v_e, v_f]
        self.assertCountEqual(maximal_clique_6, expected_maximal_clique_6)
        # Now it is a clique of 7
        g.add_edge("F", "G")
        maximal_clique_7 = g.find_maximal_clique(v_a)
        expected_maximal_clique_7 = [v_a, v_b, v_c, v_d, v_e, v_f, v_g]
        self.assertCountEqual(maximal_clique_7, expected_maximal_clique_7)

        # Test least first argument (checks neighors in sorted order)
        g = Graph(weighted=False, directed=False)
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        g.add_edge("B", "A")
        g.add_edge("B", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "D")
        least_clique = g.find_maximal_clique(v_b, least_first=True)
        # Vertex A is added to clique before Vertex C,
        # Even though B, C, D is a bigger clique that A, B
        expected_least_clique = [v_b, v_a]
        self.assertCountEqual(least_clique, expected_least_clique)
        # Test least first argument with numbers
        g = Graph(weighted=False, directed=False)
        v1 = g.add_vertex(1)
        v2 = g.add_vertex(2)
        v3 = g.add_vertex(3)
        g.add_edge(2, 1)
        g.add_edge(2, 3)
        least_clique_2 = g.find_maximal_clique(v2, least_first=True)
        # Vertex 1 is added to clique before Vertex 3
        expected_least_clique_2 = [v2, v1]
        self.assertCountEqual(least_clique_2, expected_least_clique_2)

        # Create graph where Vertex B is in 4 different cliques
        g = Graph(weighted=False, directed=False)
        v_a = g.add_vertex('A')
        v_b = g.add_vertex('B')
        v_c = g.add_vertex('C')
        v_d = g.add_vertex('D')
        v_e = g.add_vertex('E')
        # Clique 1 - B, A, C
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        # Clique 2 - B, C, D
        g.add_edge("B", "D")
        g.add_edge("C", "D")
        # Clique 3 - B, E, D
        g.add_edge("B", "E")
        g.add_edge("D", "E")
        # Clique 4 - B, A, E
        g.add_edge("A", "E")
        # Test random clique is a clique
        random_clique = g.find_maximal_clique()
        if v_a in random_clique and v_c in random_clique:
            expected_random_clique = [v_b, v_a, v_c]
        if v_c in random_clique and v_d in random_clique:
            expected_random_clique = [v_b, v_c, v_d]
        if v_e in random_clique and v_d in random_clique:
            expected_random_clique = [v_b, v_e, v_d]
        if v_a in random_clique and v_e in random_clique:
            expected_random_clique = [v_b, v_a, v_e]
        self.assertCountEqual(random_clique, expected_random_clique)

        # Should raise error if not passing vertex object for vertex parameter
        with self.assertRaises(TypeError):
            g.find_maximal_clique("A", least_first=False)
        with self.assertRaises(TypeError):
            g.find_maximal_clique("F")
        # Shoud raise error if calling find_maximal_clique on directed graph
        with self.assertRaises(TypeError):
            g.directed = True
            g.find_maximal_clique()
        with self.assertRaises(TypeError):
            a = Graph(weighted=False, directed=True)
            a.add_vertex("A")
            a.find_maximal_clique("A", least_first=False)
        # Error should be raised when vertex not in graph
        g.directed = False
        v_y = Vertex("Y")
        with self.assertRaises(ValueError):
            g.find_maximal_clique(v_y)
        v_z = Vertex("Z")
        with self.assertRaises(ValueError):
            g.find_maximal_clique(v_z, least_first=False)

    def test_is_connected(self):
        # Empty graph is not connected
        g = Graph(weighted=False, directed=False)
        self.assertEqual(g.is_connected(), False)

        # Graph with lonely vertex is connected
        g.add_vertex('A')
        self.assertEqual(g.is_connected(), True)

        # Graph with lonely vertices is not connected
        g.add_vertex('B')
        self.assertEqual(g.is_connected(), False)
        g.add_vertex('C')
        self.assertEqual(g.is_connected(), False)
        g.add_vertex('D')
        self.assertEqual(g.is_connected(), False)

        # Graph with separate subgraphs is not connected
        g.add_edge('A', 'B')
        self.assertEqual(g.is_connected(), False)
        g.add_edge('C', 'D')
        self.assertEqual(g.is_connected(), False)

        # Graph becomes connected when subgraphs are connected
        g.add_edge('A', 'D')
        self.assertEqual(g.is_connected(), True)

        # Directed graph with no vertex is not connected
        d = Graph(weighted=False, directed=True)
        self.assertEqual(d.is_connected(), False)
        # Directed graph with lonely vertex is connected
        d.add_vertex('A')
        self.assertEqual(d.is_connected(), True)

        # Directed graph with lonely vertices is not connected
        d.add_vertex('B')
        self.assertEqual(d.is_connected(), False)
        d.add_vertex('C')
        self.assertEqual(d.is_connected(), False)
        d.add_vertex('D')
        self.assertEqual(d.is_connected(), False)

        # Directed graph with separate subgraphs is not connected
        d.add_edge('A', 'B')
        self.assertEqual(d.is_connected(), False)
        d.add_edge('C', 'D')
        self.assertEqual(d.is_connected(), False)

        # Directed graph with "mother vertex" is connected
        d.add_edge('B', 'C')
        self.assertEqual(d.is_connected(), True)

    def test_is_eulerian(self):
        # Empty graph is not Eularian
        g = Graph(weighted=False, directed=False)
        self.assertEqual(g.is_eulerian(), False)

        # Graph with lonely vertex is Eularian
        g.add_vertex('A')
        self.assertEqual(g.is_eulerian(), True)

        # Graph with separate subgraphs is not Eularian
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('C', 'A')
        g.add_edge('D', 'E')
        g.add_edge('E', 'F')
        g.add_edge('F', 'D')
        self.assertEqual(g.is_eulerian(), False)
        # Graph with separate subgraphs may be considered weakly Eularian
        self.assertEqual(g.is_eulerian(is_connected=False), True)

        # Graph with two vertices having odd degree is not Eularian
        g.add_edge('C', 'D')
        self.assertEqual(g.is_eulerian(), False)
        # Graph with all vertices having equal degree is Eularian
        g.add_edge('C', 'G')
        g.add_edge('D', 'G')
        self.assertEqual(g.is_eulerian(), True)

        # Shoud raise error if calling is_eulerian on directed graph
        with self.assertRaises(TypeError):
            g.directed = True
            g.is_eulerian()
        with self.assertRaises(TypeError):
            d = Graph(weighted=False, directed=True)
            d.add_vertex("A")
            d.is_eulerian(is_connected=False)

    def test_average_path(self):
        g = Graph(weighted=False, directed=True)
        # Graph should correctly calculate path length
        g.add_edge('A', 'B')
        # Path from B to A does not exist, so it is 0
        self.assertEqual(g.average_path(), 0.5)
        # Path now exists
        g.add_edge('B', 'A')
        self.assertEqual(g.average_path(), 1)


if __name__ == '__main__':
    unittest.main()
