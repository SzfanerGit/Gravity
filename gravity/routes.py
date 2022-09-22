from flask import url_for, flash, redirect, render_template, request
from gravity import app
from gravity.forms import RegistrationForm, LoginForm
from gravity.database import User

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Form submit via POST
    if request.method == 'POST':
        pass
    
    # User reaches via GET
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account for user: "{form.username.data}" sucessfully created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Form submit via POST
    if request.method == 'POST':
        pass
    
    # User reaches via GET
    form = LoginForm()
    if form.validate_on_submit():
        if True: #TODO make database for accounts
            flash('You have been successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username and/or Password do not match', 'danger')

    return render_template('login.html', form=form)


@app.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    flash('UNDER CONSTRUCTION', 'warning')
    return render_template('index.html')