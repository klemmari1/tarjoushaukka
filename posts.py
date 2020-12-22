from dataclasses import dataclass
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class Post(db.Model):
    id: int
    likes: int
    page: int
    time: datetime
    url: str
    content: str
    content_plain: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    likes = db.Column(db.Integer)
    page = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    url = db.Column(db.String(1000))
    content = db.Column(db.String(5000))
    content_plain = db.Column(db.String(5000))

    def __repr__(self):
        return "<Post %r>" % self.id
