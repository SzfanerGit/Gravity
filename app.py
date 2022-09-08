import os

from flask import Flask, url_for, flash, redirect, render_template, request, session
from forms import RegistrationForm, LoginForm
# from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '8aabed13502bfd634e0f338428fe0e59'

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
        flash(f'Account for user: "{form.username.data}" sucessfully created!', 'sucess')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Form submit via POST
    if request.method == 'POST':
        pass
    
    # User reaches via GET
    form = LoginForm()
    return render_template('login.html', form=form)





######################## Live changes for development ########################
if __name__ == '__main__':
    app.run(debug=True)