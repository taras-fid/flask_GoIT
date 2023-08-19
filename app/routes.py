from flask_login import login_required, current_user, logout_user, login_user
from app import app, db
from app.forms import SignInForm, SignUpForm, EditProfileForm
from flask import flash, redirect, url_for, render_template, request, current_app, send_from_directory
from app.models import User, Post, Order
import os


@app.route('/')
def index():
    posts = Post.query.filter_by().all()
    return render_template('main.html', title='Main page', posts=posts)


@app.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=orders)


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


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(uploads, filename)