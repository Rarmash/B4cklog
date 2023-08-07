from django.db import models
from PIL import Image
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)  # Уникальный ID игры из IGDB
    name = models.CharField(max_length=200)
    summary = models.TextField()
    cover = models.URLField(default='https://icon-library.com/images/steam-question-mark-icon/steam-question-mark-icon-29.jpg')
    first_release_date = models.DateField(null=True)

    def __str__(self):
        return self.name