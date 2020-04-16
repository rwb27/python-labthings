import pytest

from labthings.server.view import builder


def test_property_of(app, client):
    obj = type("obj", (object,), {"property_name": "propertyValue"})

    GeneratedClass = builder.property_of(obj, "property_name")
    app.add_url_rule("/", view_func=GeneratedClass.as_view("index"))

    with client as c:
        assert c.get("/").data == b"propertyValue"
        assert c.post("/", data=b"newPropertyValue").data == b"newPropertyValue"
        assert c.get("/").data == b"newPropertyValue"


def test_property_of_dict(app, client):
    obj = type(
        "obj",
        (object,),
        {
            "properties": {
                "property_name": "propertyValue",
                "property_name_2": "propertyValue2",
            }
        },
    )

    GeneratedClass = builder.property_of(obj, "properties")
    app.add_url_rule("/", view_func=GeneratedClass.as_view("index"))

    with client as c:
        assert (
            c.get("/").data
            == b'{"property_name":"propertyValue","property_name_2":"propertyValue2"}\n'
        )
        assert (
            c.put("/", json={"property_name": "newPropertyValue"}).data
            == b'{"property_name":"newPropertyValue","property_name_2":"propertyValue2"}\n'
        )
        assert (
            c.post("/", json={"property_name": "newPropertyValue"}).data
            == b'{"property_name":"newPropertyValue"}\n'
        )


def test_property_of_readonly():
    obj = type("obj", (object,), {"property_name": "propertyValue"})

    GeneratedClass = builder.property_of(obj, "property_name", readonly=True)

    assert callable(GeneratedClass.get)
    assert not hasattr(GeneratedClass, "post")


def test_property_of_name_description():
    obj = type("obj", (object,), {"property_name": "propertyValue"})
    GeneratedClass = builder.property_of(
        obj, "property_name", name="property_name", description="property description"
    )

    assert GeneratedClass.__apispec__.get("description") == "property description"
    assert GeneratedClass.__apispec__.get("summary") == "property description"


def test_action_from(app, client):
    def f(arg: int, kwarg: str = "default"):
        return {"arg": arg, "kwarg": kwarg}

    GeneratedClass = builder.action_from(f)
    app.add_url_rule("/", view_func=GeneratedClass.as_view("index"))

    with client as c:
        assert c.post("/", json={"arg": 5}).data == b'{"arg":5,"kwarg":"default"}\n'


def test_action_from_task(app, client):
    def f(arg: int, kwarg: str = "default"):
        return {"arg": arg, "kwarg": kwarg}

    GeneratedClass = builder.action_from(f, task=True,)
    app.add_url_rule("/", view_func=GeneratedClass.as_view("index"))

    with client as c:
        response = c.post("/", json={"arg": 5}).json
        # Check we get back a Task representation
        assert isinstance(response, dict)
        assert isinstance(response.get("id"), str)
        assert isinstance(response.get("function"), str)


def test_action_from_options(app):
    def f(arg: int, kwarg: str = "default"):
        return {"arg": arg, "kwarg": kwarg}

    assert builder.action_from(
        f,
        name="action_name",
        description="action_description",
        safe=True,
        idempotent=True,
    )


def test_static_from(app, client, app_ctx, static_path):

    GeneratedClass = builder.static_from(static_path,)
    app.add_url_rule("/static", view_func=GeneratedClass.as_view("index"))

    with app_ctx.test_request_context():
        assert GeneratedClass().get("text").status_code == 200

    with client as c:
        assert c.get("/static/text").data == b"text"


def test_static_from_options(app, app_ctx, static_path):
    assert builder.static_from(static_path, name="static_name")
