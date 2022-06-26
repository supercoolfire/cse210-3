import random
from game.seeker import Seeker
import os
import sys


class Hider:
    """The person hiding from the Seeker.

    The responsibility of Hider is to keep track of its location and distance from the seeker.

    Attributes:
        _location (int): The location of the hider (1-1000).
        _distance (List[int]): The distance from the seeker.
    """

    def __init__(self):
        """Constructs a new Hider.

        Args:
            self (Hider): An instance of Hider.
        """

        # self._word = 'tae'
        try:
            self._word = random.choice(
                open(f'{os.path.dirname(os.path.abspath(__file__))}\words.txt').read().split()).upper()
        except FileNotFoundError:
            try:
                with open(os.path.join(sys.path[0], "game\words.txt"), "r") as f:
                    self._wordydordies = [line.strip() for line in f]
            except FileNotFoundError:
                self._wordydordies = [
                    'the quick brown fox jumped over the lazy dogs',
                    'HANGING MAN',
                    'PARACHUTE MAN',
                    'BATMAN',
                    'but man',
                    'and man',
                    'because man',
                    'although man',
                    'yet man',
                    'since man',
                    'unless man',
                    'or man',
                    'nor man',
                    'while man',
                    'where man',
                    'monkey man',
                    'what',
                    'cat',
                ]
            self._word = random.choice(self._wordydordies).upper()
        # self._word = 'HANGINGMAN'
        self._answer = []
        self._entries = []
        self._jumper = [
            " ___",
            "/___\\",
            "\   /",
            " \ /",
            "  O",
            " /|\\",
            " / \\",
            " ",
            "^^^^^^^",
        ]
        self._keyboard = [
            "╭───┬───┬───┬───┬───┬───┬───┬───┬───┬───╮",
            "│ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │",
            "╰─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─╯",
            "  │ A │ S │ D │ F │ G │ H │ J │ K │ L │",
            "  ╰─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───╯",
            "    │ Z │ X │ C │ V │ B │ N │ M │ ",
            "    ╰───┴───┴───┴───┴───┴───┴───╯"
        ]
        self._keyboard_entry = []
        self._lives = 4
        for i in self._word:
            if i == ' ':
                self._answer.append(' ')
            else:
                self._answer.append('_')
        self._index_of = 0

        self._right_letters = []
        self._wrong_letters = []

    def get_answer(self):
        """Gets a answer for the seeker.

        Args:
            self (Hider): An instance of Hider.

        Returns:
            string: A answer for the seeker.
        """
        answer = " ".join(self._answer)

        return answer

    def get_lives(self):
        lives = f'Lives left: {self._lives}'
        return lives

    def get_jumper_keyboard(self):
        left_offset = 0
        top_offset = 0
        print(f'\x1b[{str(top_offset)}F', end='')
        for i in range(len(self._keyboard)):
            print(f'\n\x1b[{str(left_offset)}C', end='')
            for j in range(len(self._keyboard[i])):
                if self._keyboard[i][j] in self._wrong_letters:
                    print(
                        f'\x1b[7;30;41m{self._keyboard[i][j]}\x1b[0m', end='')
                elif self._keyboard[i][j] in self._right_letters:
                    print(
                        f'\x1b[7;30;44m{self._keyboard[i][j]}\x1b[0m', end='')
                else:
                    print(self._keyboard[i][j], end='')

    def is_game_over(self):
        """Whether or not the hider has been found.

        Args:
            self (Hider): An instance of Hider.

        Returns:
            boolean: True if the hider was found; false if otherwise.
        """
        returning = False

        if self._lives == 0:
            print(f'\nThe word is {self._word}')
            print("GAME OVER!")
            returning = True

        # if every character in answer is replace,
        # that mean no more underscore _
        if '_' not in self._answer:
            print("\nYOU WIN!")
            returning = True
            # print(self._answer)

        return returning

    def watch_seeker(self, seeker):
        """Watches the seeker by keeping track of how far away it is.

        Args:
            self (Hider): An instance of Hider.
        """
        letter = seeker.get_guess()
        index_of = 0
        if letter in self._word:
            # getting the index of where is ans located in word
            # index_of = self._word.index(letter)
            # print(f'the index is {index_of}')
            # set collected input
            # self._answer[index_of] = letter

            for i in range(len(self._word)):
                if self._word[i] == letter:
                    self._answer[i] = letter
                if self._word[i] == ' ':
                    self._answer[i] = ' '

            self._right_letters.append(letter)
        else:
            self._wrong_letters.append(letter)
            # reduce lives
            self._lives = self._lives - 1
            # remove first index in jumper
            self._jumper.pop(0)
            # replace head with x
            if len(self._jumper) == 5:
                self._jumper[0] = "  x"
