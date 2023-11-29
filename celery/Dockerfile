FROM python:3.10.9-alpine3.17

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev linux-headers pango libffi

COPY ./requirements.txt .

RUN pip install -r requirements.txt
