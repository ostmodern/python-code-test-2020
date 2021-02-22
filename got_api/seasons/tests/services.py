from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

from django.test import SimpleTestCase, TestCase

from seasons.models import Episode
from seasons.services import get_all_seasons_data, upload_episodes_to_db


class GetAllSeasonDataTest(SimpleTestCase):
    @mock.patch('seasons.services.requests.get')
    def test_response_data_generator(self, m_get):
        response_mock = MagicMock()
        response_mock.json.return_value = mocked_response_data = {
            'Season': '1',
            'totalSeasons': '2'
        }
        m_get.return_value = response_mock
        generator = get_all_seasons_data()

        # first_season response
        response = generator.__next__()
        self.assertDictEqual(response, mocked_response_data)

        # second season response
        response = generator.__next__()
        self.assertDictEqual(response, mocked_response_data)

        self.assertRaises(StopIteration, generator.__next__)


class UploadEpisodesToDbTest(TestCase):
    def setUp(self):
        self.expected_response = [
            {
                'Season': 1,
                'Episodes': [
                    {
                        'Title': 'Episode1',
                        'Released': '2020-01-20',
                        'Episode': '1',
                        'imdbRating': '5.6',
                    },
                    {
                        'Title': 'Episode2',
                        'Released': '2020-02-20',
                        'Episode': '2',
                        'imdbRating': '7.6',
                    },
                ]
            },
            {
                'Season': 2,
                'Episodes': [
                    {
                        'Title': 'Episode21',
                        'Released': '2020-03-20',
                        'Episode': '1',
                        'imdbRating': '9.7',
                    },
                    {
                        'Title': 'Episode22',
                        'Released': '2020-04-20',
                        'Episode': '2',
                        'imdbRating': '6.5',
                    },
                ]
            },
        ]
        get_all_seasons_data_patcher = mock.patch('seasons.services.get_all_seasons_data')
        response_mock = get_all_seasons_data_patcher.start()
        response_mock.return_value = self.expected_response

        self.addCleanup(mock.patch.stopall)

    def check_episode_data(self, episode_response_data: dict, episode_obj: Episode):
        self.assertEqual(episode_obj.title, episode_response_data['Title'])
        self.assertEqual(episode_obj.released, datetime.strptime(episode_response_data['Released'], '%Y-%m-%d').date())
        self.assertEqual(episode_obj.imdb_rating, float(episode_response_data['imdbRating']))

    def test_creates_new_and_updates_existing_episode_object(self):
        existing_first_season_second_episode = Episode.objects.create(**{
            'episode_number': 2,
            'season_number': 1,
            'title': 'OldEpisode_s1_e2',
            'released': datetime.now().date(),
            'imdb_rating': float(9.0),
        })

        upload_episodes_to_db()
        self.assertEqual(Episode.objects.count(), 4)

        # First season
        first_episode = Episode.objects.get(episode_number=1, season_number=1)
        first_episode_data = self.expected_response[0]['Episodes'][0]
        self.check_episode_data(first_episode_data, first_episode)

        second_episode = Episode.objects.get(pk=existing_first_season_second_episode.pk)
        second_episode_data = self.expected_response[0]['Episodes'][1]
        self.check_episode_data(second_episode_data, second_episode)

        # Second season
        first_episode = Episode.objects.get(episode_number=1, season_number=2)
        first_episode_data = self.expected_response[1]['Episodes'][0]
        self.check_episode_data(first_episode_data, first_episode)

        second_episode = Episode.objects.get(episode_number=2, season_number=2)
        second_episode_data = self.expected_response[1]['Episodes'][1]
        self.check_episode_data(second_episode_data, second_episode)
