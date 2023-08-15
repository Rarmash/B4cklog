from django.db import models
from django.contrib.auth.models import User
from b4cklog.models import Game
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    backlog_want_to_play = models.ManyToManyField(Game, related_name='backlog_want_to_play', blank=True)
    backlog_playing = models.ManyToManyField(Game, related_name='backlog_playing', blank=True)
    backlog_played = models.ManyToManyField(Game, related_name='backlog_played', blank=True)
    backlog_completed = models.ManyToManyField(Game, related_name='backlog_completed', blank=True)
    backlog_completed_100 = models.ManyToManyField(Game, related_name='backlog_completed_100', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def get_backlog_by_category(self, category):
        if category == 'backlog_want_to_play':
            return self.backlog_want_to_play.all()
        elif category == 'backlog_playing':
            return self.backlog_playing.all()
        elif category == 'backlog_played':
            return self.backlog_played.all()
        elif category == 'backlog_completed':
            return self.backlog_completed.all()
        elif category == 'backlog_completed_100':
            return self.backlog_completed_100.all()
        else:
            return None