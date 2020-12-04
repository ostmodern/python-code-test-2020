import logging
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import Episode
from app.db.utils import (
    get_episodes_by_series_title,
    get_episode_by_id,
    get_episode_comments,
    add_episode_comment,
    update_episode_comment,
    delete_episode_comment,
)
from app.utils import IMDBSeries

from pydantic import BaseModel

from app.db.base import Base, engine

Base.metadata.create_all(bind=engine)


class EpisodeCommentItem(BaseModel):
    text: str


log = logging.getLogger(__name__)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/episodes/")
def read_episodes(db: Session = Depends(get_db), q: Optional[str] = Query(None)):
    episodes = get_episodes_by_series_title(db=db, title=q)
    if episodes:
        return {"data": episodes}

    episodes_list = []
    series = IMDBSeries(series_title=q)
    series_data = series.get_series_data()
    episodes_list_data = series.get_all_episodes()
    if episodes_list_data:
        for episode_item in episodes_list_data:
            rating = episode_item.get('imdbRating')
            episode_obj = Episode(
                title=episode_item.get('Title'),
                year=series_data.get('Year'),
                uuid=episode_item.get('Episode'),
                rating=None if rating == 'N/A' else rating,
                season_uuid=episode_item.get('Season'),
                series_title=series_data.get("Title"),
                series_uuid=series_data.get("imdbID"),
                director=series_data.get("Director"),
            )
            db.add(episode_obj)
        db.commit()

        episodes = get_episodes_by_series_title(db=db, title=q)
        if episodes:
            return {"data": episodes}

    return {"data": episodes_list}


@app.get("/episodes/{episode_id}")
def read_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = get_episode_by_id(db=db, episode_id=episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found.")

    return {"data": episode}



@app.get("/episodes/{episode_id}/comments")
def read_episode_comments(episode_id: int, db: Session = Depends(get_db)):
    episode_comments = get_episode_comments(db=db, episode_id=episode_id)
    return {"data": episode_comments}


@app.post("/episodes/{episode_id}/comments")
def write_episode_comment(episode_id: int, comment: EpisodeCommentItem, db: Session = Depends(get_db)):
    episode = get_episode_by_id(db=db, episode_id=episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found.")

    episode_comment = add_episode_comment(db=db, user_id=1, episode_id=episode_id, data=comment.dict())
    return {"data": episode_comment}


@app.patch("/episodes/{episode_id}/comments/{comment_id}")
def update_comment(episode_id: int, comment_id: int, comment: EpisodeCommentItem, db: Session = Depends(get_db)):
    episode_comment = update_episode_comment(db=db, comment_id=comment_id, data=comment.dict())
    if not episode_comment:
        raise HTTPException(status_code=404, detail="Episode comment not found.")

    return {"data": episode_comment}


@app.delete("/episodes/{episode_id}/comments/{comment_id}")
def delete_comment(episode_id: int, comment_id: int, db: Session = Depends(get_db)):
    is_successful = delete_episode_comment(db=db, comment_id=comment_id)
    if not is_successful:
        raise HTTPException(status_code=404, detail="Episode comment not found.")

    return {"data": None}