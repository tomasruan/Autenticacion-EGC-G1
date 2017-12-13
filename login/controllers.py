from database import db, Cookie, Role, User_account
from flask import Flask, redirect, url_for, request, render_template
from flask.json import jsonify

app = Flask(__name__)


@app.route('/cookies/<int:number_id>')
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


@app.route('/users/<int:user_id>/role', methods=['PUT'])
def assign_role(user_id):
    user = User_account.query.filter_by(id=user_id).first()
    role_assigned = Role.query.get(request.json.get('role_id'))

    if user is not None:
        if role_assigned is not None:
            user.role_id = role_assigned.id
            db.session.commit()

            user_account_json = {"id": user.id,
                                 "username": user.username,
                                 "password": user.password,
                                 "email": user.email,
                                 "role_id": user.role_id}
            res = {"codigo": 1,
                   "status": "Role cambiado",
                   "usuario": user_account_json}

        else:
            res = {"codigo": 2,
                   "status": "Role incorrecto, no existe tal role",
                   "usuario": None}
    else:
        res = {"codigo": 0,
               "status": "Id de usuario incorrecta, no existe en la base de datos",
               "usuario": None}

    return jsonify(res)


if __name__ == '__main__':
    app.run()
