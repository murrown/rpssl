from django.urls import re_path
from game.views import get_choices, get_choice, post_play

urlpatterns = [
    re_path(r'^choices/?$', get_choices),
    re_path(r'^choice/?$', get_choice),
    re_path(r'^play/?$', post_play),
]
