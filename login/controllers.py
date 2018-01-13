from database import db, Cookie, Role, User_account
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask.json import jsonify
from passlib.hash import phpass
from random import randint
import hashlib
import random
import copy


app = Flask(__name__)
db.init_app(app)

def get_random_operation():
    ops = {'+', '-', '*'}
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(list(ops))
    captcha = str(num1) + op + str(num2)
    return captcha

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        captcha = get_random_operation()
        cookie = Cookie.query.filter_by(number_id=request.cookies.get('session_id')).first()
        if cookie is None:
            return render_template('login.html',captcha=captcha)
        else:
            return redirect('https://g1admvotes.egc.duckdns.org/')

    elif request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        form_captcha  = request.form['captcha']
        form_captcha_saved = request.form['captcha_saved']

        if not validate(form_username, form_password,form_captcha):
            return render_template('login.html',captcha=form_captcha_saved,error='No deje ningún campo en blanco')

        user_from_db = User_account.query.filter_by(username=form_username).first()
        try:
            eval(form_captcha)
            print(eval(form_captcha))
            if(eval(form_captcha) !=eval(form_captcha_saved)):
                return render_template('login.html',captcha=form_captcha_saved, error='Error en el captcha, revise la operación')
        except:
            return render_template('login.html', captcha=form_captcha_saved, error='Error en el captcha, revise la operación')
        if user_from_db is not None:
            if phpass.verify(form_password, user_from_db.password):
                saved_cookie = create_cookie_and_save(user_from_db)

                response = make_response(redirect('https://g1admvotes.egc.duckdns.org/'))
                response.set_cookie('session_id', value=str(saved_cookie.number_id))

                return response
            else:
                return render_template('login.html',captcha=form_captcha_saved ,error='La contraseña no coincide con la del usuario')
        else:
            return render_template('login.html', captcha=form_captcha_saved,error='No existe el usuario')


def create_cookie_and_save(user):
    random_number = random_with_n_digits(15)
    number_id_unhashed = (user.username*4) + str(random_number) + user.password

    hasher = hashlib.sha1()
    hasher.update(number_id_unhashed.encode())

    number_id = hasher.hexdigest()

    cookie = Cookie.query.filter_by(user_account_id=user.id).first()

    if not cookie:
        cookie = Cookie(number_id=number_id, user_account_id=user.id)
        db.session.add(cookie)
        db.session.commit()
    else:
        cookie.number_id = number_id
        db.session.commit()

    return cookie


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def validate(*params):
    for parameter in params:
        if not parameter:
            return False

    return True


@app.route('/cookies/<string:number_id>')
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


@app.route('/logout/')
def logout_user():
    cookie=Cookie.query.get(request.cookies.get('session_id'))

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

@app.route("/defineSessionTest_logout_user")
def defineSessionTest_logout_user():
    response=make_response('Setting cookie')
    response.set_cookie('session_id', '2147483647')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='52000')
