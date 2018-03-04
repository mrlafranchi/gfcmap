from rest_framework import serializers
from django.core.mail import send_mail

from .models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')
        read_only_fields = ('created_at',)


class GameEventSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(input_formats=["%Y-%m-%dT%I:%M %p"])

    def create(self, validated_data):
        game = super(GameEventSerializer, self).create(validated_data)
        for player in game.players.all():
            accepted = True if player == self.context['request'].user else False
            code = uuid.uuid4().hex
            GameInvitation.objects.create(game=game, 
                                          player=player,
                                          code=code,
                                          is_accepted=accepted)
            if not accepted:
                send_mail(
                    'Game Event Notification',
                    'You are invited to a <a href="http://18.222.154.104/game/{}">game</a> at {} {}. Please accept it <a href="http://18.222.154.104/accept_invitation/{}">here</a>.'.format(game.id, game.location, game.datetime, code),
                    'info@goodfoot.club',
                    [player.email],
                    fail_silently=False,
                )
        return game

    class Meta:
        model = GameEvent
        fields = ('__all__')


class UserDetailsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True) 

    class Meta:
        model = Player
        exclude = ('password', 'groups', 'user_permissions')
        read_only_fields = ('username', 'last_login', 'is_superuser', 'date_joined', 'created_at', 
                            'is_active', 'is_staff', 'address')

    # create