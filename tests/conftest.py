import pytest
import os
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from labthings.server.labthing import LabThing
from labthings.server.view import View


@pytest.fixture
def view_cls():
    class ViewClass(View):
        def get(self):
            pass

        def post(self):
            pass

        def put(self):
            pass

        def delete(self):
            pass

    return ViewClass


@pytest.fixture
def spec():
    return APISpec(
        title="Python-LabThings PyTest",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()],
    )


@pytest.fixture()
def app(request):

    app = Flask(__name__)
    app.config["TESTING"] = True

    # pushes an application context manually
    ctx = app.app_context()
    ctx.push()

    # bind the test life with the context through the
    request.addfinalizer(ctx.pop)
    return app


@pytest.fixture
def thing(app):
    thing = LabThing(app)
    with app.app_context():
        return thing


@pytest.fixture()
def debug_app(request):

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.debug = True

    # pushes an application context manually
    ctx = app.app_context()
    ctx.push()

    # bind the test life with the context through the
    request.addfinalizer(ctx.pop)
    return app


@pytest.fixture()
def app_ctx(app):
    with app.app_context():
        yield app


@pytest.fixture()
def app_ctx_debug(debug_app):
    with debug_app.app_context():
        yield debug_app


@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def static_path(app):
    return os.path.join(os.path.dirname(__file__), "static")


@pytest.fixture
def schemas_path(app):
    return os.path.join(os.path.dirname(__file__), "schemas")
