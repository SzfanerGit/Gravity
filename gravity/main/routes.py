from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/home")
@main.route("/")
def home():
    # user = User(username=form.username.data, email=form.email.data, password=password_hash)
    # db.session.add(user)
    # db.session.commit()
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html')