from django.db import models
from django.contrib.auth.models import User


# Модель платформы, на которой доступны игры.
class Platform(models.Model):
    platform_id = models.IntegerField(unique=True)  # Уникальный идентификатор платформы.
    name = models.CharField(max_length=100)  # Название платформы
    abbreviation = models.CharField(max_length=100, blank=True)  # Аббревиатура платформы (необязательно).

    def __str__(self):
        return self.name  # Возвращает строковое представление объекта - название платформы.


# Модель игры.
class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)  # Уникальный идентификатор игры в базе данных IGDB.
    name = models.CharField(max_length=200)  # Краткое описание игры.
    summary = models.TextField()  # Ссылка на обложку игры (необязательно).
    cover = models.URLField(blank=True)  # Дата первого релиза игры (может быть пустой).
    first_release_date = models.DateField(null=True)  # Дата первого релиза игры (может быть пустой).
    platforms = models.ManyToManyField(Platform)  # Связь многие-ко-многим с моделью Platform.
    ratings = models.ManyToManyField(User, through='GameRating',
                                     related_name='rated_games')  # Оценки пользователей для игры.

    @property
    def average_rating(self):
        ratings = self.ratings.all()  # Получение всех оценок для данной игры.
        if ratings:  # Если есть оценки.
            return sum([rating.rating for rating in ratings]) / len(ratings)  # Возвращаем среднюю оценку.
        else:
            return None

    def __str__(self):
        return self.name  # Возвращает строковое представление объекта - название игры.


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, оценивший игру.
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Игра, которую пользователь оценил.
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Оценка игры от 1 до 10.

    class Meta:
        unique_together = ('user', 'game')  # Уникальность комбинации пользователя и игры.

    def __str__(self):
        # Возвращает строковое представление объекта - оценка игры пользователем.
        return f'{self.user.username}\'s rating for {self.game.name}: {self.rating}'
