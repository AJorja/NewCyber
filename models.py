from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)
    dateSubmitted = db.Column(db.DateTime)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
        self.dateSubmitted = datetime.today()

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challengeTitle = db.Column(db.String(255))
    description = db.Column(db.Text)
    hint = db.Column(db.Text)
    flag = db.Column(db.String(255))
    points = db.Column(db.Integer, default=100)
    file_url = db.Column(db.String(255))
    learning_outcomes = db.Column(db.Text)  # Will store learning outcomes as a JSON string or plain text

class ChallengeCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    user_level = db.Column(db.Integer)
    score = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean)

    def set_password (self, password):
        self.password_hash = generate_password_hash(password)

    def check_password (self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        if self.user_level == 2:
            return True
        else:
            return False

    def update_details(self, email_address, name):
        self.email_address = email_address
        self.name = name

from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))