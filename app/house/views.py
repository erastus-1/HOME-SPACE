from flask import render_template, request, url_for, flash, redirect, current_app
from flask_login import current_user, login_required
from app import db
from app.decorators import admin_required
from app.models import User, House, Language, HouseLanguage
from .forms import UserForm, EditUserProfileForm, UserAddHouseForm, HouseForm

from . import house

# Get all users.
@house.route('/users')
@login_required
@admin_required
def users():
	page = request.args.get('page', 1, type=int)
	users = User.query.order_by(User.username.asc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('.users', page=users.next_num) \
					   if users.has_next else None
	prev_url = url_for('.users', page=users.prev_num) \
					   if users.has_prev else None
	return render_template('houses/users.html', title='Explore Users', users=users.items, 
							total=users.total, next_url=next_url, prev_url=prev_url)

#
# Edit user's profile.
@house.route('/users/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_profile(id):
	user = User.query.get_or_404(id)

	if current_app.config['ADMIN_LOCKED']:
		super_admin = User.query.filter_by(username='admin').first()
	if user == super_admin:
		flash('Super admin\'s profile is locked')
		return redirect(url_for('.user', id=user.id))

	form = EditUserProfileForm(original_username = user.username,
							   original_email = user.email)
	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		user.language_id = int(form.language.data)
		user.role_id = form.role.data
		db.session.commit()
		flash('User\'s profile was successfuly updated.')
		return redirect(url_for('.user', id=user.id))

	form.username.data = user.username
	form.email.data = user.email
	form.language.data = user.language_id
	form.role.data = user.role_id
	return render_template('houses/edit_user_profile.html', title='Update user\'s profile', form=form)

# Create user.
@house.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
	form = UserForm()
	if form.validate_on_submit():
		user = User(
					username=form.username.data,
					email=form.email.data,
					language_id=int(form.language.data)
					)
		user.set_password(form.password.data)
		user.role_id = form.role.data
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you have added new user!')
		return redirect(url_for('.users'))

	return render_template('houses/create_user.html', title='Create new user', form=form)

# Delete user.
@house.route('/users/delete/<int:id>')
@login_required
@admin_required
def delete_user(id):
	user = User.query.get_or_404(id)
	admin_locked = current_app.config['ADMIN_LOCKED']
	super_admin = None
	if admin_locked: 
		super_admin = User.query.filter_by(username='admin').first()
	if user != super_admin:
		username = user.username
		db.session.delete(user)
		db.session.commit()
		flash('User {} was successfuly deleted'.format(username))
	else: 
		flash('Can\'t delete super admin')
	return redirect(url_for('.users'))

@house.route('/housers')
@login_required
@admin_required
def houses():
	page = request.args.get('page', 1, type=int)
	houses = House.query.order_by(House.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('.houses', page=houses.next_num) \
		if houses.has_next else None
	prev_url = url_for('.houses', page=houses.prev_num) \
		if houses.has_prev else None
	return render_template('houses/houses.html', title='Houses', houses=houses.items,
						   total=houses.total, next_url=next_url, prev_url=prev_url)


@house.route('/houses/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_house():
	HouseForm.add_fields()
	form = HouseForm()
	if form.validate_on_submit():
		house = House()
		#language
		langs = Language.query.all()
		for key in form.data:
			if key in [lang.code for lang in langs]:
				lang = [lang for lang in langs if lang.code == key]
				house.types.append(HouseLanguage(name=form.data[key], language=lang[0]))
		house.year = int(form.year.data)
		db.session.add(house)
		db.session.commit()
		flash('You successfuly created a new house')
		return redirect(url_for('.houses'))

	return render_template('houses/create_house.html', title='Create a new House', form=form)
