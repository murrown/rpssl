import json
from requests import get
from random import randint
from time import sleep
from collections import Counter

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import (
        HttpResponse, HttpResponseRedirect,
        JsonResponse, HttpResponseBadRequest)
from django.shortcuts import render
from django.template import loader
from game.models import CHOICE_NAMES, VICTORY_MAP, Game


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

def get_random_number():
    """
    Generate a random number between 1 and 100. Retrieves from an external API
    if configured to do so.

    @return: A random integer between 1 and 100.
    """
    if settings.USE_RNG_API:
        for _ in range(NUM_TIMEOUT_RETRIES):
            response = get(RNG_URI).json()
            try:
                value = response['random_number']
            except KeyError:
                sleep(1)
                continue
            return value
    return randint(1, 100)

def get_random_choice():
    """
    Generate a random number that is a valid choice for an action in the game.

    @return: An integer between 1 and 5 representing a gameplay choice.
    """
    return (get_random_number() % 5) + 1

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
    Plays intelligently using past knowledge.

    @param player: The user object for the player. Currently unused.
    @return: An integer between 1 and 5 representing a gameplay choice.
    """
    games = Game.objects.filter(player=player).order_by("-created")
    recent = [g.player_choice for g in games[:3]]
    while len(recent) < 3:
        recent.append(0)
    history1, history2, history3 = recent
    games = Game.objects.filter(
        player=player, history1=history1, history2=history2, history3=history3)
    if games.count() == 0:
        games = Game.objects.filter(
            history1=history1, history2=history2, history3=history3)
        if games.count() == 0:
            return get_random_choice()

    next_choices = Counter([g.player_choice for g in games])
    win_ratio = {}
    for computer_choice in sorted(VICTORY_MAP):
        wins, losses = 1, 1
        for player_choice in sorted(next_choices):
            if player_choice in VICTORY_MAP[computer_choice]:
                wins += next_choices[player_choice]
            elif computer_choice in VICTORY_MAP[player_choice]:
                losses += next_choices[player_choice]
        win_ratio[computer_choice] = wins / float(wins + losses)

    highest = max(win_ratio.values())
    options = sorted([c for c in win_ratio if win_ratio[c] == highest])
    if len(options) > 1:
        chosen = options[get_random_number() % len(options)]
    else:
        chosen = options[0]

    return chosen

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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST["username"],
                                    password=request.POST["password1"])
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    template = loader.get_template('registration/register.html')
    return HttpResponse(template.render({'form': form}, request))

def index(request):
    context = {}
    return render(request, "index.html", context=context)

def scoreboard(request):
    games = [g.get_record() for g in Game.objects.order_by("-created")[:10]]
    for i, g in enumerate(games):
        g['index'] = i
    return render(request, "scoreboard.html", context={'games': games})
