FROM python:3.10.2-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get -y update \
    && apt-get install -y \
    python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
    && apt-get -y clean

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "manage.py", "runserver"]

