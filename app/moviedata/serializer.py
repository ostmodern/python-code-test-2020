from rest_framework import serializers

from moviedata.models import Movie, Episode, Comment


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(source='episode.movie', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
