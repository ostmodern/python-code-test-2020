from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from seasons.models import Episode


class EpisodeViewSetTest(APITestCase):
    def test_filter_episodes(self):
        good_imdb_episode_season_1 = Episode.objects.create(**{
            'episode_number': 1,
            'season_number': 1,
            'title': 'Episode1',
            'released': datetime.now().date(),
            'imdb_rating': float(8.0),
        })

        bad_imdb_episode_season_1 = Episode.objects.create(**{
            'episode_number': 2,
            'season_number': 1,
            'title': 'Episode2',
            'released': datetime.now().date(),
            'imdb_rating': float(4.0),
        })

        good_imdb_episode_season_2 = Episode.objects.create(**{
            'episode_number': 1,
            'season_number': 2,
            'title': 'Episode1',
            'released': datetime.now().date(),
            'imdb_rating': float(8.0),
        })

        bad_imdb_episode_season_2 = Episode.objects.create(**{
            'episode_number': 2,
            'season_number': 2,
            'title': 'Episode2',
            'released': datetime.now().date(),
            'imdb_rating': float(4.0),
        })

        # For first season
        response_data = self.client.get(
            reverse('episodes-filter-episodes'), {'gt_imdb_rating': 7.9, 'season': 1}
        ).json()

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], good_imdb_episode_season_1.id)

        # For all seasons
        response_data = self.client.get(
            reverse('episodes-filter-episodes'), {'gt_imdb_rating': 7.9}
        ).json()

        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['id'], good_imdb_episode_season_1.id)
        self.assertEqual(response_data[1]['id'], good_imdb_episode_season_2.id)
