import json
from base64 import b64encode
from time import sleep

from django.test import TestCase
from game.models import Game, VICTORY_MAP, CHOICE_NAMES

REVERSE_CHOICE_NAMES = dict([(v, k) for (k, v) in CHOICE_NAMES.items()])


class TestAPI(TestCase):
    fixtures = ['empty_fixture.json']

    def test_winning_combinations(self):
        for a, b in [
                ('rock', 'scissors'),
                ('rock', 'lizard'),
                ('paper', 'rock'),
                ('paper', 'spock'),
                ('scissors', 'paper'),
                ('scissors', 'lizard'),
                ('spock', 'rock'),
                ('spock', 'scissors'),
                ('lizard', 'paper'),
                ('lizard', 'spock')]:
            g = Game.objects.create(player_choice=REVERSE_CHOICE_NAMES[a],
                                    computer_choice=REVERSE_CHOICE_NAMES[b])
            self.assertEqual(g.get_response()['results'], 'win')

    def test_losing_combinations(self):
        for a, b in [
                ('rock', 'scissors'),
                ('rock', 'lizard'),
                ('paper', 'rock'),
                ('paper', 'spock'),
                ('scissors', 'paper'),
                ('scissors', 'lizard'),
                ('spock', 'rock'),
                ('spock', 'scissors'),
                ('lizard', 'paper'),
                ('lizard', 'spock')]:
            g = Game.objects.create(player_choice=REVERSE_CHOICE_NAMES[b],
                                    computer_choice=REVERSE_CHOICE_NAMES[a])
            self.assertEqual(g.get_response()['results'], 'lose')

    def test_draw_combinations(self):
        for a in ['rock', 'paper', 'scissors', 'spock', 'lizard']:
            g = Game.objects.create(player_choice=REVERSE_CHOICE_NAMES[a],
                                    computer_choice=REVERSE_CHOICE_NAMES[a])
            self.assertEqual(g.get_response()['results'], 'tie')

    def test_computer_ai(self):
        for _ in range(3):
            for _ in range(4):
                Game.objects.create(
                    player_choice=REVERSE_CHOICE_NAMES['rock'],
                    computer_choice=REVERSE_CHOICE_NAMES['rock'])

            for _ in range(5):
                data = json.dumps({'player': REVERSE_CHOICE_NAMES['rock']})
                response = self.client.generic('POST', '/play/', data)
                response_dict = json.loads(response.content.decode())
                self.assertEqual(response_dict['results'], 'lose')
                self.assertIn(response_dict['computer'], {
                    REVERSE_CHOICE_NAMES['paper'], REVERSE_CHOICE_NAMES['spock']})

            Game.objects.all().delete()
