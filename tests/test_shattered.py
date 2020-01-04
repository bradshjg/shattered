from unittest.mock import call

import pytest

from shattered.shattered import Shattered, ShatteredListener


trap_call = None


@pytest.fixture
def app():
    app = Shattered()

    @app.subscribe("foo")
    def foo(headers, body, conn):
        return "foo"

    @app.subscribe("foo")
    def bar(headers, body, conn):
        return "bar"

    @app.subscribe("bar")
    def baz(headers, body, conn):
        global trap_call
        trap_call = "baz"
        return "baz"

    return app


def test_default_connection(app, mocker):
    mock_conn = mocker.patch("shattered.shattered.stomp.Connection")
    app._run()
    mock_conn.assert_called_once_with(
        [("localhost", 61613)], vhost="/", heartbeats=(10000, 10000)
    )


def test_set_listener(app, mocker):
    mock_conn = mocker.patch("shattered.shattered.stomp.Connection")
    app._run()
    mock_conn.return_value.set_listener.assert_called_once()


def test_default_connect(app, mocker):
    mock_conn = mocker.patch("shattered.shattered.stomp.Connection")
    app._run()
    mock_conn.return_value.connect.assert_called_once_with("guest", "guest", wait=True)


def test_subscriptions(app):
    assert len(app.subscriptions) == 2

    assert len(app.subscriptions["foo"]) == 2
    assert callable(app.subscriptions["foo"][0])
    assert app.subscriptions["foo"][0].__name__ == "foo"
    assert callable(app.subscriptions["foo"][1])
    assert app.subscriptions["foo"][1].__name__ == "bar"

    assert len(app.subscriptions["bar"]) == 1
    assert callable(app.subscriptions["bar"][0])
    assert app.subscriptions["bar"][0].__name__ == "baz"


def test_listener_on_connected_subscribes(app, mocker):
    mock_conn = mocker.patch("shattered.shattered.stomp.Connection")
    app._run()
    assert app.conn.subscribe.mock_calls == []
    app.listener.on_connected({}, "")
    assert app.conn.subscribe.mock_calls == [call("foo", 1), call("bar", 1)]


def test_listener_on_message(app, mocker):
    global trap_call
    trap_call = None
    mock_conn = mocker.patch("shattered.shattered.stomp.Connection")
    app._run()
    assert trap_call is None
    app.listener.on_message({"destination": "bar"}, "")
    assert trap_call == "baz"
