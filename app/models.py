from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
from time import time
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User( UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), index=True, unique= True)
    email = db.Column(db.String(120), index=True, unique= True)
    password_hash = db.Column(db.String(128))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    language = db.relationship('Language', back_populates='users')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index= True)
    date_entered = db.Column(db.String(32), index = True, unique= True)
    date_out = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

