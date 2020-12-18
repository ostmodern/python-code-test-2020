from rest_framework.routers import DefaultRouter

from moviedata.views import MovieView, EpisodeView, CommentView

router = DefaultRouter()
router.register(r'movie', MovieView, basename='movie')
router.register(r'episode', EpisodeView, basename='episode')
router.register(r'comment', CommentView, basename='comment')

urlpatterns = router.urls
