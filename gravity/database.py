from gravity import db

# Database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_img.jpg')

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"