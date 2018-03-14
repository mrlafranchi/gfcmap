# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail

import uuid
from time import sleep
import geocoder
import urllib3
urllib3.disable_warnings()

GENDER = (
    ('male', 'MALE'),
    ('female', 'FEMALE')
)

class Player(AbstractUser):
    avatar = models.CharField(max_length=100, default="default_avatar.png")
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default='male') 
    address = models.CharField(max_length=255, blank=True, null=True) 
    home_field = models.ForeignKey("Location", blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return self.email


FACILITY_TYPE = (
    ('indoor', 'Indoor'),
    ('outdoor', 'Outdoor')
)

FIELD_TYPE = (
    ('grass', 'Grass'),
    ('turf', 'Turf'),
    ('futsal', 'Futsal')
)

class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255) 
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE, default='outdoor') 
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE, default='grass') 
    url = models.CharField(max_length=120, null=True, blank=True) 
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    created_by = models.ForeignKey(Player, related_name="field_creator")
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        address = self.address.encode('utf-8')
        trial = 3

        while trial > 0:
            sleep(0.05)
            try:
                g = geocoder.google(address)
                latlon = g.geojson['features'][0]['geometry']['coordinates']
                self.lat = latlon[1]
                self.lng = latlon[0]
                break
            except (RuntimeError, ValueError, TypeError, Exception):
                trial = trial - 1

        super(Location, self).save()


class GameEvent(models.Model):
    location = models.ForeignKey(Location, related_name="events")
    datetime = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, null=True) 
    players = models.ManyToManyField(Player)
    created_by = models.ForeignKey(Player, related_name="game_creator")

    def __str__(self):
        return self.location.name


class GameInvitation(models.Model):
    game = models.ForeignKey(GameEvent)
    player = models.ForeignKey(Player)
    code = models.CharField(max_length=50)
    is_accepted = models.BooleanField(default=False)

    
def notify_players(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        send_mail(
            'Game Event Notification',
            'You are invited to the game ({}) at {} {}'.format(instance.description, instance.location, instance.datetime),
            'info@goodfoot.club',
            [ii.email for ii in Player.objects.filter(id__in=pk_set)],
            fail_silently=False,
        )

# m2m_changed.connect(notify_players, sender=GameEvent.players.through)
