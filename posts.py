from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


ADT = NewType("ADT", datetime)  # timezone aware datetime


@dataclass
class Post(db.Model):
    id: int
    likes: int
    page: int
    time: ADT
    url: str
    content: str
    content_plain: str
    is_sent: bool

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    likes = db.Column(db.Integer)
    page = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    url = db.Column(db.String(1000))
    content = db.Column(db.String(5000))
    content_plain = db.Column(db.String(5000))
    is_sent = db.Column(db.Boolean())

    def __repr__(self):
        return "<Post %r>" % self.id
