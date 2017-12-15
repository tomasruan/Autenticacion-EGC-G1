import pytest
from flask import Flask
from controllers import get_app

@pytest.fixture
def app(request):
    app=get_app()
    app.debug = True
    return app
