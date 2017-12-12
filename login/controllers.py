from database import db, Cookie, Role, User_account
from flask import Flask, redirect, url_for


app = Flask(__name__)


if __name__ == '__main__':
    app.run()