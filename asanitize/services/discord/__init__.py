import requests

session = requests.Session()
base_url = 'https://discord.com/api/v9'

def build_url(*paths) -> str:
    return '/'.join([base_url, *paths])