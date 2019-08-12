#!python

from collections import deque
import random
import string


class Vertex(object):
    """Helper class that defines vertices and vertex neighbors."""

    def __init__(self, vertex_id):
        """Initialize a vertex and its neighbors.

        id: a number or string to identify the vertex
        neighbors: set of vertices adjacent to self, stored in dictionary with:
            key = vertex object
            value = weight of edge between self and neighbor
        """
        self.id = vertex_id
        self.neighbors = {}
        self.parent = None

    def __repr__(self):
        """Return representation of vertex object."""
        return f"Vertex({self.id})"

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        return f"{self.id} adjacent to {[x.id for x in self.neighbors]}"

    def __hash__(self):
        """Return hash of vertex class, for using this class as a dict key."""
        return hash(self.id)

    def _check_type(self, other, operator):
        """Raise TypeError if there is a type mismatch."""
        # Get the name of the type of other object
        other_type = type(other).__name__
        # Create the error message if there is a type mismatch
        error_message = f"""'{operator}' not supported between
                            instances of 'Vertex' and '{other_type}'"""
        # If the other object is not of type Vertex, raise TypeError
        if not isinstance(other, Vertex):
            raise TypeError(error_message)

    def __lt__(self, other):
        """Determine if this vertex is less than the other vertex."""
        # Check the type of the other object, and raise error if type mismatch
        self._check_type(other, '<')

        # Otherwise, handle accordingly
        return self.id < other.id

    def __le__(self, other):
        """Determine if this vertex is less than or equal to other vertex."""
        # Check the type of the other object, and raise error if type mismatch
        self._check_type(other, '<=')

        # Otherwise, handle accordingly
        return self.id <= other.id

    def __eq__(self, other):
        """Determine if two vertices are equal."""
        # If the type of the other object is not a Vertex, it is not equal
        if not isinstance(other, Vertex):
            return False

        # Otherwise, handle accordingly
        return self.id == other.id

    def __ne__(self, other):
        """Determine if two vertices are not equal."""
        # If the type of the other object is not a Vertex, it is not equal
        if not isinstance(other, Vertex):
            return True

        # Otherwise, handle accordingly
        return self.id != other.id

    def __ge__(self, other):
        """Determine if this vertex is greater than or equal to other vert."""
        # Check the type of the other object, and raise error if type mismatch
        self._check_type(other, '>=')

        # Otherwise, handle accordingly
        return self.id >= other.id

    def __gt__(self, other):
        """Determine if this vertex is greater than other vertex."""
        # Check the type of the other object, and raise error if type mismatch
        self._check_type(other, '>')

        # Otherwise, handle accordingly
        return self.id > other.id

    def add_neighbor(self, vertex, weight=1):
        """Add a neighbor along a weighted edge."""
        # Check if vertex is already a neighbor
        if vertex in self.neighbors:
            # If so, raise KeyError
            raise KeyError(f"{vertex.id} is already a neighbor of {self.id}")
        # If not, add vertex to neighbors and assign weight
        self.neighbors[vertex] = weight

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        # Return the neighbors
        return set(self.neighbors.keys())

    def get_id(self):
        """Return the id of this vertex."""
        # Return the id of the vertex
        return self.id

    def get_edge_weight(self, vertex):
        """Return the weight of this edge."""
        # Return the weight of the edge from this vertex to the given vertex
        return self.neighbors[vertex]


