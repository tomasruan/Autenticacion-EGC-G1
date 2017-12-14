from database import db, Cookie, Role, User_account
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask.json import jsonify
from passlib.hash import phpass
from random import randint

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        cookie = Cookie.query.filter_by(number_id=request.cookies.get('session_id')).first()

        if cookie is None:
            return render_template('login.html')
        else:
            return redirect('/')

    elif request.method == 'POST':
        #Comprobar que no son vacios
        form_username = request.form['username']
        form_password = request.form['password']

        user_from_db = User_account.query.filter_by(username=form_username).first()

        if user_from_db is not None:
            if phpass.verify(form_password, user_from_db.password):
                saved_cookie = create_cookie_and_save(user_from_db)

                response = make_response(redirect('/'))
                response.set_cookie('session_id', value=str(saved_cookie.number_id))

                return response
            else:
                return render_template('login.html', error='La contraseña no coincide con la del usuario')
        else:
            return render_template('login.html', error='No existe el usuario')


def create_cookie_and_save(user):
    number_id = random_with_n_digits(7)
    cookie = Cookie(number_id=number_id, user_account_id=user.id)

    db.session.add(cookie)
    db.session.commit()

    return cookie


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


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

    return redirect(url_for('login'))


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
