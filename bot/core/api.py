import requests

from .files import Data

BASE_URL = "https://discord.com/api"

def avatar(user_id):
	apiData = requests.get(BASE_URL + f"/users/{user_id}", headers = {
		"Authorization": "Bot " + Data("config").yaml_read()['token']
	}).json()
	return f"https://cdn.discordapp.com/avatars/{apiData['id']}/{apiData['avatar']}.png?size=1024"