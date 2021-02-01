from marshmallow import fields

from app import ma
from app.models import Comment, Episode


class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    imdb_rating = fields.Function(lambda obj: str(obj.imdb_rating))

    class Meta:
        model = Episode


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment


episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
