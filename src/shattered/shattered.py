import logging
import time

import stomp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShatteredListener(stomp.ConnectionListener):
    def __init__(self, app):
        self.app = app

    def on_connected(self, headers, body):
        logger.info("STOMP connection established")
        for destination in self.app.subscriptions:
            self.app.conn.subscribe(destination, 1)

    def on_message(self, headers, body):
        logger.info("STOMP message received")
        destination = headers["destination"]
        for callback in self.app.subscriptions[destination]:
            callback(headers, body, self.app.conn)


class Shattered:
    subscriptions = {}
    conn = None

    def __init__(self, **config):
        self.config = config

    def add_subscription(self, destination, callback):
        if destination not in self.subscriptions:
            self.subscriptions[destination] = []
        self.subscriptions[destination].append(callback)

    def subscribe(self, destination):
        def decorator(callback):
            self.add_subscription(destination, callback)
            return callback

        return decorator

    def run(self):
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 61613)
        username = self.config.get("username", "guest")
        password = self.config.get("password", "guest")
        vhost = self.config.get("vhost", "/")
        self.conn = stomp.Connection(
            [(host, port)], vhost=vhost, heartbeats=(10000, 10000)
        )
        self.conn.set_listener("shattered", ShatteredListener(self))
        self.conn.connect(username, password, wait=True)
        while True:
            time.sleep(60)
