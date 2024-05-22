# Luminite V2 API
Live Swagger UI endpoint
[LuminiteV2 Swagger UI](https://luminitev2-production.up.railway.app/api/docs)

Live Redoc Api endpoint
[LuminiteV2 Redoc](https://luminitev2-production.up.railway.app/)

## Description
### Scalable Multivendor RESTful E-commerce API

This project is a scalable Multivendor E-commerce web application built with modern technologies, designed for performance, security, and efficient deployment.

**Tech Stack:**

-   **Backend:** Django REST Framework (DRF) provides a robust foundation for API development.
-   **Authentication:** Secure JWT-based user authentication ensures data protection.
-   **Background Tasks:** Celery handles asynchronous tasks like email sending and invoice generation, improving responsiveness.
-   **Testing:** Test-Driven Development (TDD) with pytest guarantees code quality through comprehensive unit testing.
-   **Deployment:** Docker Compose enables containerized deployment for efficient scaling and maintainability.
-   **Load Balancing:** Nginx acts as a Reverse Proxy for high availability and traffic distribution.

## Getting started

Before go any further Please ``example.env``  file to ``.env`` 

To start this project, Run:

```
docker-compose up --build -d
```

To observe the Django server logs

```
docker-compose logs web3 --follow
```
Testing

```
docker-compose exec web3 pytest
```

### Access Api
You can access this API by your Host Machine with [http://127.0.0.1:8000](http://127.0.0.1:8000)
