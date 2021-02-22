from django.db import models


class Comment(models.Model):
    episode = models.ForeignKey('seasons.Episode', related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.episode.name}: {self.comment_text[:10]}...'
