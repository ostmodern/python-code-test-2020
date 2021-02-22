from rest_framework import serializers

from comments.models import Comment


class CommentsListSerializer(serializers.ListSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'episode', 'comment_text')
        list_serializer_class = CommentsListSerializer

