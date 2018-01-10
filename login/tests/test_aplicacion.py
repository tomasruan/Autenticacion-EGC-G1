from flask import url_for, request
from database import Cookie, User_account, db
import json


def test_incorrect_cookie(client):
    res = client.get(url_for('check_cookies', number_id="65416846684"))
    assert res.status_code == 200
    assert res.json == {"codigo": 0,
                        "status": "Cookie Incorrecta, no existe en la base de datos",
                        "usuario": None}


def test_correct_cookie(client):
    cookie_db = Cookie.query.get("2147483647")
    user_account_db = User_account.query.get(cookie_db.user_account_id)
    user_account_dict = {"id": user_account_db.id,
                         "username": user_account_db.username,
                         "password": user_account_db.password,
                         "email": user_account_db.email,
                         "role_id": user_account_db.role_id}

    res = client.get(url_for('check_cookies', number_id="2147483647"))
    assert res.status_code == 200
    assert res.json == {"codigo": 1,
                        "status": "Cookie valida y existente en la base de datos",
                        "usuario": user_account_dict}


def test_incorrect_user(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "role_id": 1
    }
    url = '/users/65416846684/role'

    response = client.put(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert response.json == {"codigo": 0,
                             "status": "Id de usuario incorrecta, no existe en la base de datos",
                             "usuario": None}


def test_incorrect_role(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "role_id": 3
    }
    url = '/users/1/role'

    response = client.put(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert response.json == {"codigo": 2,
                             "status": "Role incorrecto, no existe tal role",
                             "usuario": None}

def test_all_correct(client):
    user = User_account.query.filter_by(id=1).first()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "role_id": 1
    }
    url = '/users/1/role'

    response = client.put(url, data=json.dumps(data), headers=headers)

    user_account_json = {"id": user.id,
                         "username": user.username,
                         "password": user.password,
                         "email": user.email,
                         "role_id": user.role_id}

    assert response.status_code == 200
    assert response.json == {"codigo": 1,
                             "status": "Role cambiado",
                             "usuario": user_account_json}





def test_logout_user(client):

    client.get(url_for('defineSessionTest_logout_user'))
    numeroCookies = db.session.query(Cookie).count()

    cookie=request.cookies.get('session_id')
    client.get(url_for('logout_user'))
    numeroCookies1 = db.session.query(Cookie).count()
    assert numeroCookies == (numeroCookies1 + 1)

