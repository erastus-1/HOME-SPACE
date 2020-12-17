from flask import render_template, current_app
from flask_mail import Message
from app.email import send_email


def send_notice_user_about_house_email(user, about):
	""" 
	Send user email if a house/home was added/removed to his account.
	:param user: User model
	:param about: text string. Can be [add, remove]
	"""
	send_email('[Houserent] Notice a house was {}'.format(about),
			   sender=current_app.config['ADMINS'][0],
			   recipients=[user.email],
			   text_body=render_template('houses/email/notice_user_about_house.txt',
			   							 user=user, about=about),
			   html_body=render_template('houses/email/notice_user_about_house.html',
			   							 user=user, about=about))
