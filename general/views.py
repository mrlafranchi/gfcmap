# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from math import sin, cos, sqrt, atan2, radians

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets

from general.models import *
from general.serializers import *

from rest_framework.decorators import detail_route
from rest_framework.response import Response

def index(request):
    if request.method == 'POST':
        center = request.POST.get('center')
        zoom = request.POST.get('zoom')
    else:
        center = '38.60909, -121.3768'
        zoom = 11
        if request.user.is_authenticated() and request.user.home_field:
            center = '{}, {}'.format(request.user.home_field.lat, request.user.home_field.lng)
            
    players = []
    if request.user.is_authenticated() and request.user.home_field:
        players = get_players_in_range(Player.objects.all(), request.user.home_field)

    locations = []
    for loc in Location.objects.all().order_by('name'):
        if calc_distance(float(center.split(', ')[0]), float(center.split(', ')[1]), loc.lat, loc.lng) < settings.RANGE_RADIUS:
            locations.append(loc)        

    return render(request, 'index.html', {
        'players': players,
        'locations': locations,
        'center': center,
        'zoom': zoom
    })

@login_required(login_url='/')
def profile(request):
    games = GameEvent.objects.filter(datetime__gte=datetime.datetime.now(), players__in=[request.user]).order_by('datetime')
    locations = Location.objects.all().order_by('name')

    players = []
    if request.user.home_field:
        players = get_players_in_range(Player.objects.all(), request.user.home_field)

    return render(request, 'profile.html', {
        'games': games,
        'players': players,
        'num_players': Player.objects.all().count(),
        'locations': locations
    })

def location(request, id):
    location = Location.objects.get(id=id)
    games = location.events.filter(datetime__gte=datetime.datetime.now()) \
                           .order_by('datetime')

    players = get_players_in_range(Player.objects.all(), location)

    return render(request, 'location.html', {
        'games': games,
        'location': location,
        'players': players,
    })

def game(request, id):
    game = GameEvent.objects.get(id=id)

    return render(request, 'game.html', {
        'game': game,
        'players': Player.objects.all(),
    })

def accept_invitation(request, code):    
    try:
        gi = GameInvitation.objects.get(code=code)
        gi.is_accepted = True
        gi.save()
        next = '/game/{}'.format(gi.game.id)
    except Exception as e:
        next = '/'

    return redirect(next)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GameEventViewSet(viewsets.ModelViewSet):
    queryset = GameEvent.objects.all()
    serializer_class = GameEventSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    @detail_route(methods=['POST'])
    def join_game(self, request, *args, **kwargs):
        game = self.get_object()
        game.players.add(request.user)
        game.save()
        GameInvitation.objects.create(game=game, player=request.user, is_accepted=True, code="***")
        return Response(status=200)

    @detail_route(methods=['POST'])
    def leave_game(self, request, *args, **kwargs):
        game = self.get_object()
        game.players.remove(request.user)
        game.save()
        GameInvitation.objects.filter(game=game, player=request.user).delete()
        return Response(status=200)


@csrf_exempt
def upload_image(request):
    myfile = request.FILES['images']
    _type = request.POST.get('type', '')
    if _type:
        _type = _type + '/' 

    fs = FileSystemStorage()
    filename = fs.save(_type+myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    res = {"image_url": uploaded_file_url,"image_name": uploaded_file_url.split('/')[-1]}
    return JsonResponse(res, safe=False)


def calc_distance(lat1, lon1, lat2, lon2):
    if lat1 and lon1 and lat2 and lon2:
        radius = 6371  # km

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (sin(dlat / 2) * sin(dlat / 2) +
             cos(radians(lat1)) * cos(radians(lat2)) *
             sin(dlon / 2) * sin(dlon / 2))
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = radius * c
        return d
    return settings.RANGE_RADIUS * 10


def get_players_in_range(players, loc):
    players_ = []
    for player in players:
        if player.home_field:
            if calc_distance(loc.lat, loc.lng, player.home_field.lat, player.home_field.lng) < settings.RANGE_RADIUS:
                players_.append(player)
    return players_
