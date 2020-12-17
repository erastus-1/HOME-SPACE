from wtforms import StringField, SelectField, SubmitField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired, ValidationError,Required,Email,EqualTo
from flask_wtf import FlaskForm
from app.models import User, Language

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    language = SelectField('Language', coerce=int, validators=[DataRequired()])
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        # Populate choices of language.
        self.language.choices = Language.choices()

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('SUBMIT') 

           
class FindHome(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    area = StringField('Enter area you will love to live',validators = [Required()])
    minimum = StringField('Enter minimum amount to pay',validators = [Required()])
    maximum = StringField('Enter maximum amount to pay',validators = [Required()])
    submit = SubmitField('Sent')