class Graph:
    """Demonstrates the essential facts and functionalities of graphs."""

    def __init__(self, weighted=False, directed=True):
        """Initialize a graph object with an empty dictionary.

        vert_list: a dictionary of the vertices in this graph where:
            key = the id of a vertex
            value = a vertex object with an id that matches the key
        num_vertices: number of vertices in the graph
        """
        self.vert_list = {}
        self.num_vertices = 0
        self.weighted = weighted
        self.directed = directed

    def __iter__(self):
        """Iterate over the vertex objects in the graph.

        to use sytax: for v in g
        """
        return iter(self.vert_list.values())

    def add_vertex(self, key):
        """Add a new vertex object to the graph with the given key.

        Return the vertex if the vertex is new, else raise KeyError.
        """
        # Raise error if key already exists in graph
        if key in self.vert_list:
            raise KeyError(f"Vertex({key}) is already in the Graph")
        # Increment the number of vertices
        self.num_vertices += 1
        # Create a new vertex
        new_vertex = Vertex(key)
        # Add the new vertex to the vertex list
        self.vert_list[key] = new_vertex
        # Return the new vertex
        return new_vertex

    def get_vertex(self, key):
        """Return the vertex if it exists, else raise KeyError."""
        # Raise error if key does not exist in graph
        if key not in self.vert_list:
            raise KeyError(f"Vertex({key}) is not in the Graph")
        # Return the vertex if it is in the graph
        return self.vert_list[key]

    def add_edge(self, from_key, to_key, weight=1):
        """Add edge from vertex with key `from_key` to vertex with key `to_key`.

        If a weight is provided, use that weight.
        """
        if weight != 1 and not self.weighted:
            print(f"Detected weight of {weight} in unweighted graph.")
            print("Graph is now weighted, all previous vertices have weight 1")
            self.weighted = True

        # Add from_key vertex if it is not in the graph
        if from_key not in self.vert_list:
            self.add_vertex(from_key)

        # Add to_key vertex if it is not in the graph
        if to_key not in self.vert_list:
            self.add_vertex(to_key)

        # Get vertices from keys
        from_vert = self.vert_list[from_key]
        to_vert = self.vert_list[to_key]

        # When both vertices in graph, make from_vert a neighbor of to_vert
        from_vert.add_neighbor(to_vert, weight)
        # If the graph undirected, add connection back from to_vert to from_key
        if not self.directed:
            to_vert.add_neighbor(from_vert, weight)

    def get_vertices(self):
        """Return all the vertices in the graph."""
        return set(self.vert_list.values())

    def make_graph_from_file(self, file_name):
        """Read graph data from a file, and create a graph based on it."""
        valid_types = "gGdD"

        graph_type = ""
        vertices = ""
        edge_list = []
        directed = False
        weighted = False
        got_type = False

        with open(file_name, 'r') as f:
            for line in f.readlines():
                # Strip trailing whitespace
                line = line.rstrip()

                # Skip line if it is empty to prevent index range errors below
                if line == "":
                    # Moves to next line (next iteration of for loop)
                    continue

                # Find graph type
                if line[0] in string.ascii_letters and not got_type:
                    if line[0] in valid_types:
                        graph_type = line[0].upper()
                        got_type = True
                    else:
                        raise ValueError("Looking for type 'G' or 'D'")

                # Find list of vertices
                if line[0] in string.digits:
                    vertices = line

                # Find edges
                if line[0] == "(":
                    edge_list.append(line)

        # See if graph is a digraph
        if graph_type == "D":
            directed = True
        # See if graph is weighted
        if len(edge_list[0].split(",")) == 3:
            weighted = True

        # Set the graph type if it has not been set yet
        if self.num_vertices == 0:
            self.weighted = weighted
            self.directed = directed

        # Add vertices to graph
        # TODO: Does not handle string vertex names
        if vertices != "":
            for vertex in vertices.split(","):
                self.add_vertex(vertex)

        # Add edges to graph
        # TODO: Does not handle string vertex names or decimal weights
        for edge in edge_list:
            # Remove parenthesis
            data = edge[1:-1]
            # Turn data into array by splitting on commas
            data = data.split(",")

            # Split the tuple correctly
            if weighted:
                # Remove parenthesis from strings, and convert strings to ints
                self.add_edge(data[0], data[1], int(data[2]))
            else:
                # Remove parenthesis from strings, and convert strings to ints
                self.add_edge(data[0], data[1])

    def get_edge_list(self):
        """Return a list of edges (with their weights if weighted)."""
        edge_list = set()

        for from_vert in self.get_vertices():
            for to_vert in from_vert.get_neighbors():
                # If the graph is weighted, store the edge weight in a graph
                if self.weighted:
                    weight = from_vert.neighbors[to_vert]

                # If the graph is directed, as to edge list as normal
                if self.directed and self.weighted:
                    edge_list.add((from_vert.id, to_vert.id, weight))
                if self.directed and not self.weighted:
                    edge_list.add((from_vert.id, to_vert.id))

                # If the graph is undirected, make sure only one edge between
                # two vertices is counted. My implementation stores a directed
                # edge from and to both vertices for easier traversals.
                if not self.directed and self.weighted:
                    if (to_vert.id, from_vert.id, weight) not in edge_list:
                        edge_list.add((from_vert.id, to_vert.id, weight))
                if not self.directed and not self.weighted:
                    if (to_vert.id, from_vert.id) not in edge_list:
                        edge_list.add((from_vert.id, to_vert.id))

        return edge_list

    def breadth_first_search(self, vertex, n, only_new=True):
        """Find all vertices n edges away from the passed in vertex."""
        # Raise error if non vertex object is passed in as vertex
        if not isinstance(vertex, Vertex):
            raise TypeError("vertex parameter must be of type Vertex")

        # Raise error if vertex not in the graph
        if vertex not in self.get_vertices():
            raise ValueError(f"{vertex} is not in the Graph")

        # If the search is looking for vertices only accessible at level n,
        if only_new:
            # Create a set of vertices that have already been visited
            seen_vertices = set([vertex])

        # Create deque with passed in vertex
        vertex_deque = deque([vertex])
        # n_counter tracks the current level
        n_counter = 0
        # counter tracks how many vertices from level n are still in the deque
        counter = 1

        # Keep looping until there are no more vertices to go through, or
        # until the nth level has been reached
        while len(vertex_deque) > 0 and n_counter < n:
            # Grab a vertex from the front of the deque
            popped_vertex = vertex_deque.popleft()

            # Queue vertices if they will be seen for the first time
            if only_new:
                # Go through the neighbors of the popped_vertex
                for vert in popped_vertex.get_neighbors():
                    # If this vertex is new, allow it to be traversed
                    if vert not in seen_vertices:
                        # Set the parent of this vertex as the popped vertex
                        vert.parent = popped_vertex
                        # Add vertex to back of the deque
                        vertex_deque.append(vert)
                        # Mark that the vertex has been seen
                        seen_vertices.add(vert)
            # Otherwise, just add all vertices
            else:
                # Add all vertices that vert can reach to the back of the deque
                vertex_deque.extend(popped_vertex.get_neighbors())
            # Remove one from the counter because a vertex was just popped
            counter -= 1

            # When all nodes from the current level are removed
            if counter == 0:
                # Set the current level that all the current vertices are on
                n_counter += 1
                # Track how many vertices can be reached on this level
                counter = len(vertex_deque)

        # If the loop above ends early due to lack of levels,
        if n_counter < n:
            # Return empty set because no vertices exist n edges away
            return set()
        # Return a set of all the vertices that can be reached at the nth level
        return set(vertex_deque)

    def find_shortest_path(self, start, end):
        """Find the shortest path between two vertices."""
        # Raise error if start or end does not exist in graph
        if start not in self.vert_list:
            raise KeyError(f"Vertex({start}) is not in the Graph")
        if end not in self.vert_list:
            raise KeyError(f"Vertex({end}) is not in the Graph")

        # Set the starting and ending vertices, using start and end keys
        start_vert = self.vert_list[start]
        end_vert = self.vert_list[end]

        # Get the vertices one edge away from starting vertex
        level = 1
        verts_at_n_level = self.breadth_first_search(start_vert, level)
        # Keep searching levels there is nothing, or the end vertex is found
        while end_vert not in verts_at_n_level:
            # If there are no more vertices to search
            if len(verts_at_n_level) == 0:
                # Return None because there is no path between the vertices
                return None
            # Get the vertices one more edge away from the starting vertex
            level += 1
            verts_at_n_level = self.breadth_first_search(start_vert, level)

        # Create a path list and the ending vertex
        path = [end_vert]
        parent = end_vert
        # Go through the parents of each vertex, until start vertex is reached
        while start_vert != parent:
            # Move to the parent of the current vertex, and add it to the path
            parent = parent.parent
            path.append(parent)

        # Reverse the path, and return it
        path[:] = reversed(path)
        return path

    def depth_first_search(self, vertex, least_first=True, clear_parents=True):
        """Create DFS spanning tree by setting parent property of vertex."""
        # Raise error if non vertex object is passed in as vertex
        if not isinstance(vertex, Vertex):
            raise TypeError("vertex parameter must be of type Vertex")

        # Get set of vertices
        vertices = self.get_vertices()

        # Raise error if vertex not in the graph
        if vertex not in vertices:
            raise ValueError(f"Vertex({vertex}) is not in the Graph")

        # Ensure vertex does not have stale parent property from previous call
        if clear_parents:
            # For each vertex, set the parent to None
            for vert in vertices:
                vert.parent = None

            # Set starting vertex parent to False, it does not get a parent
            vertex.parent = False

        # If order matters, sort the neighbors
        if least_first:
            # Sort the neighbors
            neighbors = sorted(vertex.get_neighbors())
        else:
            # Otherwise, just get the unordered set
            neighbors = vertex.get_neighbors()

        # For each neighor of this vertex,
        for neighbor in neighbors:
            # Check if it does not have a parent
            if neighbor.parent is None:
                # If it doesn't, give it a parent
                neighbor.parent = vertex
                # Continue the depth first search (no return needed)
                self.depth_first_search(neighbor, least_first, False)

    def find_path(self, start, end):
        """Find any path from from_vert to to_vert."""
        # Raise error if vertex object is passed in as start or end
        if isinstance(start, Vertex) or isinstance(end, Vertex):
            raise TypeError("Expected vertex ids as start and end.")

        # Raise error if start or end keys do not exist in graph
        if start not in self.vert_list:
            raise KeyError(f"Vertex({start}) is not in the Graph")
        if end not in self.vert_list:
            raise KeyError(f"Vertex({end}) is not in the Graph")

        # Set the starting and ending vertices, using start and end keys
        start_vert = self.vert_list[start]
        end_vert = self.vert_list[end]

        # Run depth first tree that creates spanning tree of graph
        self.depth_first_search(start_vert, least_first=True)

        # Create a path list and the ending vertex
        path = [end_vert]
        parent = end_vert
        # Go through the parents of each vertex, until start vertex is reached
        while start_vert != parent:
            # If parent is None, the spanning tree is broken, no path exists
            if parent is None:
                # Return None as no path exists betwen the start and end vertex
                return None

            # Move to the parent of the current vertex, and add it to the path
            parent = parent.parent
            path.append(parent)

        # Reverse the path, and return it
        path[:] = reversed(path)
        return path

    def find_maximal_clique(self, vertex=None, least_first=True):
        """Return a maximal clique of a given vertex."""
        # Raise error if non vertex object is passed in as vertex
        if not isinstance(vertex, Vertex) and vertex is not None:
            raise TypeError("vertex parameter must be of type Vertex")

        # Raise error if called when graph is directed
        if self.directed:
            raise TypeError("maximal_clique can't be called on directed graph")

        # If looking for random maximal clique,
        if vertex is None:
            # Set the vertex parameter to randomly selected vertex
            vertex = random.choice(list(self.get_vertices()))

        # Raise error if vertex not in the graph
        if vertex not in self.get_vertices():
            raise ValueError(f"Vertex({vertex}) is not in the Graph")

        # Initialize clique as a set of vertices
        clique = set([vertex])

        # If order matters, sort the neighbors
        if least_first:
            # Sort the neighbors
            neighbors = sorted(vertex.get_neighbors())
        else:
            # Otherwise, just get the unordered set
            neighbors = vertex.get_neighbors()

        # Clique members must be neighor of vertex parameter
        for neighor in neighbors:
            # Keep track of clique memebers that are adjacent to neighor
            clique_counter = 0
            # Check each clique member if it is adjacent to current neighor
            for clique_member in clique:
                # If the current neighor is not adjacent to this clique member
                if neighor not in clique_member.get_neighbors():
                    # Break out of this loop, and move to next neighor
                    break
                # If it is, increase the count of adjacent clique members
                clique_counter += 1
                # If all clique members are adjacent to current neighor,
                if clique_counter == len(clique):
                    # Add the current neighor to the clique
                    clique.add(neighor)
                    # Make sure to break out of loop
                    # Avoids RuntimeError: Set changed size during iteration
                    break

        # After all neighors checked, return the clique
        return clique

    def is_connected(self):
        """Return if this graph is connected.

        Use edge list to check if directed graph is connected.
        Edge list will also handle if undirected graph is connected.
        """
        # Need to check all edges to see if connected
        all_edges = deque(self.get_edge_list())

        # If the graph only has one vertex, it is connected
        if self.num_vertices == 1:
            return True

        # If there are no edges, the graph is not connected
        if len(all_edges) == 0:
            return False

        # Get all vertex keys to check that they are all connected
        all_vert_keys = set(self.vert_list.keys())
        # The actual keys of the connected vertices
        # A key will not show up if it has 0 degree
        actual_vert_keys = set()

        # Initialize actual_vert_keys with the vertices of a random edge
        start_edge = all_edges.popleft()
        actual_vert_keys.add(start_edge[0])
        actual_vert_keys.add(start_edge[1])

        # Edge counter will track if anymore edges could have new vertices
        edge_counter = 0
        # While there are still edges to check,
        while len(all_edges) > 0:
            # Get the edge and vertices at the start of the queue
            edge = all_edges.popleft()
            from_vert = edge[0]
            to_vert = edge[1]

            # Check if one vertex key is inside the set of connected keys
            if from_vert in actual_vert_keys or to_vert in actual_vert_keys:
                # If a key is already inside, both vertices are connected
                actual_vert_keys.add(from_vert)
                actual_vert_keys.add(to_vert)
                # Since a new vertex was added, all other edges could be added
                edge_counter = 0
            else:
                # If no vertices can be added now, they could be added later
                # Add edge to the back of the queue
                all_edges.append(edge)
                # Keep track of number of edges with verts that can't be added
                edge_counter += 1

            # If no more vertices can be added, the graph is not connected
            if edge_counter > len(all_edges):
                return False

        # If all edges have been checked, and all keys are here,
        if all_vert_keys == actual_vert_keys:
            # the graph is connected
            return True
        # Handles case where loop never enters (only 1 edge)
        else:
            return False

    def is_eulerian(self, is_connected=True):
        """Return if this undirected graph is an Eulerian Cycle."""
        # Raise error if called when graph is directed
        if self.directed:
            raise TypeError("is_eulerian can't be called on directed graph")

        # If the graph needs to be connected, but it is not,
        if is_connected and not self.is_connected():
            # The graph is not Eulerian
            return False

        # Check all vertices in self for their degree
        for vertex in self:
            # If a vertex has an odd degree, the graph is not Eulerian
            if len(vertex.get_neighbors()) % 2 == 1:
                return False

        # If all vertices have an even degree, the graph is Eulerian
        return True

    def reverse_directions(self):
        """Return dictionary of vertices and vertcies that lead into them."""
        reverse_dict = {}

        for from_vert in self:
            for to_vert in from_vert.get_neighbors():
                if to_vert in reverse_dict:
                    reverse_dict[to_vert].add(from_vert)
                else:
                    reverse_dict[to_vert] = set([from_vert])

        return reverse_dict

    def diameter(self):
        """Return the diameter of the graph."""
        pass

    def influencer(self, iterations=30):
        """Calculate the influence of each vertex."""
        # All vertices start with the same rank: 1 / number of vertices
        ranks = {vertex: 1 / self.num_vertices for vertex in self}

        # Get all vertices and vertices that lead into those vertices
        reverse_dict = self.reverse_directions()

        # Calculate the rank "iterations" number of times
        for _ in range(iterations):
            new_ranks = {}

            # Calculate new rank for each vertex
            for vertex in ranks:
                new_rank = 0

                # Each rank for a given vertex depends on the vertices
                # directing into it
                for from_vert in reverse_dict[vertex]:
                    # Portion of rank provided by from_vert is:
                    # from_vert's previous rank
                    # ------- divided by -------
                    # number of vertices from_vert directs into
                    portion = ranks[from_vert] / len(from_vert.get_neighbors())
                    # Each from_vert leading into this vertex contributes to
                    # this vertex's rank
                    new_rank += portion

                # Set new rank for this vertex
                new_ranks[vertex] = new_rank

            # Reset ranks after all of the new ranks have been calculated
            ranks = new_ranks.copy()

        # Create a list of vertex ids and their ranks
        rank_list = [(rank, vert.id) for vert, rank in ranks.items()]
        # Sort the vertices by their rank
        rank_list.sort()

        return rank_list


# Driver code
if __name__ == "__main__":
    pass
