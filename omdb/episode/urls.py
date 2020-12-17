from django.urls import path

from .views import index, download_game_of_thrones_series, EpisodesList,\
     EpisodesRetreive, HighlyRatedEpisodesList,  CommentListCreate, CommentRetrieveUpdateDestroy


urlpatterns = [
    path('', index, name='home'),
    path('download-episodes/', download_game_of_thrones_series, name='download-series'),
    path('episodes/', EpisodesList.as_view(), name='episodes-list'),
    path('episodes/<int:pk>/', EpisodesRetreive.as_view(), name='episode-retrieve'),
    path('episodes/get-highly-rated/', HighlyRatedEpisodesList.as_view(), name='episodes-highly-rated'),
    path('episodes/<int:pk>/comments/', CommentListCreate.as_view(), name='comments-list-create'),
    path('comments/<int:comment_pk>/', CommentRetrieveUpdateDestroy.as_view(), name='comments-list-create')
]