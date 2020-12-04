from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    comments = relationship("EpisodeComment", back_populates="user")


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    year = Column(Integer)
    uuid = Column(String)
    rating = Column(Float)
    director = Column(String, nullable=True)
    series_title = Column(String)
    series_uuid = Column(String)
    season_title = Column(String, nullable=True)
    season_uuid = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    comments = relationship("EpisodeComment", back_populates="episode")


class EpisodeComment(Base):
    __tablename__ = "episode_comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(length=512), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    episode_id = Column(Integer, ForeignKey("episodes.id"))

    episode = relationship("Episode", back_populates="comments")
    user = relationship("User", back_populates="comments")
