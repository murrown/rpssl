import json
from requests import get
from random import randint
from time import sleep

from django.conf import settings
from django.http import (
        JsonResponse, HttpResponseBadRequest)
from django.shortcuts import render
from game.models import CHOICE_NAMES, Game


RNG_URI = 'https://codechallenge.boohma.com/random'
NUM_TIMEOUT_RETRIES = 5


def get_choices(request):
    """
    Handler for API calls of the form GET /choices

    @param request: The request for this API call. (only used for method)
    @return: JSON response containing all valid choices.
    """
    if request.method != 'GET':
        return HttpResponseBadRequest()

    response = []
    for choice_id, choice_name in sorted(CHOICE_NAMES.items()):
        response.append({"choice": {"id": choice_id, "name": choice_name}})
    return JsonResponse(response, safe=False)

def get_random_choice():
    """
    Generate a random number that is a valid choice for an action in the game.
    Attempts to use an external API if configured to do so.

    @return: An integer between 1 and 5 representing a gameplay choice.
    """
    if settings.USE_RNG_API:
        for _ in range(NUM_TIMEOUT_RETRIES):
            response = get(RNG_URI).json()
            try:
                value = response['random_number']
            except KeyError:
                sleep(1)
                continue
            return (value % 5) + 1
    return randint(1, 5)

def get_choice(request):
    """
    Handler for API calls of the form GET /choice

    @param request: The request for this API call. (only used for method)
    @return: JSON response containing a random choice.
    """
    if request.method != 'GET':
        return HttpResponseBadRequest()

    chosen = get_random_choice()
    response = {"id": chosen, "name": CHOICE_NAMES[chosen]}
    return JsonResponse(response)

def get_computer_choice(player=None):
    """
    Choose an action for the computer in a round of the game.

    @param player: The user object for the player. Currently unused.
    @return: An integer between 1 and 5 representing a gameplay choice.
    """
    if player is None:
        return get_random_choice()

def post_play(request):
    """
    Handler for API calls of the form GET /choice

    @param request: The request for this API call.
        player: the player's choice in this round of the game.
    @return: JSON response containing the results of the round.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest()

    parameters = json.loads(request.body.decode())
    if 'player' not in parameters:
        return HttpResponseBadRequest()

    try:
        player_choice = int(parameters['player'])
        assert player_choice in range(1, 6)
    except (ValueError, AssertionError):
        return HttpResponseBadRequest()

    if hasattr(request, 'user'):
        player = request.user
        if player.is_anonymous:
            player = None
    else:
        player = None

    computer_choice = get_computer_choice(player)

    g = Game.objects.create(player=player, player_choice=player_choice,
                            computer_choice=computer_choice)

    return JsonResponse(g.get_response())
