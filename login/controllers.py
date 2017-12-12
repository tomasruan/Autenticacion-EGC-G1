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

@app.route('/assignRole/<int:id>/<int:role_id>')
def assign_role(id, role_id):
    roleNumber_id = role_id
    users = User_account.query.all()
    print(len(users))
    user = User_account.query.get(id)
    if user is not None:
        user.role_id = roleNumber_id
        db.session.commit()
        user_account_assigned={"id":user.id,
                           "username":user.username,
                           "password":user.password,
                           "email":user.email,
                           "role_id":roleNumber_id}
        res= {"codigo":1,
              "status":"Role cambiado",
              "usuario":user_account_assigned,}
    else:
        res= {"codigo":0,
              "status":"Id de usuario incorrecta, no existe en la base de datos",
              "usuario":None,}
    return jsonify(assignRole=res)

if __name__ == '__main__':
    app.run()