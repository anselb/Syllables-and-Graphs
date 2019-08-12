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


def main():
    """Run the project."""
    common_syllables = ['ing', 'er', 'a', 'ly', 'ed', 'i', 'es', 're', 'tion',
                        'in', 'e', 'con', 'y', 'ter', 'ex', 'al', 'de', 'com',
                        'o', 'di', 'en', 'an', 'ty', 'ry', 'u', 'ti', 'ri',
                        'be', 'per', 'to']
    syllables_set = set(common_syllables)

    graph = Graph(weighted=True, directed=True)
    for syllable in common_syllables:
        graph.add_vertex(syllable)

    edges = get_edges(syllables_set)
    for edge in edges:
        from_vert = edge[0]
        to_vert = edge[1]
        weight = edges[edge]
        graph.add_edge(from_vert, to_vert, weight)


if __name__ == '__main__':
    main()
