import logging

from shattered import Shattered


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Shattered(host="rabbitmq")


@app.subscribe("/queue/echo")
def echo(headers, body, conn):
    logger.info("Message headers: %s", headers)
    logger.info("Message body: %s", body)
    logger.info("Connection: %s", conn)


@app.subscribe("/queue/echo")
def echo_fancy(headers, body, conn):
    logger.info("%s %s", headers, body)


app.run()
