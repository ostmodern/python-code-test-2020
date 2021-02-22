from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(methods=['GET'], detail=False)
    def episode_comments(self, request, *args, **kwargs):
        episode_id = request.query_params.get('episode_id')
        if episode_id:
            serializer = self.get_serializer_class()
            return Response(serializer(self.queryset.filter(episode__id=int(episode_id)), many=True).data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

