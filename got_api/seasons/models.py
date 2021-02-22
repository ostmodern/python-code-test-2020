from django.db import models

# Create your models here.


class Episode(models.Model):
    title = models.CharField(max_length=100)
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    released = models.DateField()
    imdb_rating = models.FloatField()

    def __str__(self):
        return f'{self.episode_number} - {self.title}'
