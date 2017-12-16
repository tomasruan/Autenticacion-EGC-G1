from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


uri_database = 'mysql://{user}:{password}@{host}:{port}/votaciones_splc'.format(user=os.environ['MARIADB_USER'],
                                                                                password=os.environ['MARIADB_PASSWORD'],
                                                                                host=os.environ['MARIADB_HOST'],
                                                                                port=os.environ['MARIADB_PORT'])

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri_database

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Modelos de las tablas

class Role(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name


class User_account(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Cookie(db.Model):
    number_id = db.Column(db.String(40), nullable=False, primary_key=True)
    user_account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    def __repr__(self):
        return '<Cookie %r>' % self.number_id
