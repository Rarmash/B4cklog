import requests
from django.core.management.base import BaseCommand
from ...models import Game, Platform
import datetime
from options import twitch_clientID, twitch_clientSecret


class Command(BaseCommand):
    help = 'Import games from IGDB'

    def add_arguments(self, parser):
        parser.add_argument('search_query', type=str, help='The search query for the game')

    def handle(self, *args, **options):
        search_query = options['search_query']

        clientID = twitch_clientID
        clientSecret = twitch_clientSecret

        pre_response = requests.post(
            f'https://id.twitch.tv/oauth2/token?client_id={clientID}&client_secret={clientSecret}&grant_type=client_credentials').json()
        access_token = pre_response['access_token']

        url = "https://api.igdb.com/v4/games"
        headers = {
            "Client-ID": clientID,
            "Authorization": f"Bearer {access_token}",
        }
        print(access_token)
        data = f'search "{search_query}"; fields name,summary,cover.url,first_release_date,genres,platforms; limit 500;'  # Измените параметры запроса по своему усмотрению

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
                        game.cover = str('https://' + str(game_data.get("cover")[u"url"])[2:]).replace("t_thumb",
                                                                                                       "t_cover_big")
                game.first_release_date = first_release_date
                platforms_data = game_data.get("platforms")
                if platforms_data:
                    for platform_id in platforms_data:
                        try:
                            platform = Platform.objects.get(platform_id=platform_id)
                        except Platform.DoesNotExist:
                            platform_url = f"https://api.igdb.com/v4/platforms"
                            platform_response = requests.post(platform_url, headers=headers,
                                                              data=f"fields *; where id = {platform_id};").json()[0]
                            platform, created = Platform.objects.get_or_create(
                                platform_id=platform_id,
                                defaults={'name': platform_response.get('name')}
                            )
                            if 'abbreviation' in platform_response:
                                platform.abbreviation = platform_response.get('abbreviation')
                            else:
                                platform.abbreviation = platform_response.get('name')
                            platform.save()

                        game.platforms.add(platform)
                game.save()
                self.stdout.write(self.style.SUCCESS(f"Imported game: {game.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data from IGDB ({response.status_code})"))
