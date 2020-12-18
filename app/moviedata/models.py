from datetime import datetime

from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=1024)
    total_seasons = models.PositiveIntegerField()
    rating = models.FloatField()
    imdbId = models.CharField(max_length=256)
    released = models.DateTimeField()

    @staticmethod
    def handle_omdb_data(data):
        return Movie(title=data['title'],
                     total_seasons=int(data['total_seasons']),
                     rating=data['imdb_rating'],
                     imdbId=data['imdb_id'],
                     released=datetime.strptime(data['released'], '%d %b %Y'))


class Episode(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    released = models.DateTimeField()
    rating = models.FloatField()
    imdbId = models.CharField(max_length=256)
    season = models.PositiveIntegerField()
    episode = models.PositiveIntegerField()

    @staticmethod
    def handle_omdb_data(movie, season_data):
        episodes = []
        for episode in season_data['episodes']:
            season = episode.get('season') or season_data['season']
            try:
                release_date = datetime.strptime(episode['released'], '%Y-%m-%d')
            except:
                release_date = datetime.strptime(episode['released'], '%d %b %Y')
            info = {
                'movie': movie,
                'title': episode['title'],
                'released': release_date,
                'rating': episode['imdb_rating'],
                'imdbId': episode['imdb_id'],
                'season': season,
                'episode': int(episode['episode'])
            }
            episodes.append(Episode(**info))
        return episodes


class Comment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    text = models.TextField()
