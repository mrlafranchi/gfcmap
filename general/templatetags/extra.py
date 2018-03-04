import json
import datetime

from django import template
from django.db.models import Avg

from general.models import *

register = template.Library()

@register.filter
def is_accepted(player, game):
    try:
        return GameInvitation.objects.filter(player=player, game=game)[0].is_accepted
    except Exception as e:
        return False

@register.filter
def player_count(game):
    return GameInvitation.objects.filter(game=game, is_accepted=True).count()

@register.filter
def game_count(location):
    return location.events.filter(datetime__gte=datetime.datetime.now()).count()
