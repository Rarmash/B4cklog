from dotenv import load_dotenv
from os import environ

load_dotenv()

twitch_clientID = environ.get('twitch_clientID')
twitch_clientSecret = environ.get('twitch_clientSecret')