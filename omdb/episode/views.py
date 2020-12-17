import requests

from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import EpisodeSerializer, CommentSerializer
from .models import Comment, Episode


def index(request):
    download_game_of_thrones_series = reverse('download-series')
    episodes_list_url = reverse('episodes-list')
    highly_rated_episodes_url = reverse('episodes-list')
    response = """<h1>Home page</h1>
    <p>In order to download the game of thrones episodes follow: <a href={}>Link</a><p>
    <p>In order to see the list of episodes follow: <a href={}>Link</a><p>
    <p>In order to see the list of highly rated episodes follow: <a href={}>Link</a><p>
    """.format(download_game_of_thrones_series, episodes_list_url, highly_rated_episodes_url)
    return HttpResponse(response)

def download_game_of_thrones_series(request):
    api_key = settings.OMDB_API_KEY
    params = {'apikey': api_key, 't':'Game of Thrones'}
    seasons_number = requests.get('http://www.omdbapi.com/', params=params, timeout=10).json().get('totalSeasons')
    for season_number in range(1, (int(seasons_number)+1)):
        params['Season'] = season_number
        episodes = requests.get('http://www.omdbapi.com/', params=params, timeout=10).json().get('Episodes')
        for episode in episodes:
            e, _ = Episode.objects.get_or_create(
                episode_number = episode.get('Episode'),
                title = episode.get('Title'),
                season = season_number,
                release_date = episode.get('Released'),
                imdb_rating = episode.get('imdbRating')
            )
            e.save()
    episodes_list_url = reverse('episodes-list')
    return HttpResponse(f'Game of thrones series are downloaded successfully and case be seen on <a href={episodes_list_url}>Link</a>')


class EpisodesList(generics.ListAPIView):
    queryset = Episode.objects.all().order_by('release_date')
    serializer_class = EpisodeSerializer


class HighlyRatedEpisodesList(generics.ListAPIView):
    queryset = Episode.objects.filter(imdb_rating__gt=8.8).order_by('release_date')
    serializer_class = EpisodeSerializer


class EpisodesRetreive(generics.RetrieveAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk):
        queryset = self.get_queryset().filter(episode=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        episode_pk = self.kwargs.get('pk')
        episode = get_object_or_404(Episode, pk=episode_pk)
        return serializer.save(episode=episode, user=self.request.user)


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_pk'))
