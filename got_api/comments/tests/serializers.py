from datetime import datetime

from django.test import TestCase

from comments.models import Comment
from comments.serializers import CommentSerializer
from seasons.models import Episode


class CommentSerializerTest(TestCase):
    def test_serializer_data(self):
        episode_data = {
            'episode_number': 2,
            'season_number': 1,
            'title': 'Episode1',
            'released': datetime.now().date(),
            'imdb_rating': float(9.0),
        }
        episode = Episode.objects.create(**episode_data)

        comment_data = {
            'episode': episode,
            'comment_text': 'Some text',
        }
        episode = Comment.objects.create(**comment_data)
        serialized_data = CommentSerializer(episode).data

        self.assertEqual(serialized_data['episode'], episode.id)
        self.assertEqual(serialized_data['comment_text'], 'Some text')