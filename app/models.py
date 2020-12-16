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

class AnonymousUser(AnonymousUserMixin):
    __tablename__ = 'user'

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
 
#     def Login():
    
#         if start == "Login":
#             Login()


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(5), unique=True)
    users = db.relationship('User', back_populates='language')
    Houses = db.relationship('HouseLanguage', back_populates='language')

    def __repr__(self):
        return '<Language {}>'.format(self.code)

    @staticmethod
    def insert_values():
        values = [('English', 'en'),
                  ('French', 'fr')]
        for name, code in values:
            exist = Language.query.filter_by(code=code).first()
            if exist:
                continue
            new_lang = Language(name=name, code=code)
            db.session.add(new_lang)
        db.session.commit()

    def get_name(self):
        return self.name


class House(db.Model):
    __tablename__ = 'house'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4), index=True)
    names = db.relationship('HouseLanguage', cascade='all, delete-orphan', 
                            back_populates='house', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary=userhouse_table,
            back_populates='houses', lazy='dynamic')

    def __repr__(self):
        return '<House {}>'.format(self.get_name('en'))

    # House types. 
    def set_type(self, language, type):
        self.types.append(HouseLanguage(language, type))
    
    def get_type(self, lang_code='en', year=True):
        q = self.types.join('language').filter(Language.code==lang_code).first()
        # If it does not have a type for the selected language, give the default 'en'.
        if not q.type:
            q = self.types.join('language').filter(Language.code=='en').first() 
        # leave the housein a particular time before one year.
        if not self.year:
            return q.type
        # leave a house after one year
        return '|'.join((q.type, self.year)) if year else q.type


class HouseLanguage(db.Model):
    __tablename__ = 'houselanguage'

    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), primary_key=True)
    type = db.Column(db.String(124), index=True, nullable=False)
    house = db.relationship('House', back_populates='types')
    language = db.relationship('Language', back_populates='types')

    def __init__(self, language, type, **kwargs):
        super(HouseLanguage, self).__init__(**kwargs)
        self.language = language
        self.type = type
    
    def __repr__(self):
        return '<houseLanguage {} {}>'.format(self.language.code, self.type)

    def get_language_code(self):
        return self.language.code

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    house = db.Column(db.Integer,db.ForeignKey("house.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,houses):
        comments = Comment.query.filter_by(house_id=house).all()
        return comments



    
