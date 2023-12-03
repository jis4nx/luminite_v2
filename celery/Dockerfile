FROM python:3.10.9-alpine3.17

COPY --from=luminite:web /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=luminite:web /usr/local/bin/ /usr/local/bin/


RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add pango libffi

COPY . . 

RUN adduser -D celery
RUN getent group celery || addgroup celery
RUN addgroup celery celery

RUN chown -R celery:celery .
USER celery
