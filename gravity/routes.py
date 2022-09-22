from flask import url_for, flash, redirect, render_template, request
from gravity import app, db
from gravity.forms import RegistrationForm, LoginForm
from gravity.database import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # request.form.get method is handled in forms.py by FlaskForm
    form = RegistrationForm()
    # user subbmits form via POST
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello "{form.username.data}"! You have sucessfully created your account. Please login', 'success')
        return redirect(url_for('login'))
    # User reached via GET
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # request.form.get method is handled in forms.py by FlaskForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Username and/or Password do not match', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html')


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    flash('UNDER CONSTRUCTION', 'warning')
    return render_template('index.html')