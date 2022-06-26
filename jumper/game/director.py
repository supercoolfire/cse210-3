from game.seeker import Seeker
from game.hider import Hider
from game.terminal_service import TerminalService

import subprocess
import sys
while True:
    try:
        import ansicon
        ansicon.load()
        # print(u'\x1b[32mIf you see this color GREEN means ansicom is working.\x1b[m')
        break
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                               'ansicon'])


class Director:
    """A person who directs the game.

    The responsibility of a Director is to control the sequence of play.

    Attributes:
        hider (Hider): The game's hider.
        is_playing (boolean): Whether or not to keep playing.
        seeker (Seeker): The game's seeker.
        terminal_service: For getting and displaying information on the terminal.
    """

    def __init__(self):
        """Constructs a new Director.

        Args:
            self (Director): an instance of Director.
        """
        self._hider = Hider()
        self._is_playing = True
        self._seeker = Seeker()
        self._terminal_service = TerminalService()
        self._run_once = True

    def start_game(self):
        """Starts the game by running the main game loop.

        Args:
            self (Director): an instance of Director.
        """
        while self._is_playing:
            self._get_inputs()
            self._do_updates()
            self._do_outputs()

    def _get_inputs(self):
        """Moves the seeker to a new location.

        Args:
            self (Director): An instance of Director.
        """
        while self._run_once:
            # prepare graphics area
            print('\n\n\n\n\n\n')

            # show game info
            answer = self._hider.get_answer()
            self._terminal_service.write_text(answer)

            # print every line in jumper
            for line in self._hider._jumper:
                self._terminal_service.write_text(line)

            # show lives left
            lives = self._hider.get_lives()
            self._terminal_service.write_text(lives)

            # show jumper on left keybaord on right
            self._hider.get_jumper_keyboard()

            self._run_once = False

        ans = self._terminal_service.read_number(
            "\nGuess a letter of a word: ")

        self._seeker.set_guess(ans)

    def _do_updates(self):
        """Keeps watch on where the seeker is moving.

        Args:
            self (Director): An instance of Director.
        """
        self._hider.watch_seeker(self._seeker)

    def _do_outputs(self):
        """Provides a answer for the seeker to use.

        Args:
            self (Director): An instance of Director.
        """
        print('\n\n\n\n\n\n')
        # show game info
        answer = self._hider.get_answer()
        self._terminal_service.write_text(answer)

        # print every line in jumper
        for line in self._hider._jumper:
            self._terminal_service.write_text(line)

        # show lives left
        lives = self._hider.get_lives()
        self._terminal_service.write_text(lives)

        # show jumper on left keybaord on right
        self._hider.get_jumper_keyboard()

        if self._hider.is_game_over():
            self._is_playing = False
