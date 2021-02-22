from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from comments.models import Comment
from seasons.models import Episode


class CommentViewSetTest(APITestCase):
    def test_retrieve_episode_comments(self):
        first_episode_data = {
            'episode_number': 1,
            'season_number': 1,
            'title': 'Episode1',
            'released': datetime.now().date(),
            'imdb_rating': float(9.0),
        }
        first_episode = Episode.objects.create(**first_episode_data)

        second_episode_data = {
            'episode_number': 2,
            'season_number': 1,
            'title': 'Episode2',
            'released': datetime.now().date(),
            'imdb_rating': float(9.0),
        }
        second_episode = Episode.objects.create(**second_episode_data)

        first_episode_comment_data = {'comment_text': '1234', 'episode_id': first_episode.id}
        first_episode_comment = Comment.objects.create(**first_episode_comment_data)

        second_episode_comment_data = {'comment_text': '4567', 'episode_id': second_episode.id}
        second_episode_comment = Comment.objects.create(**second_episode_comment_data)

        response_data = self.client.get(
            reverse('comments-episode-comments'), {'episode_id': first_episode.id}
        ).json()

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], first_episode_comment.id)

        response_data = self.client.get(
            reverse('comments-episode-comments'), {'episode_id': second_episode.id}
        ).json()

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], second_episode_comment.id)
