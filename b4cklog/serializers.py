from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Platform, Game


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['platform_id', 'name', 'abbreviation']


class GameRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Показать имя пользователя в ответе
    game = serializers.StringRelatedField()  # Показать название игры в ответе


class GameSerializer(serializers.ModelSerializer):
    platforms = PlatformSerializer(many=True)  # Вложенный сериализатор для платформ
    # average_rating = serializers.FloatField()  # Поле для отображения среднего рейтинга

    class Meta:
        model = Game
        fields = ['igdb_id', 'name', 'summary', 'cover', 'first_release_date', 'platforms']
