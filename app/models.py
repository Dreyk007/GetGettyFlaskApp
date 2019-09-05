from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import os
import base64


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    downloads_count = db.Column(db.Integer)

    token = db.Column(db.String(32), index=True, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_token(self):
        self.token = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
