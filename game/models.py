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
    player = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, db_index=True)
    player_choice = models.IntegerField(default=0, null=False)
    history1 = models.IntegerField(default=0, null=False)
    history2 = models.IntegerField(default=0, null=False)
    history3 = models.IntegerField(default=0, null=False)
    computer_choice = models.IntegerField(default=0, null=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        index_together = [("player", "history1", "history2", "history3"),
                          ("history1", "history2", "history3"),
                          ("player", "created"),
                         ]

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

    def get_record(self):
        data = self.get_response()
        data['results'] = data['results'].upper()
        data['player'] = CHOICE_NAMES[data['player']]
        data['computer'] = CHOICE_NAMES[data['computer']]
        if self.player is None:
            data['player_name'] = 'ANONYMOUS PLAYER'
        else:
            data['player_name'] = self.player.username
        return data

    def save(self, *args, **kwargs):
        history = [g.player_choice for g in Game.objects.filter(
            player=self.player).order_by("-created")[:3]]
        while len(history) < 3:
            history.append(0)
        self.history1, self.history2, self.history3 = history
        super(Game, self).save(*args, **kwargs)
