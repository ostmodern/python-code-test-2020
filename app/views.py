from decimal import Decimal
from typing import Dict

from connexion import NoContent
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Comment, Episode
from app.schemas import (
    comment_schema, comments_schema, episode_schema, episodes_schema
)


def episodes_retrieve_all(only_best: bool):
    if only_best:
        episodes = db.session.query(Episode).filter(Episode.imdb_rating >= Decimal('8.8')).all()
    else:
        episodes = db.session.query(Episode).all()

    response = episodes_schema.dump(episodes)

    return response, 200


def episode_retrieve_one(id: int):
    episode = db.session.query(Episode).get_or_404(id)
    response = episode_schema.dump(episode)

    return response, 200


def comments_retrieve_all():
    comments = db.session.query(Comment).all()
    response = comments_schema.dump(comments)

    return response, 200


def comment_retrieve_one(id: int):
    comment = db.session.query(Comment).get_or_404(id)
    response = comment_schema.dump(comment)

    return response, 200


def comment_delete_one(id: int):
    comment = db.session.query(Comment).get_or_404(id)
    db.session.delete(comment)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {'error': f'Sqlalchemy Error {repr(ex)}'}, 400

    return NoContent, 204


def comment_update_one(id: int, body: Dict):
    comment = db.session.query(Comment).get_or_404(id)
    text = body.get('text', None)
    episode_id = body.get('episode_id', None)
    episode = db.session.query(Episode).get_or_404(episode_id)

    comment.update({'text': text, 'episode_id': episode_id})
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {'error': f'Sqlalchemy Error {repr(ex)}'}, 400

    response = comment_schema.dump(comment)

    return response, 200


def comment_create_one(body: Dict):
    text = body.get('text', None)
    episode_id = body.get('episode_id', None)
    episode = db.session.query(Episode).get_or_404(episode_id)

    comment = Comment(text=text, episode_id=episode_id)
    db.session.add(comment)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {'error': f'Sqlalchemy Error {repr(ex)}'}, 400
    response = comment_schema.dump(comment)

    return response, 201
