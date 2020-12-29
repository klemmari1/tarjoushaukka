from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from models.db import db


@dataclass
class Post(db.Model):
    id: int
    likes: int
    page: int
    time: datetime
    url: str
    content: str
    content_plain: str
    is_sent: bool

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    likes = db.Column(db.Integer)
    page = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    url = db.Column(db.String(1000))
    content = db.Column(db.String(8000))
    content_plain = db.Column(db.String(8000))
    is_sent = db.Column(db.Boolean())

    def __repr__(self):
        return "<Post %r>" % self.id
