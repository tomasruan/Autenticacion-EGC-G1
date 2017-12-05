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
