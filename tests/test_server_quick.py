
from labthings.server import quick

from flask import Flask
from labthings.server.labthing import LabThing


def test_create_app():
    app, labthing = quick.create_app(__name__)
    assert isinstance(app, Flask)
    assert isinstance(labthing, LabThing)


def test_create_app_options():
    app, labthing = quick.create_app(
        __name__, flask_kwargs={"static_url_path": "/static"}, handle_cors=False
    )
    assert isinstance(app, Flask)
    assert isinstance(labthing, LabThing)
