FROM python:3

ENV FLASK_APP=chat.py
ENV FLASK_ENV=development

COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY . /src

WORKDIR /src

CMD ["flask", "run", "--host", "0.0.0.0"]
