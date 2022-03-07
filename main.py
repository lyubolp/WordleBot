from collections import namedtuple
from random import randint
from typing import List, Optional

Entry = namedtuple('Entry', ['word', 'score'])




if __name__ == '__main__':
    bot = WordleBot("words", starter="crane")
    bot.play()

