#Builder Stage
FROM python:3.10.9-alpine3.17 as builder

COPY ./requirements.txt .

RUN apk add --update --virtual .tmp-build-deps \
	postgresql-dev gcc python3-dev musl-dev  font-inconsolata font-noto

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Final Stage
FROM python:3.10.9-alpine3.17

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/share/fonts/ /usr/share/fonts/

RUN mkdir /app
WORKDIR /app

COPY ./entrypoint.sh .

RUN sed -i 's/\r$//g' /app/entrypoint.sh && \
	chmod +x /app/entrypoint.sh

COPY . .

RUN apk add pango libffi

RUN adduser -D django
RUN getent group django || addgroup django
RUN addgroup django django

RUN chown -R django:django .
USER django

CMD ["gunicorn", "LuminiteV2.wsgi:application", "--bind", "0.0.0.0:8000"]
ENTRYPOINT ["/app/entrypoint.sh"]
