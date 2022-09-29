from flask import url_for, flash, redirect, render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from gravity import db
from gravity.database import User
from gravity.users.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from gravity.users.utils import send_password_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # request.form.get method is handled in forms.py by FlaskForm
    form = RegistrationForm()
    # user subbmits form via POST
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)

        # Create user and add them to the database
        user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()

        flash(f'Hello "{form.username.data}"! You have sucessfully created your account. Please login', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # request.form.get method is handled in forms.py by FlaskForm
    # user subbmits form via POST
    form = LoginForm()
    if form.validate_on_submit():
        # querry the database
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # function from flask_login
            login_user(user, remember=form.remember.data)
            flash('You have been successfully logged in!', 'success')

            # Redirect user back to the page they tried to acces but were requred to login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Username and/or Password do not match', 'danger')

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    return render_template('account.html')



@users.route("/password_reset", methods=['GET', 'POST'])
def password_reset_request():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Sending password reset email
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('A password reset email has been sent. Check your inbox to reset password.', 'info')
        return redirect(url_for('users.login'))

    return render_template('password_reset.html', form=form)


@users.route("/password_reset/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Ensure token is valid and non expired
    user = User.verify_reset_token(token)
    if user is None:
        flash('This request has expired or is invalid. Request password reset again.', 'warning')
        return redirect(url_for('users.password_reset_request'))
    
    # New password form and assigment
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user.password = password_hash
        db.session.commit()
        flash(f'Your password has been reset. Please login', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', form=form)