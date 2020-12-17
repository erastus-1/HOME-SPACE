
from flask import render_template,redirect,url_for, abort,request,flash
from . import main
# from ..requests import get_house
from .forms import CommentsForm, EditProfileForm
from ..models import User,House, Language, Comment
from flask_login import login_required, current_user
from .. import db, photos
# import markdown2
from ..email import mail_message



    

# @main.route('/index')
@main.route("/")
def index():

    title = 'Home-  Welcome to The House Space Website'
    return render_template('index.html', title = title)


@main.route("/houses",methods=['GET','POST'])
def houses():

    page = request.args.get('page', 1, type=int)
    Houses = current_user.houses.order_by(House.timestamp.desc()).paginate(
    page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('.house', page=houses.next_num) \
    	if houses.has_next else None
    prev_url = url_for('.house', page=houses.prev_num) \
    	if houses.has_prev else None

    return render_template('houses.html', title='Home', houses=houses.items,
                           next_url=next_url, prev_url=prev_url)



@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('user.html', title='User Profile', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_app.config['ADMIN_LOCKED']:
        super_admin = User.query.filter_by(username='admin').first()
    if current_user == super_admin:
        flash('Super admin\'s profile is locked')
        return redirect(url_for('.user', username=current_user.username))
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        language = Language.query.get(int(form.language.data))
        if language:
            current_user.language = language
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.language.data = current_user.language_id
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@main.route('/about')
def about():
    '''
    View root page function that returns the about page and its data
    '''
    title = ''
    return render_template('about.html', title=title)


@main.route('/contact')
def contact():
    '''
    View root page function that returns the contact page and its data
    '''
    title = ''
    return render_template('contact.html', title = title)

@main.route('/house/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
   
    if form.validate_on_submit():
        new_comment = Comment(house_id =id,comment=form.comment.data)
        new_comment.save_comments()
        return redirect(url_for('main.post',post_id=id))
    
    return render_template('new_comment.html',comment_form=form)
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
    print(type(house_type))
    house_type_list = house_type.split(" ")
    house_type_format = "+".join(house_type_list)
    searched_houses = search_house(house_type_format)


    title = f'search results for {house_type}'

    return render_template('search.html',houses = searched_houses)

