# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from general.models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'facility_type', 'field_type', 'lat', 'lng', 'url', 'created_by', 'created_at')
    search_fields = ['name', 'address']


class GameInvitationAdmin(admin.ModelAdmin):
    list_display = ('game', 'player', 'code', 'is_accepted')
    search_fields = ['game', 'player', 'code']


class GameEventAdmin(admin.ModelAdmin):
    list_display = ('location', 'datetime', 'created_by', 'description')


admin.site.register(Location, LocationAdmin)
admin.site.register(Player)
admin.site.register(GameEvent, GameEventAdmin)
admin.site.register(GameInvitation, GameInvitationAdmin)
