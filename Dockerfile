FROM python:alpine3.18

WORKDIR /app

COPY ./requirements.txt .

RUN apk add --update --no-cache gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev && \
  pip install --no-cache-dir -r requirements.txt && \
  apk del gcc musl-dev && \
  adduser -D docker01

COPY . /app

USER docker01

CMD ["python", "manage.py", "runserver"]
