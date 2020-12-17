from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from .. import db
from .forms import UpdateProfile
from flask_login import login_required
import datetime
from ..email import mail_message


@main.route('/')
def index():

    title = 'Home-  Welcome to The House Space Website'
    return render_template('index.html', title = title)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)


main.route('/subscribe', methods=['GET','POST'])
def subscribe():
    '''
    Function to send email upon subscription
    '''
    if request.method == 'POST':
        email = request.form['email']
        new_email = Subscribe(email=email)
        db.session.add(new_email)
        db.session.commit()

        mail_message("Thank you for picking us","email/home_user",user.email,user=user)

        return redirect(url_for('main.index'))

    return render_template('profile/home.html',form = form)     