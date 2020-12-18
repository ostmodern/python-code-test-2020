from django_filters.rest_framework import FilterSet
from django_filters import CharFilter, NumberFilter

from moviedata.models import Movie, Episode, Comment


class BaseFilterMixin:
    title = CharFilter(field_name='title', lookup_expr='icontains')

    rating = NumberFilter(field_name='rating')
    rating__gte = NumberFilter(field_name='rating', lookup_expr='gte')
    rating__lt = NumberFilter(field_name='rating', lookup_expr='lt')


class MovieFilter(BaseFilterMixin, FilterSet):
    class Meta:
        model = Movie
        fields = {'title': ['exact'],
                  'rating': ['exact', 'lt', 'gte'],
                  'imdbId': ['exact']}


class EpisodeFilter(BaseFilterMixin, FilterSet):
    class Meta:
        model = Episode
        fields = {'id': ['exact'], 'title': ['exact'],
                  'rating': ['exact', 'lt', 'gte'],
                  'imdbId': ['exact']}


class CommentFilter(FilterSet):
    owner = CharFilter(field_name='owner__username')

    class Meta:
        model = Comment
        fields = ('owner', 'text')
