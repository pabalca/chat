import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    username = db.Column(db.String)
    pwd_hash = db.Column(db.String)

    def __init__(self, username, pwd):
        self.username = username
        self.pwd_hash = generate_password_hash(pwd)

    def __repr__(self):
        return f"<User> {self.username}"

    def verify_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)


class Message(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    who = db.Column(db.String)
    to = db.Column(db.String)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message> <{self.who}:{self.to}> {self.text}"

