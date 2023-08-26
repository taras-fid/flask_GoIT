from sqlalchemy import ForeignKey
from datetime import time

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    telegram_id = db.Column(db.Integer, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True)
    text = db.Column(db.String(128))
    timestamp_created = datetime.now().timestamp()
    img_path = db.Column(db.String(128))



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref='orders')
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    timestamp_created = datetime.now().timestamp()

    @staticmethod
    def check_date_time(datetime_value):
        time_component = datetime_value.time()

        start_time = time(8, 0)
        end_time = time(16, 0)

        if start_time <= time_component <= end_time:
            return datetime_value
        else:
            raise ValueError('Datetime must be between 8:00 AM and 4:00 PM')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
