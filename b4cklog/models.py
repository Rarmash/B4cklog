from django.db import models
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    cover = models.URLField(blank=True)  # Убрали default значение
    first_release_date = models.DateField(null=True)

    def __str__(self):  # Исправлена ошибка в методе str
        return self.name