from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1/votaciones_splc'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class TableNameExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


class TableNameExampleSchema(ma.ModelSchema):
    class Meta:
        model = TableNameExample


class Cookie(db.Model):
    number_id=db.Column(db.Integer,primary_key=True)
    user_account_id = db.Column(db.Integer)

class CookieSchema(ma.ModelSchema):
    class Meta:
        model = Cookie

class User_account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50))
    password = db.Column(db.String(50))
    email =db.Column(db.String(100))
    role_id= db.Column(db.Integer)


class User_accountSchema(ma.ModelSchema):
    class Meta:
        model = User_account