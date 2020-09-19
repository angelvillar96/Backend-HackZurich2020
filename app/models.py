from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    calories = db.Column(db.Integer)
    foods = db.relationship('Food', backref='consumer', lazy='dynamic')
    #TODO add restrictions

    def __reg__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date_consumed = db.Column(db.DateTime, index=True, default=datetime.now)
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    sugar = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '<Food {}'.format(self.name)
