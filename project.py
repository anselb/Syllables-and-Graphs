import time
from graph import Graph
from hyphenator import read_patterns_file, parse_word


def get_edges(syllables):
    """Get the edges by using the hyphenator."""
    start = time.time()
    edges = {}
    trie = read_patterns_file()

    content = []
    with open("enable1.txt") as file:
        content = [line.rstrip() for line in file]
        file.close()

    for line in content:
        result = parse_word(line, trie)
        word_syllables = result.split("-")

        for syl_ind in range(len(word_syllables) - 1):
            pre_syl = word_syllables[syl_ind]
            next_syl = word_syllables[syl_ind + 1]
            if pre_syl in syllables and next_syl in syllables:
                edge = (pre_syl, next_syl)
                if edge in edges:
                    edges[edge] += 1
                else:
                    edges[edge] = 1

    end = time.time()
    print(f"{end - start} seconds to process enable1 List")

    return edges


def old_main():
    """Old code for creating graph using hyphenator."""
    common_syllables = ['ing', 'er', 'a', 'ly', 'ed', 'i', 'es', 're', 'tion',
                        'in', 'e', 'con', 'y', 'ter', 'ex', 'al', 'de', 'com',
                        'o', 'di', 'en', 'an', 'ty', 'ry', 'u', 'ti', 'ri',
                        'be', 'per', 'to']
    syllables_set = set(common_syllables)

    graph = Graph(weighted=True, directed=True)

    # Make graph using hyphenator
    for syllable in common_syllables:
        graph.add_vertex(syllable)

    edges = get_edges(syllables_set)
    for edge in edges:
        from_vert = edge[0]
        to_vert = edge[1]
        weight = edges[edge]
        graph.add_edge(from_vert, to_vert, weight)

    # Write edge info to graph
    with open("syllable_graph.txt", "w") as file:
        file.write("D\n")
        vertices = ",".join(common_syllables)
        file.write(vertices + "\n")
        for edge in edges:
            data = f"({edge[0]},{edge[1]},{edges[edge]})\n"
            file.write(data)

    verify_graph(graph)


def verify_graph(graph):
    """Vertify that file write is accurate.

    30 vertices, 284 edges
    """
    sum = 0
    for vertex in graph.get_vertices():
        sum += len(vertex.get_neighbors())
    print(len(graph.get_vertices()))
    print(sum)


def main():
    """Run the project."""
    graph = Graph(weighted=True, directed=True)
    graph.make_graph_from_file("syllable_graph.txt")

    # Used to verify that file write is accurate
    # verify_graph(graph)


if __name__ == '__main__':
    main()
