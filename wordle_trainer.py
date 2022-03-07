class WordleTrainer:
    def __init__(self, word_to_guess: str):
        self.__word_to_guess = word_to_guess

    def guess(self, guess: str) -> str:
        if guess == self.__word_to_guess:
            return '*****'

        result = []
        for i in range(len(guess)):
            if guess[i] == self.__word_to_guess[i]:
                result.append('*')
            elif guess[i] in self.__word_to_guess:
                result.append('?')
            else:
                result.append('_')

        return "".join(result)

