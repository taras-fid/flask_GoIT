from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
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


class WorkForm(FlaskForm):
    position = StringField('What do you want to do?', validators=[DataRequired('this field is required')])
    city = SelectField(u'City', choices=[
        ('no_choice', 'no choice'),
        ('kyiv', 'Kiev'),
        ('dnipro', 'Dnipro'),
        ('kharkiv', 'Kharkiv'),
        ('zaporizhia', 'Zaporizhia'),
        ('odessa', 'Odessa'),
        ('lviv', 'Lviv'),
        ('ukraine', 'Ukraine'),
        ('other_countries', 'Other countries ')])
    no_experience = BooleanField('No experience')  # ?experienceType=true
    submit = SubmitField('Save')
