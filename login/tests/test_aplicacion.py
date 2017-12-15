# test_app.py
import pytest
from flask import url_for,Flask
from database import *


def test_incorrect_cookie(client):
    res = client.get(url_for('check_cookies',number_id="65416846684"))
    assert res.status_code == 200
    assert res.json == {"codigo": 0,
           "status": "Cookie Incorrecta, no existe en la base de datos",
           "usuario": None}


def test_correct_cookie(client):
    old=Cookie.query.get("2147483647")
    if(old is not None):
        db.session.delete(old)
        db.session.commit()
    cookieTest = Cookie(number_id=2147483647,user_account_id=3)
    db.session.add(cookieTest)
    db.session.commit()
    cookie_db = Cookie.query.get("2147483647")
    user_account_db = User_account.query.get(cookie_db.user_account_id)
    user_account_dict = {"id": user_account_db.id,
                         "username": user_account_db.username,
                         "password": user_account_db.password,
                         "email": user_account_db.email,
                         "role_id": user_account_db.role_id}

    res = client.get(url_for('check_cookies',number_id="2147483647"))
    assert res.status_code == 200
    assert res.json == {"codigo": 1,
           "status": "Cookie valida y existente en la base de datos",
           "usuario": user_account_dict}




































