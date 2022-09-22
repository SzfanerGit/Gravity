from flask import url_for, flash, redirect, render_template
from gravity import app, db
from gravity.forms import RegistrationForm, LoginForm
from gravity.database import User
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
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
    # request.form.get method is handled in forms.py by FlaskForm
    form = LoginForm()
    if form.validate_on_submit():
        if True:
            flash('You have been successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username and/or Password do not match', 'danger')

    return render_template('login.html', form=form)


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    flash('UNDER CONSTRUCTION', 'warning')
    return render_template('index.html')