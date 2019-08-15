import time
import random
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


def generate_word(graph):
    syllable_counts = {1: 21830, 2: 56852, 3: 50452, 4: 26630, 5: 11751,
                       6: 4044, 7: 1038, 8: 195, 9: 30, 10: 1}
    word_count = sum(syllable_counts.values())
    rand_int = random.randint(1, word_count)

    word_length = 0
    word_counter = 21830
    for syllable_count in syllable_counts:
        num_words = syllable_counts[syllable_count]
        if rand_int >= word_counter:
            word_counter += num_words
        else:
            word_length = syllable_count
            break

    syllables = graph.stochastic_walk(word_length)
    word = ""
    for syllable in syllables:
        word += syllable.id
    return word


def main():
    """Run the project."""
    graph = Graph(weighted=True, directed=True)
    graph.make_graph_from_file("syllable_graph.txt")

    # print(graph.longest_walk())

    # Generate Words
    print("Here are three randomly generated words:")
    print(f"1. {generate_word(graph)}")
    print(f"2. {generate_word(graph)}")
    print(f"3. {generate_word(graph)}")
    print("")

    # Add edge from 'er' to 'y' to make algorithm work better (bakery)
    graph.add_edge('er', 'y', 1)

    # Diameter
    diameter_info = graph.diameter()
    diameter = diameter_info[0]
    start = diameter_info[1]
    end = diameter_info[2]
    print(f"Diameter: {diameter}")
    shortest_path = graph.find_shortest_path(start.id, end.id)
    print(f"Path with length of diameter: {[v.id for v in shortest_path]}\n")

    # Syllable influence
    print("Which syllable has the greatest influence?")
    ranks = graph.influencer()
    for i in range(len(ranks)):
        print(f"{i + 1}. {ranks[i][1]}: {ranks[i][0]}")


if __name__ == '__main__':
    main()
