import os
import requests

API_KEY = os.getenv('API_KEY')

ALL_SEASONS_URL = f"http://www.omdbapi.com/?t=Game%20of%20Thrones&apikey={API_KEY}"
EP_URL = f"http://www.omdbapi.com/?i=<episode title id>&apikey={API_KEY}"

all_seasons_json = requests.get(ALL_SEASONS_URL).json()
seasons_qty = int(all_seasons_json["totalSeasons"])


def get_episodes():
    def get_season(season_num):
        season_url = f"http://www.omdbapi.com/?t=Game of Thrones&Season={season_num}&apikey={API_KEY}"
        season_json = requests.get(season_url).json()
        return season_json

    seasons = []
    for season_num in range(seasons_qty+1):
        episodes = [dict(ep, **{"Season": season_num}) for ep in get_season(season_num)]
        seasons.append(episodes)

    return episodes
