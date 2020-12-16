from flask import render_template, current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
	email = Message(subject, sender=sender, recipients=recipients)
	email.body = text_body
	email.html = html_body
	mail.send(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# def mail_message(subject,template,to,**kwargs):
#     sender_email = maranahuwase12@gmail.com

#     email = Message(subject, sender=sender_email, recipients=[to])
#     email.body= render_template(template + ".txt",**kwargs)
#     email.html = render_template(template + ".html",**kwargs)
#     mail.send(email)