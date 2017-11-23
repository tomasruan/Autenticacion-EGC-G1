from database import db, User, UserSchema
from flask import Flask, redirect, url_for


app = Flask(__name__)


@app.route('/')
def root():
    users_schema = UserSchema(many=True)
    all_users = User.query.all()

    return users_schema.dump(all_users).data






if __name__ == '__main__':
    app.run()