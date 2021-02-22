from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Q

from .models import Episode


def get_all_seasons_data():
    query_params = {
        'apikey': settings.OMDB_API_KEY,
        't': 'Game Of Thrones',
        'Season': 1
    }
    first_season_data = requests.get(settings.OMDB_API_URL, params=query_params).json()

    yield first_season_data

    total_seasons = int(first_season_data.get('totalSeasons'))
    for season_n in range(2, total_seasons + 1):
        query_params['Season'] = season_n

        yield requests.get(settings.OMDB_API_URL, params=query_params).json()


def upload_episodes_to_db():
    """Creates new Episodes and updates existing episodes in a bulk way. It is not suitable for large datasets."""
    seasons_data_generator = get_all_seasons_data()
    all_episodes_data_mapping = {}
    existing_episodes_filter_query = Q()

    for season_data in seasons_data_generator:
        season_number = int(season_data.get('Season'))

        for episode_data in season_data.get('Episodes'):
            episode_number = int(episode_data.get('Episode'))

            db_episode_data = {
                'title': episode_data.get('Title'),
                'released': datetime.strptime(episode_data.get('Released'), '%Y-%m-%d'),
                'episode_number': episode_number,
                'season_number': season_number,
                'imdb_rating': float(episode_data.get('imdbRating'))
            }
            if all_episodes_data_mapping.get(season_number):
                all_episodes_data_mapping[season_number][episode_number] = db_episode_data
            else:
                all_episodes_data_mapping[season_number] = {episode_number: db_episode_data}

            existing_episodes_filter_query |= Q(season_number=season_number, episode_number=episode_number)

    existing_episodes = Episode.objects.filter(existing_episodes_filter_query)

    fields_to_update = ['title', 'released', 'imdb_rating']
    for existing_episode in existing_episodes:
        # Pops data for update, so duplicate will not be created in next steps
        for_update_episode_data = all_episodes_data_mapping[existing_episode.season_number]\
            .pop(existing_episode.episode_number)

        for field_to_update in fields_to_update:
            setattr(existing_episode, field_to_update, for_update_episode_data[field_to_update])

    Episode.objects.bulk_update(existing_episodes, fields_to_update)

    for_bulk_create = []
    for _, season_data in all_episodes_data_mapping.items():
        for _, episode_data in season_data.items():
            for_bulk_create.append(Episode(**episode_data))

    Episode.objects.bulk_create(for_bulk_create)
