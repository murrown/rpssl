from django.conf.urls import include, url
from django.urls import re_path
from django.contrib.auth import views as auth_views
from game.views import get_choices, get_choice, post_play, register, index

urlpatterns = [
    re_path(r'^choices/?$', get_choices),
    re_path(r'^choice/?$', get_choice),
    re_path(r'^play/?$', post_play),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.logout_then_login,
            {"login_url": "/login/"}, name='logout'),
    re_path(r'^register/$', register, name='register'),
    re_path(r'^$', index),
]
