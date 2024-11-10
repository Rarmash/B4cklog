from rest_framework import serializers
from .models import Profile, Game
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    backlog_want_to_play = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())
    backlog_playing = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())
    backlog_played = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())
    backlog_completed = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())
    backlog_completed_100 = serializers.PrimaryKeyRelatedField(many=True, queryset=Game.objects.all())

    class Meta:
        model = Profile
        fields = [
            'user',
            'image',
            'backlog_want_to_play',
            'backlog_playing',
            'backlog_played',
            'backlog_completed',
            'backlog_completed_100'
        ]
