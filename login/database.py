from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@127.0.0.1/votaciones_splc'

db = SQLAlchemy(app)
ma = Marshmallow(app)


#Vamos a necesitar 2 modelos y 2 schemas (1 schema por cada modelo)


class TableNameExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),)

#Modelos de las tablas

class user_account(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    title = db.Column(db.String(100),)

    def __repr__(self):
        return '<User %r>' % self.username


#Schemas de las tablas

class TableNameExampleSchema(ma.ModelSchema):
    class Meta:
        model = TableNameExample
