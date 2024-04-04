from django.db import models  # Импорт модуля models из библиотеки Django для работы с базой данных.
from django.contrib.auth.models import User  # Импорт модели пользователя Django для аутентификации.
from b4cklog.models import Game  # Импорт модели игры из приложения b4cklog.
from PIL import Image  # Импорт модуля Image из библиотеки Pillow для работы с изображениями.


# Модель профиля пользователя.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь "один к одному" с моделью User.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # Изображение профиля пользователя.
    # Игры, которые пользователь хочет поиграть.
    backlog_want_to_play = models.ManyToManyField(Game, related_name='backlog_want_to_play', blank=True)
    # Игры, которые пользователь в настоящее время играет.
    backlog_playing = models.ManyToManyField(Game, related_name='backlog_playing', blank=True)
    # Игры, которые пользователь уже играл.
    backlog_played = models.ManyToManyField(Game, related_name='backlog_played', blank=True)
    # Игры, которые пользователь завершил.
    backlog_completed = models.ManyToManyField(Game, related_name='backlog_completed', blank=True)
    # Игры, которые пользователь завершил на 100%.
    backlog_completed_100 = models.ManyToManyField(Game, related_name='backlog_completed_100', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'  # Возвращает строковое представление объекта - профиль пользователя.

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сохранение профиля пользователя.

        img = Image.open(self.image.path)  # Открытие изображения профиля.

        if img.height > 300 or img.width > 300:  # Если размер изображения больше 300x300.
            output_size = (300, 300)
            img.thumbnail(output_size)  # Создание превью изображения.
            img.save(self.image.path)  # Сохранение изменений.

    def get_backlog_by_category(self, category):
        if category == 'backlog_want_to_play':
            return self.backlog_want_to_play.all()  # Получение списка игр, которые пользователь хочет поиграть.
        elif category == 'backlog_playing':
            return self.backlog_playing.all()  # Получение списка игр, которые пользователь в настоящее время играет.
        elif category == 'backlog_played':
            return self.backlog_played.all()  # Получение списка игр, которые пользователь уже играл.
        elif category == 'backlog_completed':
            return self.backlog_completed.all()  # Получение списка игр, которые пользователь завершил.
        elif category == 'backlog_completed_100':
            return self.backlog_completed_100.all()  # Получение списка игр, которые пользователь завершил на 100%.
        else:
            return None  # Если указана некорректная категория, возвращается None.
