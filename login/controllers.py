from database import db, TableNameExample, TableNameExampleSchema
from flask import Flask, redirect, url_for
from database import Role, RoleSchema, User_account
from flask.json import jsonify
from flask import request


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

@app.route('/users/<int:user_id>/role', methods=['PUT'])
def assign_role(user_id):
    user = User_account.query.filter_by(id=user_id).first()
    new_role = request.json.get('role_id')
    if user is not None:
        if new_role in (1,2):
            user.role_id = new_role
            db.session.commit()
            user_account_json = {"id": user.id,
                                 "username": user.username,
                                 "password": user.password,
                                 "email": user.email,
                                 "role_id": user.role_id}
            res = {"codigo":1,
                "status":"Role cambiado",
                "usuario":user_account_json,}
        else:
            res = {"codigo": 2,
                   "status": "Role incorrecto, es diferente de 1 o 2",
                   "usuario": None, }
    else:
        res = {"codigo":0,
            "status":"Id de usuario incorrecta, no existe en la base de datos",
            "usuario":None,}
    return jsonify(res)

if __name__ == '__main__':
    app.run()