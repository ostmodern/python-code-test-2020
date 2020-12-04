from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from app.db.models import Episode, EpisodeComment


def get_episodes_by_series_title(db: Session, title: str):
    return (
        db.query(Episode)
        .filter(Episode.series_title.like(title))
        .all()
    )


def get_episode_by_id(db: Session, episode_id: int):
    try:
        return db.query(Episode).filter(Episode.id == episode_id).one()
    except (MultipleResultsFound, NoResultFound) as e:
        return


def get_episode_comments(db: Session, episode_id: int):
    return (
        db.query(EpisodeComment)
        .filter(EpisodeComment.episode_id == episode_id)
        .all()
    )


def add_episode_comment(db: Session, user_id: int, episode_id: int, data: dict):
    new_episode_comment = EpisodeComment(user_id=user_id, episode_id=episode_id, **data)
    db.add(new_episode_comment)
    db.commit()

    return db.query(EpisodeComment).filter(EpisodeComment.id == new_episode_comment.id).one()


def update_episode_comment(db: Session, comment_id: int, data: dict):
    try:
        existing_episode = db.query(EpisodeComment).filter(EpisodeComment.id == comment_id).one()
    except (MultipleResultsFound, NoResultFound) as e:
        return

    for attr, value in data.items():
        setattr(existing_episode, attr, value)

    db.commit()
    return db.query(EpisodeComment).filter(EpisodeComment.id == existing_episode.id).one()


def delete_episode_comment(db: Session, comment_id: int):
    try:
        existing_episode = db.query(EpisodeComment).filter(EpisodeComment.id == comment_id).one()
        db.delete(existing_episode)
        db.commit()
        return True
    except (MultipleResultsFound, NoResultFound) as e:
        return


