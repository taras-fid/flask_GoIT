from flask_login import login_required, current_user, logout_user, login_user
from app import app, db
from app.forms import SignInForm, SignUpForm
from flask import flash, redirect, url_for, render_template, request
from app.models import User, Task
import datetime


def delete_completed_tasks():
    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    completed_tasks = Task.query.filter(
        Task.completed == True,
        Task.updated_at <= one_week_ago
    ).all()

    for task in completed_tasks:
        db.session.delete(task)

    db.session.commit()


@app.route('/')
def index():
    delete_completed_tasks()
    tasks = Task.query.all()
    return render_template('view_tasks.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        new_task = Task(text=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # TODO: змінити логіку видалення - не видаляти запис з бд, а змінювати статус('completed') на `True`
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))


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
