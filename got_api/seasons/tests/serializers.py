from datetime import datetime

from django.test import TestCase

from seasons.models import Episode
from seasons.serializers import EpisodeSerializer


class EpisodeSerializerTest(TestCase):
    def test_serializer_data(self):
        episode_data = {
            'episode_number': 2,
            'season_number': 1,
            'title': 'Episode1',
            'released': datetime.now().date(),
            'imdb_rating': float(9.0),
        }
        episode = Episode.objects.create(**episode_data)
        serialized_data = EpisodeSerializer(episode).data

        self.assertEqual(serialized_data['episode_number'], episode_data['episode_number'])
        self.assertEqual(serialized_data['season_number'], episode_data['season_number'])
        self.assertEqual(serialized_data['released'], str(episode_data['released']))
        self.assertEqual(serialized_data['imdb_rating'], episode_data['imdb_rating'])

