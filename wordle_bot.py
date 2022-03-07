from collections import namedtuple
from random import randint
from typing import List, Optional

Entry = namedtuple('Entry', ['word', 'score'])


class WordleBot:
    def __init__(self, words_file_path: str, starter: Optional[str] = None, tries: int = 5):
        self.__words = self.__open_words(words_file_path)
        self.__starter = starter
        self.__tries = tries

    def play(self) -> bool:
        if self.__starter is None:
            self.__starter = self.__get_random_starer()

        current_word = self.__starter
        for i in range(5):
            result = input("Please enter the result from Wordle: _ if no match, ? if letter is in word, * for exact match")

            if result == '*****':
                return True

            next_word = self.get_next_word(Entry(current_word, result))
            print(next_word)
            current_word = next_word

        return False

    def get_next_word(self, entry: Entry) -> str:
        possible_words = self.__filter_words(entry)

        distances = sorted([(word, self.__edit_distance(entry.word, word)) for word in possible_words],
                           key=lambda x: x[1])

        target_distances = distances[0][1]

        possible_results = [distance for distance in distances if distance[1] == target_distances]

        if len(possible_results) > 0:
            return possible_results[randint(0, len(possible_results))][0]
        else:
            return possible_results[0][0]

    def __get_random_starer(self) -> str:
        return self.__words[randint(0, len(self.__words))]

    def __filter_words(self, entry: Entry) -> List[str]:
        return [word for word in self.__words if self.__is_word_possible(entry, word)]

    @staticmethod
    def __open_words(path: str) -> List[str]:
        lines = []

        with open(path, 'r') as f:
            lines = f.readlines()

        return sorted([line.strip() for line in lines])

    @staticmethod
    def __edit_distance(source_word: str, target_word: str) -> int:
        if source_word == '':
            return len(target_word)

        if target_word == '':
            return len(source_word)

        if source_word[-1] == target_word[-1]:
            return WordleBot.__edit_distance(source_word[:-1], target_word[:-1])

        result = 1 + min(WordleBot.__edit_distance(source_word[:-1], target_word[:-1]),
                         WordleBot.__edit_distance(source_word[:-1], target_word),
                         WordleBot.__edit_distance(source_word, target_word[:-1])
                        )

        return result

    @staticmethod
    def __is_word_possible(entry: Entry, target_word: str) -> bool:
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
