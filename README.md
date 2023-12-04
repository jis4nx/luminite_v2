# Luminite V2 API

## Description
### An E-Commerce RESTful API, built on top of Django Rest Framework 


Live Swagger UI endpoint
[LuminiteV2 Swagger UI](https://luminitev2-production.up.railway.app/api/docs)

Live Redoc Api endpoint
[LuminiteV2 Redoc](https://luminitev2-production.up.railway.app/)

## Getting started

To start this project, Run:

```
docker-compose up -d
```

To observe the Django server logs

```
docker logs web --follow
```
Testing

```
docker exec web pytest
```

### Access Api
You can access this API by your Host Machine with [http://127.0.0.1:8000](http://127.0.0.1:8000)
