
 
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
from time import time
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
userhouse_table = db.Table('userhouses', db.Model.metadata,
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('houses_id', db.Integer, db.ForeignKey('houses.id'),
              primary_key=True)
    )

class User( UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), index=True, unique= True)
    email = db.Column(db.String(120), index=True, unique= True)
    password_hash = db.Column(db.String(128))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    language = db.relationship('Language', backref='user')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    houses = db.relationship('House', secondary=userhouse_table,backref='user', lazy='dynamic')
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

class Permission:
    USER = 1
    ADMIN = 2

class Role(db.Model):
    __tablename__ = 'roles'    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.USER],
            'Administrator': [Permission.USER, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def get_name(self):
        return self.name


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
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(5), unique=True)
    users = db.relationship('User', backref='languages')
    Houses = db.relationship('HouseLanguage', backref='languages')

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
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4), index=True)
    names = db.relationship('HouseLanguage', cascade='all, delete-orphan', 
                            backref='housee', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary=userhouse_table,
            backref='housee', lazy='dynamic')
    types = db.Column(db.Integer, index=True, nullable=False)

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
    __tablename__ = 'houselanguages'

    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), primary_key=True)
    types = db.Column(db.Integer, index=True, nullable=False)
    house = db.relationship('House', backref='houseLanguage')
    language = db.relationship('Language', backref='houseLanguage')

    def __init__(self, language, type, **kwargs):
        super(HouseLanguage, self).__init__(**kwargs)
        self.language = language
        self.type = type
    
    def __repr__(self):
        return '<houseLanguage {} {}>'.format(self.language.code, self.type)

    def get_language_code(self):
        return self.language.code

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    house = db.Column(db.Integer,db.ForeignKey("houses.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,houses):
        comments = Comment.query.filter_by(house_id=house).all()
        return comments