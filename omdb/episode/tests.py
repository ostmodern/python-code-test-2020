from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Episode


class EpisodesTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(1, 3):
            Episode.objects.create(
                episode_number=i,
                title=f'Title {i}',
                season=i,
                release_date=timezone.now().date(),
                imdb_rating=7+i
            ).save()

    def test_get_episodes_list(self) -> None:
        episodes_list_url = reverse('episodes-list')
        response = self.client.get(episodes_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Unexpected status code')
        self.assertEqual(response.get('content-type'), 'application/json', 'Unexpected response type')
        episodes = response.json()
        self.assertEqual(type(episodes), list, 'Response should be a list')
        self.assertNotEqual(len(episodes), 0, 'Response should not be empty')
    
    def test_episode_retrieve(self) -> None:
        episode_retrieve_url = reverse('episode-retrieve', kwargs={'pk':1})
        response = self.client.get(episode_retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Unexpected status code')
        self.assertEqual(response.get('content-type'), 'application/json', 'Unexpected response type')
        episode = response.json()
        self.assertEqual(type(episode), dict, 'Response should be a dict')
        self.assertEqual(episode.get('episode_number'), 1, 'Episode number should be 1')
    
    def test_impossible_episode_retrieve(self) -> None:
        episode_retrieve_url = reverse('episode-retrieve', kwargs={'pk':10000000})
        response = self.client.get(episode_retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'Unexpected status code')
        self.assertEqual(response.get('content-type'), 'application/json', 'Unexpected response type')
        data = response.json()
        self.assertEqual(type(data), dict, 'Response should be a dict')
        self.assertEqual(data.get('detail'), 'Not found.', 'Error message is not as expected')
    