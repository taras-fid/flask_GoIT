from flask_login import login_required, current_user, logout_user, login_user
from app import app, db
from app.forms import SignInForm, SignUpForm, EditProfileForm, WorkForm
from flask import flash, redirect, url_for, render_template, request
from app.models import User
import requests


@app.route('/')
def index():
    if request.args.get('url'):
        return render_template('main.html', title='Main page', url=request.args['url'])
    else:
        return render_template('main.html', title='Main page', url='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Sign in requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('sign_in.html', title='Sign in123', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if the email address already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is not None:
            flash('The email address is already registered')
            return redirect(url_for('sign_up'))

        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to our community')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.telegram_id = form.telegram_id.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit profile', form=form)


@app.route('/work-form', methods=['GET', 'POST'])
@login_required
def work_form():
    form = WorkForm()
    if form.validate_on_submit():
        flash(f'Your changes have been saved.')
        url = f'https://robota.ua/zapros/{form.position.data}/{"ukraine" if "no_choice" == form.city.data else form.city.data}?experienceType={str(form.no_experience.data).lower()}'
        #  TODO: parse url and send to bot
        result = 'test'
        requests.get(f'https://api.telegram.org/bot5803031167:AAGyRzVMJUWTvUl8PLEqC4CiR3pK1duXxH4/sendMessage?chat_id=623695791&text={result}')
        return redirect(url_for('index', url=url))
    return render_template('work_form.html', title='Work form', form=form)
