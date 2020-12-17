from django.contrib.auth import get_user_model
from django.db import models


class Episode(models.Model):
    """
    Model used for saving Game of Thrones episodes
    """
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    season = models.PositiveIntegerField()
    release_date = models.DateField()
    imdb_rating = models.FloatField()

    def __str__(self) -> str:
        return f'{self.title}, season {self.season}'


class Comment(models.Model):
    """
    Model used for saving comments for the episodes
    """
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    added = models.DateTimeField(auto_now=True)
