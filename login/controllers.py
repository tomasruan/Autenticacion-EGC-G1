from database import db, TableNameExample, TableNameExampleSchema
from database import Cookie, CookieSchema, User_account
from flask import request
from flask.json import jsonify
from flask import Flask, redirect, url_for


app = Flask(__name__)

#Example of how to add something to database
@app.route('/add')
def add():
    schema = TableNameExampleSchema()

    prueba = TableNameExample(title='Titulo')

    db.session.add(prueba)
    db.session.commit()

    return schema.dump(prueba).data


#Example of how to retrieve a table from database and return it as json
@app.route('/prueba')
def root():
    prueba_schema = TableNameExampleSchema(many=True)
    prueba = TableNameExample.query.all()

    return prueba_schema.dump(prueba).data

# @app.route('/addCookie')
# def addCookieTest():
#     cookieSchema = CookieSchema()
#
#     cookieTest = Cookie(number_id=2147483647,user_account_id=3)
#
#     db.session.add(cookieTest)
#     db.session.commit()


@app.route('/cookie/<int:number_id>')
def check_cookies(number_id):
    cookie_id = number_id
    cookie_schema = CookieSchema(many=True)
    cookie_db = Cookie.query.get(cookie_id)
    if cookie_db is not None:

        user_account_db=User_account.query.get(cookie_db.user_account_id)
        user_account_dict={"id":user_account_db.id,
                           "username":user_account_db.username,
                           "password":user_account_db.password,
                           "email":user_account_db.email,
                           "role_id":user_account_db.role_id}
        res= {"codigo":1,
              "status":"Cookie valida y existente en la base de datos",
              "usuario":user_account_dict,}
    else:
        res= {"codigo":0,
              "status":"Cookie Incorrecta, no existe en la base de datos",
              "usuario":None,}
    return jsonify(checkCookie=res)

if __name__ == '__main__':
    app.run()