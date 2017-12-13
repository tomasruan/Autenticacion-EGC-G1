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

@app.route('/users/<int:user_id>/role', methods=['PATCH'])
def assign_role(user_id):
    user = User_account.query.get(user_id)
    if user is not None:
        if request.json.get('role_id') == 1 | 2:
            user.role_id = request.json.get('role_id')
            print(request.json.get('role_id'))
            print(user.role_id)
            res = {"codigo":1,
                "status":"Role cambiado",
                "usuario":user,}
    else:
        res = {"codigo":0,
            "status":"Id de usuario incorrecta, no existe en la base de datos",
            "usuario":None,}
    return jsonify(user = res)

if __name__ == '__main__':
    app.run()