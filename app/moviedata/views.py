from rest_framework import viewsets, generics
from rest_framework.response import Response

from moviedata import omdb
from moviedata.filters import MovieFilter, EpisodeFilter, CommentFilter
from moviedata.models import Movie, Episode, Comment
from moviedata.serializer import MovieSerializer, EpisodeSerializer, CommentSerializer


class IMDBQueryMixin:
    def _get_items(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    def load_from_imdb(self, request, *args, **kwargs):
        raise NotImplemented('Must be implemented')

    def list(self, request, *args, **kwargs):
        items = self._get_items()
        if not items:
            self.load_from_imdb(request, *args, **kwargs)
            items = self._get_items()
        return Response(items)


class MovieView(IMDBQueryMixin, viewsets.ModelViewSet):
    filterset_class = MovieFilter
    serializer_class = MovieSerializer
    queryset = Movie.objects

    def load_from_imdb(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        if title:
            res = omdb.title(title)
            movie = Movie.handle_omdb_data(res)
            movie.save()
            for season in range(1, movie.total_seasons + 1):
                season_data = omdb.get(title=title, season=season)
                season_data['season'] = season
                episodes = Episode.handle_omdb_data(movie, season_data)
                Episode.objects.bulk_create(episodes)


class EpisodeView(IMDBQueryMixin, viewsets.ModelViewSet):
    filterset_class = EpisodeFilter
    serializer_class = EpisodeSerializer
    queryset = Episode.objects

    def load_from_imdb(self, request, *args, **kwargs):
        episode_id = request.query_params.get('episode')
        if episode_id:
            episode_data = omdb.imdbid(episode_id)
            movie_id = episode_data['seriesID']
            movie = Movie.objects.filter(imdbId=movie_id).first()
            if not movie:
                movie_data = omdb.imdbid(movie_id)
                movie = Movie.handle_omdb_data(movie_data)
                movie.save()
            episode = Episode.handle_omdb_data([episode_data])
            episode[0].save()


class CommentView(viewsets.ModelViewSet):
    filterset_class = CommentFilter
    serializer_class = CommentSerializer
    queryset = Comment.objects
