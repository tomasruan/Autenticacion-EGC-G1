from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1/votaciones_splc'

db = SQLAlchemy(app)
ma = Marshmallow(app)


#Modelos de las tablas

class Role(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name


class User_account(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Cookie(db.Model):
    number_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    def __repr__(self):
        return '<Cookie %r>' % self.number_id

