from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('ви маєте заповнити це поле')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Sign Un')


class EditProfileForm(FlaskForm):
    username = StringField('Username')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=128)])
    telegram_id = StringField('Telegram ID')
    submit = SubmitField('Save')
