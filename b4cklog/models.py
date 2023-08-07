from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateTimeField(default=timezone.now)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name