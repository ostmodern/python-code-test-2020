from django.urls import path, include
from rest_framework.routers import SimpleRouter

from comments.views import CommentViewSet

comments_viewset_router = SimpleRouter()
comments_viewset_router.register('', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(comments_viewset_router.urls))
]
