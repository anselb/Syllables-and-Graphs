from graph import Graph
import sys


def main():
    """Run the challenge with a passed in graph file name."""
    if len(sys.argv) < 2:
        print("Please enter a file name.")
    graph_file = sys.argv[1]

    graph = Graph()
    graph.make_graph_from_file(graph_file)
    is_eulerian = graph.is_eulerian()

    print(f"This graph is Eulerian: {is_eulerian}")


if __name__ == '__main__':
    main()
