from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from .. import db
from .forms import UpdateProfile
from flask_login import login_required
import datetime



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

@main.route('/search/<house_type>')
def search(house_type):
    '''
    View function to display the search results
    '''
    print(type(house_type)
    house_type_list = house_type.split(" ")
    house_type_format = "+".join(house_type_list)
    searched_houses = search_house(house_type_format)


    title = f'search results for {house_type}'
    
    return render_template('search.html',houses = searched_houses)

