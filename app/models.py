from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    Integer,
    Date,
    DateTime,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    episode_id = Column(Integer, ForeignKey('episodes.id'), nullable=False)

    def __repr__(self):
        return f'Comment #{self.id} {self.text}'


class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    released = Column(Date)
    season = Column(Integer)
    episode = Column(Integer)
    imdb_rating = Column(Numeric(2, 1))
    imdb_id = Column(String(100), index=True)
    comments = relationship('Comment', backref='episode', lazy='dynamic')

    def __repr__(self):
        return f'<S{self.season}E{self.episode} "{self.title}">'
