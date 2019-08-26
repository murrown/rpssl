from django.contrib.auth.models import User
from django.db import models

WIN, LOSE, DRAW = 1, 0, 2
ROCK, PAPER, SCISSORS, SPOCK, LIZARD = 1, 2, 3, 4, 5
VICTORY_MAP = {
    ROCK:       {SCISSORS, LIZARD},
    PAPER:      {ROCK, SPOCK},
    SCISSORS:   {PAPER, LIZARD},
    SPOCK:      {ROCK, SCISSORS},
    LIZARD:     {PAPER, SPOCK},
}

CHOICE_NAMES = {
    ROCK: 'rock',
    PAPER: 'paper',
    SCISSORS: 'scissors',
    SPOCK: 'spock',
    LIZARD: 'lizard',
}

RESULT_NAMES = {
    WIN: 'win',
    LOSE: 'lose',
    DRAW: 'tie',
}


class Game(models.Model):
    """
    The Game model stores information about a single game of RPSSL
    """
    player = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    player_choice = models.IntegerField(default=0, null=False)
    computer_choice = models.IntegerField(default=0, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_response(self):
        """
        Reports the results of this round of the game.

        @return: a data dictionary containing the results for the round,
            suitable for JSON serialization.
        """
        if self.player_choice == self.computer_choice:
            results = RESULT_NAMES[DRAW]
        elif self.computer_choice in VICTORY_MAP[self.player_choice]:
            results = RESULT_NAMES[WIN]
        else:
            assert self.player_choice in VICTORY_MAP[self.computer_choice]
            results = RESULT_NAMES[LOSE]

        return {'results': results,
                'player': self.player_choice,
                'computer': self.computer_choice}
