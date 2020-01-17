FROM python:slim

ENV SHATTERED_APP=logger.py

COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY . /src

WORKDIR /src

CMD ["shattered", "run"]
