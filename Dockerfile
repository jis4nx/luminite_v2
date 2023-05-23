FROM python:alpine3.18

WORKDIR /app

COPY ./requirements.txt .

RUN apk add --update gcc libc-dev postgresql-dev musl-dev && \
    pip install -r requirements.txt && \
    apk del gcc musl-dev

COPY . /app

CMD ["python", "manage.py", "runserver"]

