import logging

import requests

from app.settings import IMDB_API_KEY

log = logging.getLogger(__name__)

BASE_IMDB_URL = "http://www.omdbapi.com/"


class IMDBSeries:

    def __init__(self, series_title):
        self.series_title = series_title


    def get_series_data(self):
        try:
            response = requests.get(
                url=BASE_IMDB_URL,
                params={'t': self.series_title, 'apikey': IMDB_API_KEY}
            )
            return response.json()
        except requests.RequestException:
            log.error('Something wrong during to fetching series data.')

        return {}


    def get_season_data(self, season_id):
        try:
            response = requests.get(
                url=BASE_IMDB_URL,
                params={'i': self.series_title, 'apikey': IMDB_API_KEY, 'Season': season_id}
            )
            print('url', response.url)
            return response.json()
        except requests.RequestException:
            log.error('Something wrong during to fetching series data.')

        return {}


    def get_all_episodes(self):
        episodes_list = []
        series_data = self.get_series_data()
        total_seasons = int(series_data.get("totalSeasons"))

        for season_id in range(1, total_seasons + 1):
            season_data = self.get_season_data(season_id=season_id)
            for episode in season_data.get('Episodes', []):
                episode['Season'] = str(season_id)
                episodes_list.append(episode)

        return episodes_list
