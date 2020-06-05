# Docs: https://python-gino.org/docs/en/master/how-to/schema.html#gino-orm
from backend.db import db
import bcrypt
from passlib.context import CryptContext
import datetime
import jwt
from backend.config import SECRET_KEY


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String, nullable=False)
    errors = db.Column(db.ARRAY(db.String))
    created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    def __repr__(self):
        return self.email


class Whitelist(db.Model):
    __tablename__ = "whitelist"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=True)

    def __repr__(self):
        return self.word
