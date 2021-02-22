from django.urls import path, include
from rest_framework.routers import SimpleRouter

from seasons.views import EpisodeViewSet

episodes_viewset_router = SimpleRouter()
episodes_viewset_router.register('episodes', EpisodeViewSet, basename='episodes')

urlpatterns = [
    path('', include(episodes_viewset_router.urls))
]
