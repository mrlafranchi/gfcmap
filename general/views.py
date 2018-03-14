# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework import viewsets

from general.models import *
from general.serializers import *

from rest_framework.decorators import detail_route
from rest_framework.response import Response

def index(request):
    locations = Location.objects.all().order_by('name')
    center = '38.60909, -121.3768'

    if request.user.is_authenticated() and request.user.home_field:
        if request.user.home_field.lat and request.user.home_field.lng:
            center = '{}, {}'.format(request.user.home_field.lat, request.user.home_field.lng)

    return render(request, 'index.html', {
        'players': Player.objects.all(),
        'locations': locations,
        'center': center
    })

@login_required(login_url='/')
def profile(request):
    games = GameEvent.objects.filter(datetime__gte=datetime.datetime.now(), players__in=[request.user]).order_by('datetime')
    locations = Location.objects.all().order_by('name')

    return render(request, 'profile.html', {
        'games': games,
        'locations': locations
    })

def location(request, id):
    location = Location.objects.get(id=id)
    games = location.events.filter(datetime__gte=datetime.datetime.now()) \
                           .order_by('datetime')
    return render(request, 'location.html', {
        'games': games,
        'location': location,
        'players': Player.objects.all(),
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
