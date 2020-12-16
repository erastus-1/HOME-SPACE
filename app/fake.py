from datetime import datetime
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app import db
from app.models import User, House, HouseLanguage, Language


house_types = [
('appartment', 'appartement'),
('single-family detached', 'unifamiliale détachée'),
('Tinny home', 'petite maison'),
('cape cod', 'cape cod'),
('contamporary', 'contamporaire'),
('cottage', 'chalet'),
('french country', 'pays français')
]


def users(count=100):
	fake = Faker()
	i = 0
	lang_count = Language.query.count()
	while i < int(count):
		u = User(username=fake.user_name(),
				 email=fake.email()
		)
		u.language = Language.query.offset(randint(0, lang_count - 1)).first()
		u.set_password('password')
		db.session.add(u)
		try:
			db.session.commit()
			i += 1
		except IntegrityError:
			db.session.rollback()
	print('{} fake users were successfully created.'.format(i))

def houses(count=100):
	fake = Faker()
	i = 0
	user_count = User.query.count()
	langs = Language.query.all()
	house_types_len = len(house_types)
	while i < int(count):
		u = User.query.offset(randint(0, user_count - 1)).first()
		h = House()
		h.year = randint(1970, datetime.now().year)
		h.timestamp = fake.past_date()
		h.users.append(u)
		for lang in langs:
			if lang.code == 'en':
				h.set_type(lang, house_types[randint(0, house_types_len - 1)][0])
			elif lang.code == 'fr':
				c.set_type(lang, house_types[randint(0, house_types_len - 1)][1])
		db.session.add(c)
		try:
			db.session.commit()
			i += 1
		except IntegrityError:
			db.session.rollback()
		print('{} fake houses were successfully created.'.format(i))
