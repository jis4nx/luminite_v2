FROM python:3.10.9-alpine3.17

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev linux-headers pango libffi

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /media
RUN mkdir -p /static

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . .
CMD ["gunicorn", "LuminiteV2.wsgi:application", "--bind", "0.0.0.0:8000"]
ENTRYPOINT ["/app/entrypoint.sh"]
