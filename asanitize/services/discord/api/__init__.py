import requests

session = requests.Session()
base_url = 'https://discordapp.com/api'

def build_url(self, *paths: list) -> str:
    return '/'.join([base_url, *paths])