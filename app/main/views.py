from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from .. import db
from .forms import UpdateProfile,QuoteForm,CommentForm
from flask_login import login_required,current_user
import datetime


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