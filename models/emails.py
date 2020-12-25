from dataclasses import dataclass

from models.db import db


@dataclass
class Email(db.Model):
    email: str

    email = db.Column(db.String(120), primary_key=True)

    def __repr__(self):
        return "<Email %r>" % self.email

    def subscribe(self):
        db.session.add(self)
        db.session.commit()

    def unsubscribe(self):
        db.session.delete(self)
        db.session.commit()
