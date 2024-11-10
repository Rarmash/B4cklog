from dotenv import load_dotenv
from os import environ

load_dotenv()

twitch_clientID = environ.get('twitch_clientID')
twitch_clientSecret = environ.get('twitch_clientSecret')
mysql_user = environ.get('mysql_user')
mysql_password = environ.get('mysql_password')
mysql_host = environ.get('mysql_host')
