import time
from graph import Graph
from hyphenator import read_patterns_file, parse_word


def get_edges(syllables):
    """Get the edges by using the hyphenator."""
    start = time.time()
    trie = read_patterns_file()

    content = []
    with open("enable1.txt") as file:
        content = [line.rstrip() for line in file]
        file.close()

    for line in content:
        result = parse_word(line, trie)
        word_syllables = result.split("-")
        if word_syllables[0] == "a":
            print(word_syllables)

    end = time.time()
    print(f"{end - start} seconds to process enable1 List")


def main():
    """Run the project."""
    common_syllables = ['ing', 'er', 'a', 'ly', 'ed', 'i', 'es', 're', 'tion',
                        'in', 'e', 'con', 'y', 'ter', 'ex', 'al', 'de', 'com',
                        'o', 'di', 'en', 'an', 'ty', 'ry', 'u', 'ti', 'ri',
                        'be', 'per', 'to']
    syllables_set = set(common_syllables)

    graph = Graph()
    for syllable in common_syllables:
        graph.add_vertex(syllable)

    get_edges(syllables_set)


if __name__ == '__main__':
    main()
