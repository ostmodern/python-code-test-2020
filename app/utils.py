import logging
import os
import requests

API_KEY = os.getenv('API_KEY')

ALL_SEASONS_URL = f"http://www.omdbapi.com/?t=Game%20of%20Thrones&apikey={API_KEY}"
EP_URL = f"http://www.omdbapi.com/?i=<episode title id>&apikey={API_KEY}"

all_seasons_json = requests.get(ALL_SEASONS_URL).json()
seasons_qty = int(all_seasons_json["totalSeasons"])


def get_episodes():
    episodes = []
    seasons = []
    for season_num in range(seasons_qty):
        season_url = f'http://www.omdbapi.com/?t=Game of Thrones&Season={season_num+1}&apikey={API_KEY}'
        season_json = requests.get(season_url).json()
        seasons.append(season_json)

    for season in seasons:
        logging.info(season)
        season_num = season['Season']
        for ep in season['Episodes']:
            ep['Season'] = season_num

        episodes.extend(season['Episodes'])

    return episodes
