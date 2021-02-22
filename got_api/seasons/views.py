from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from seasons.models import Episode
from seasons.serializers import EpisodeSerializer


class EpisodeViewSet(ModelViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()

    @action(methods=['GET'], detail=False)
    def filter_episodes(self, request, *args, **kwargs):
        query = Q()

        season = request.query_params.get('season')
        if season:
            query &= Q(season_number=season)

        gt_imdb_rating = request.query_params.get('gt_imdb_rating')
        if gt_imdb_rating:
            query &= Q(imdb_rating__gt=gt_imdb_rating)

        lt_imdb_rating = request.query_params.get('lt_imdb_rating')
        if lt_imdb_rating:
            query &= Q(imdb_rating__lt=lt_imdb_rating)

        return Response(self.serializer_class(self.queryset.filter(query), many=True).data)



