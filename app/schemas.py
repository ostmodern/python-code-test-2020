from marshmallow import fields

from app import ma
from app.models import Comment, Episode


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment


class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Episode


episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
