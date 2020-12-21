import json

from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()
api_movie = '/api/v0/movie/'
api_episode = '/api/v0/episode/'
api_comment = '/api/v0/comment/'


from moviedata.models import Movie, Episode, Comment


class MovieEpisodeCommentTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin',
                                              email='admin@some.random.domainfffm',
                                              password='random pass for person!!!')
        for user in ('user1', 'user2', 'user3'):
            u = User.objects.create_user(username=user,
                                         email=f'{user}@some.random.domainfffm',
                                         password='random pass for person!')

        self.movie = Movie.objects.create(title='Movie', total_seasons=5,
                                          rating=9.5, imdbId='ttMovieId',
                                          released=datetime.now())
        self.movie2 = self.movie = Movie.objects.create(title='Movie2', total_seasons=5,
                                                        rating=8.5, imdbId='ttMovie2Id',
                                                        released=datetime.now())

        self.episode = Episode.objects.create(movie=self.movie, title='Episode',
                                              released=datetime.now(), rating=9.5,
                                              imdbId='ttEpisodeID', episode=1, season=1)

        self.episode2 = Episode.objects.create(movie=self.movie2, title='Episode Movie2',
                                               released=datetime.now(), rating=7.5,
                                               imdbId='ttEpisodeMovie2ID', episode=1, season=1)

        self.comment = Comment.objects.create(owner=self.admin, episode=self.episode,
                                              text='My comment')

    def test_create_movie(self):
        title = 'Movie3'
        data = {'title': title, 'total_seasons': 3,
                'rating': 7, 'imdbId': 'movie3', 'released': datetime.now()}
        res = self.client.post(api_movie, data)
        self.assertEqual(res.status_code, 201)
        movie = Movie.objects.get(title=title)
        self.assertEqual(movie.total_seasons, data['total_seasons'])
        self.assertEqual(movie.rating, data['rating'])
        self.assertEqual(movie.imdbId, data['imdbId'])

    def test_filter_movie(self):
        title = self.movie.title
        rating7 = 7
        rating9 = 9
        res = self.client.get(f'{api_movie}?title={title}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 1)
        res = self.client.get(f'{api_movie}?rating__gte={rating7}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 2)
        res = self.client.get(f'{api_movie}?rating__gte={rating9}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 1)

    def test_update_movie(self):
        title = 'New title'
        old_title = self.movie.title
        data = {'title': title}
        res = self.client.patch(f'{api_movie}{self.movie.pk}/', json.dumps(data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.movie.refresh_from_db()
        self.assertFalse(Movie.objects.filter(title=old_title).exists())
        self.assertTrue(Movie.objects.filter(title=title).exists())

    def test_delete_movie(self):
        res = self.client.delete(f'{api_movie}{self.movie.pk}/')
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_create_episode(self):
        title = 'Episode2'
        data = {'movie': self.movie.pk, 'title': title,
                'rating': 7, 'imdbId': 'movie3', 'released': datetime.now(),
                'season': 1, 'episode': 2}
        res = self.client.post(api_episode, data)
        self.assertEqual(res.status_code, 201)
        episode = Episode.objects.get(title=title)
        self.assertEqual(episode.episode, data['episode'])
        self.assertEqual(episode.rating, data['rating'])
        self.assertEqual(episode.imdbId, data['imdbId'])

    def test_filter_episode(self):
        title = self.episode.title
        rating7 = 7
        rating9 = 9
        res = self.client.get(f'{api_episode}?title={title}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 1)
        res = self.client.get(f'{api_episode}?rating__gte={rating7}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 2)
        res = self.client.get(f'{api_episode}?rating__gte={rating9}')
        response = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(response), 1)

    def test_update_episode(self):
        title = 'New title'
        old_title = self.episode.title
        data = {'title': title}
        res = self.client.patch(f'{api_episode}{self.episode.pk}/', json.dumps(data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Episode.objects.filter(title=old_title).exists())
        self.assertTrue(Episode.objects.filter(title=title).exists())

    def test_delete_episode(self):
        res = self.client.delete(f'{api_episode}{self.episode.pk}/')
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Episode.objects.filter(pk=self.episode.pk).exists())

    def test_create_comment(self):
        data = {'owner': self.admin.pk, 'episode': self.episode.pk,
                'text': 'Comment'}
        res = self.client.post(api_comment, data)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(api_comment)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.content)), 2)
        comment = Comment.objects.filter(owner=self.admin)
        comment = comment.exclude(pk=self.comment.pk).first()
        self.assertEqual(comment.text, data['text'])

    def test_filter_comment(self):
        text = 'random text'
        res = self.client.get(f'{api_comment}?text={text}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.content)), 0)

        res = self.client.get(f'{api_comment}?text={self.comment.text}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.content)), 1)

        res = self.client.get(f'{api_comment}?owner={self.comment.owner.username}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.content)), 1)

    def test_update_comment(self):
        text = 'New text'
        old_text = self.comment.text
        data = {'text': text}
        res = self.client.patch(f'{api_comment}{self.comment.pk}/', json.dumps(data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Comment.objects.filter(text=old_text).exists())
        self.assertTrue(Comment.objects.filter(text=text).exists())

    def test_delete_comment(self):
        res = self.client.delete(f'{api_comment}{self.comment.pk}/')
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
