import pytest
from controllers import app as _app
from database import db
from database import Cookie





@pytest.fixture(scope='session')
def app():
    _app.debug = True


    with _app.app_context():
        #Aquí lo que se quiera añadir a la base de datos

        #cookie2 = Cookie.query.get(2147483647)
        #db.session.delete(cookie2)

        cookie = Cookie(number_id='2147483647', user_account_id=1)
        db.session.add(cookie)
        db.session.commit()

        yield _app
