import requests
from django.core.management.base import BaseCommand
from ...models import Game
import datetime
from ....options import twitch_clientID, twitch_clientSecret

class Command(BaseCommand):
    help = 'Import games from IGDB'

    def handle(self, *args, **options):
        # Настройте параметры запроса к API IGDB
        
        clientID = twitch_clientID
        clientSecret = twitch_clientSecret
        
        pre_response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={clientID}&client_secret={clientSecret}&grant_type=client_credentials').json()
        access_token = pre_response['access_token']
        
        url = "https://api.igdb.com/v4/games"
        headers = {
            "Client-ID": clientID,
            "Authorization": f"Bearer {access_token}",
        }
        data = "fields name,summary,cover.url,first_release_date,genres; limit 500;"  # Измените параметры запроса по своему усмотрению

        # Отправьте запрос к API IGDB
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            games_data = response.json()
            for game_data in games_data:
                unix_timestamp = game_data.get("first_release_date")
                if unix_timestamp:
                    first_release_date = datetime.datetime.fromtimestamp(unix_timestamp).date()
                else:
                    first_release_date = None
                # Создайте или обновите запись в модели Game
                game, created = Game.objects.update_or_create(
                    igdb_id=game_data.get("id"),
                    defaults={
                        "name": game_data.get("name"),
                    }
                )
                if "summary" in game_data:
                    game.summary = game_data.get("summary")
                if "cover" in game_data:
                    if "url" in game_data[u'cover']:
                        game.cover = 'https://' + str(game_data.get("cover")[u"url"])[2:]
                game.first_release_date = first_release_date
                game.save()
                self.stdout.write(self.style.SUCCESS(f"Imported game: {game.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data from IGDB ({response.status_code})"))

