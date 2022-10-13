from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from gravity import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    satelites = db.relationship('Satelite', backref='owner', lazy=True)
    plots = db.relationship('Plot', backref='author', lazy=True)

    def get_reset_token(self, expire_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Satelite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default='Satelite')
    # position and velocity have format 'x_val, y_val, z_val' as string,
    # need to convert them into int list or array before proper use
    pos_0 = db.Column(db.String, nullable=False)
    vel_0 = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Satelite('{self.pos_0}', '{self.vel_0}', '{self.user_id}')"


class Plot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plot_image = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Plot('{self.plot_image}', '{self.user_id}')"