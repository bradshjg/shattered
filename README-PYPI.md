# Shattered

STOMP meets `bottle.py`

[![Build Status](https://travis-ci.com/bradshjg/shattered.svg?branch=master)](https://travis-ci.com/bradshjg/shattered)

## Getting Started

### Installation

`pip install shattered`

### CLI

`shattered run` will run a Shattered app, using one of the following (in order):

1. The `--app` flag.
2. The `SHATTERED_APP` environment variable.
3. `app.py` as the application module name.

Use `shattered config` to see the current configuration (same app resolution as `run` command).

### Echo Server

`app.py`

```python
import logging

from shattered import Shattered


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Shattered(host="rabbitmq")


@app.subscribe("/queue/echo")
def echo(headers, body, conn):
    logger.info("%s %s", headers, body)


@app.subscribe("/queue/echo")
def echo_fancy(headers, body, conn):
    logger.info("✨✨✨%s %s✨✨✨", headers, body)


app.run()
```

#### Running the Demo

Start up RabbitMQ using `docker-compose up`

In another shell, run `docker-compose run shattered python examples/echo/echo.py`

In another shell, run `docker-compose run shattered python examples/echo/send.py`
