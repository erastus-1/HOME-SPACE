from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,Email


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio.',validators = [Required()])
    submit = SubmitField('Submit')


class FindHome(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    area = StringField('Enter your area youll love to live',validators = [Required()])
    minimum = StringField('Enter the minimum amount you will love to pay',validators = [Required()])
    maximum = StringField('Enter the maximum amount you will love to pay ',validators = [Required()])
    submit = SubmitField('Send')
