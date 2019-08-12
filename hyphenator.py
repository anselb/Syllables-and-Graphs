import time
# Words from https://github.com/dolph/dictionary
# Patterns from https://gist.githubusercontent.com/cosmologicon/1e7291714094d71a0e25678316141586/raw/006f7e9093dc7ad72b12ff9f1da649822e56d39d/tex-hyphenation-patterns.txt
# Code from https://www.reddit.com/r/dailyprogrammer/comments/8qxpqd/20180613_challenge_363_intermediate_word/e2uhjs5/


class TrieNode:
    def __init__(self, letter, value, parent, isWord):
        self.letter = letter
        self.value = value
        self.parent = parent
        self.children = {}
        self.isWord = isWord

    def get(self, key):
        if key in self.children:
            return self.children[key]
        else:
            return -1

    def add(self, node):
        if node.get_letter() not in self.children:
            self.children[node.get_letter()] = node
            return node
        else:
            return self.get(node.get_letter())

    def get_letter(self):
        return self.letter

    def get_is_word(self):
        return self.isWord

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Trie:
    def __init__(self):
        self.children = {}

    def get(self, key):
        if key in self.children:
            return self.children[key]
        else:
            return -1

    def create_value_dict(self, word):
        valueDict = {}
        modifiedword = word.replace(".", "")
        amountOfNumbers = 0
        for x in range(0, len(modifiedword)):
            try:
                int(modifiedword[x])
                valueDict[x-amountOfNumbers] = int(modifiedword[x])
                amountOfNumbers += 1
            except ValueError:
                continue
        return valueDict

    def add(self, word):
        valueDict = self.create_value_dict(word)
        modifiedWord = ''.join([i for i in word if not i.isdigit()])

        if modifiedWord[0] not in self.children:
            self.children[modifiedWord[0]] = TrieNode(modifiedWord[0], 0, self, False)
        currentParent = self.get(modifiedWord[0])

        for x in range(1, len(modifiedWord)):
            isLastLetter = (x == len(modifiedWord)-1)
            node = TrieNode(modifiedWord[x], 0, currentParent, isLastLetter)
            currentParent = currentParent.add(node)
            if isLastLetter:
                currentParent.set_value(valueDict)


def read_patterns_file():
    start = time.time()
    trie = Trie()
    content = []
    with open("patterns.txt") as file:
        content = [line.rstrip() for line in file]
        file.close()
    for line in content:
        trie.add(line)
    end = time.time()
    print(str(end - start) + " trie built")
    return trie


def attempt_to_match_pattern(index, word, trie):
    pattern = ""
    nextNode = trie
    valueDict = {}

    for x in range(index, len(word)):
        letter = word[x]
        nextNode = nextNode.get(letter)
        if nextNode != -1:
            pattern += letter
            if nextNode.get_is_word():
                resultDict = nextNode.get_value()
                pattern = ""
                for x in resultDict.items():
                    previousValue = valueDict.get(x[0]+index, 0)
                    if previousValue < x[1]:
                        valueDict[x[0]+index] = x[1]
        else:
            return valueDict if len(valueDict) > 0 else False
    return valueDict if len(valueDict) > 0 else False


def parse_word(word, trie):
    values = [0] * len(word)
    results = []
    for x in range(0, len(word)):
        res = attempt_to_match_pattern(x, word, trie)
        resBack = attempt_to_match_pattern(x, word+".", trie)
        if res is not False:
            results.append(res)
        if resBack is not False:
            results.append(resBack)
    resFirst = attempt_to_match_pattern(0, "."+word, trie)
    results.append(resFirst) if resFirst is not False else None

    mainDict = {}
    for x in range(0, len(results)):
        for x in results[x].items():
            if mainDict.setdefault(x[0], 0) < x[1]:
                mainDict[x[0]] = x[1]

    finalWord = ""
    for x in range(0, len(word)):
        if(mainDict.get(x) is not None and mainDict.get(x) % 2 != 0 and x != 0 and x != len(word)):
            finalWord += "-"
        finalWord += word[x]
    return finalWord


def process_enable1():
    start = time.time()
    trie = read_patterns_file()
    hyphenCounts = {key: 0 for key in range(0, 10)}
    content = []
    with open("enable1.txt") as file:
        content = [line.rstrip() for line in file]
        file.close()
    for line in content:
        result = parse_word(line, trie)
        amount = result.count("-")
        hyphenCounts[amount] += 1
    print(hyphenCounts)
    end = time.time()
    print(str(end - start) + " Seconds to process enable1 List")
