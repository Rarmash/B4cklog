from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


class Platform(models.Model):
    platform_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    cover = models.URLField(blank=True)
    first_release_date = models.DateField(null=True)
    platforms = models.ManyToManyField(Platform)
    ratings = models.ManyToManyField(User, through='GameRating', related_name='rated_games')

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum([rating.rating for rating in ratings]) / len(ratings)
        else:
            return None

    def __str__(self):
        return self.name


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f'{self.user.username}\'s rating for {self.game.name}: {self.rating}'
