from flask import url_for, flash, redirect, render_template, request
from gravity import app, db, mail
from gravity.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from gravity.database import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Username and/or Password do not match', 'danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html')


def send_password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='gravity.project.app@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset_request():
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Sending password reset email
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('A password reset email has been sent. Check your inbox to reset password.', 'info')
        return redirect(url_for('login'))

    return render_template('password_reset.html', form=form)


@app.route("/password_reset/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Ensure token is valid and non expired
    user = User.verify_reset_token(token)
    if user is None:
        flash('This request has expired or is invalid. Request password reset again.', 'warning')
        return redirect(url_for('password_reset_request'))
    
    # New password form and assigment
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user.password = password_hash
        db.session.commit()
        flash(f'Your password has been reset. Please login', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', form=form)