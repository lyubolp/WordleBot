from collections import namedtuple
from random import randint
from typing import List

Entry = namedtuple('Entry', ['word', 'score'])



def open_words(path: str) -> List[str]:
    lines = []

    with open(path, 'r') as f:
        lines = f.readlines()

    return sorted([line.strip() for line in lines])


def edit_distance(source_word: str, target_word: str) -> int:
    # print(source_word, target_word)
    if source_word == '':
        return len(target_word)

    if target_word == '':
        return len(source_word)

    if source_word[-1] == target_word[-1]:
        return edit_distance(source_word[:-1], target_word[:-1])

    result = 1 + min(edit_distance(source_word[:-1], target_word[:-1]),
                     edit_distance(source_word[:-1], target_word),
                     edit_distance(source_word, target_word[:-1])
                    )

    return result


def is_word_possible(entry: Entry, target_word: str) -> bool:
    guess = entry.score

    for i, c in enumerate(guess):
        if c == '_':
            for j in range(5):
                if entry.word[i] == target_word[j] and entry.score[j] != '*':
                    return False
        elif c == '*' and entry.word[i] != target_word[i]:
            return False
        elif c == '?' and (entry.word[i] not in target_word or entry.word[i] == target_word[i]):
            return False

    return True


def filter_words(entry: Entry, words: List[str]) -> List[str]:
    return [word for word in words if is_word_possible(entry, word)]


def get_next_word(entry: Entry, words: List[str]) -> str:
    possible_words = filter_words(entry, words)

    distances = sorted([(word, edit_distance(entry.word, word)) for word in possible_words],
                       key=lambda x: x[1])

    target_distances = distances[0][1]

    possible_results = [distance for distance in distances if distance[1] == target_distances]

    if len(possible_results) > 0:
        return possible_results[randint(0, len(possible_results))][0]
    else:
        return possible_results[0][0]


if __name__ == '__main__':
    words = open_words("words")

    initial_word = words[randint(0, len(words))]

    initial_word = "crane"
    print(initial_word)

    current_word = initial_word
    for i in range(5):
        result = input("Please enter the result from Wordle: _ if no match, ? if letter is in word, * for exact match")

        if result == '*****':
            print("I WON !")
            break

        next_word = get_next_word(Entry(current_word, result), words)
        print(next_word)
        current_word = next_word

