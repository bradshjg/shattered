import logging

from shattered import Shattered

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

shattered_app = Shattered(host="rabbitmq")


@shattered_app.subscribe("/queue/test")
@shattered_app.subscribe("/topic/test")
@shattered_app.subscribe("/topic/bunny")
def echo(headers, body, conn):
    logger.info(body)
