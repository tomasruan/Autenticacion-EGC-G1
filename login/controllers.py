from database import db, Cookie, Role, User_account
from flask import Flask, redirect, url_for, request, render_template
from flask.json import jsonify

app = Flask(__name__)


@app.route('/cookie/<int:number_id>')
def check_cookies(number_id):
    cookie_id = number_id
    cookie_db = Cookie.query.get(cookie_id)

    if cookie_db is not None:
        user_account_db = User_account.query.get(cookie_db.user_account_id)
        user_account_dict = {"id": user_account_db.id,
                             "username": user_account_db.username,
                             "password": user_account_db.password,
                             "email": user_account_db.email,
                             "role_id": user_account_db.role_id}
        res = {"codigo": 1,
               "status": "Cookie valida y existente en la base de datos",
               "usuario": user_account_dict}
    else:
        res = {"codigo": 0,
               "status": "Cookie Incorrecta, no existe en la base de datos",
               "usuario": None}

    return jsonify(res)


@app.route('/logout/<int:number_id>')
def logout_user(number_id):
    cookie_id = number_id
    cookie = Cookie.query.get(cookie_id)

    if cookie is not None:
        db.session.delete(cookie)
        db.session.commit()

    return redirect('/login')


if __name__ == '__main__':
    app.run()
