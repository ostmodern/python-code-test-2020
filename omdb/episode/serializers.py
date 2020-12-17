from django.db import models
from rest_framework import serializers

from .models import Episode, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'text', 'added')
        read_only_fields = ('user',)
        


class EpisodeSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['episode_number', 'title', 'season', 'release_date', 'imdb_rating', 'comment_set']
