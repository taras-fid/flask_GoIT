from app import app
from app.forms import SignInForm, SignUpForm
from flask import flash, redirect, url_for, render_template


@app.route('/')
def index():
    return render_template('main.html', title='Sign up')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        flash('Sign in requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('sign_in.html', title='Sign in123', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Welcome to our community')
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', title='Sign up', form=form)
