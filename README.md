# Trackfolio (in development)
Web application to track your portfolio in Tinkoff Investments.

Libraries planned for use: alembic, sqlalchemy, fastapi-users, fastapi-cache, celery, redis, jinja.

## Notes
- created endpoints for user registration and authentication

## Todo
- create templates for auth: login
- add tests for auth: login, update, delete

## Technologies stack
- Fast-API (python web framework)
- Poetry (python packaging and dependency manager)
- postgreSQL (database)
- Uvicorn (HTTP server)
- Docker (container virtualization)
- fastapi-users (user authentication)
- pytest (testing)
- redis (query caching)
- celery + redis (background tasks)

## Deployment

To start the database services for local development, you need to run the following command:

```
make up
```

To apply migrations you need to run the following command in the terminal:

```
alembic upgrade head
```

To start in Poetry shell you may use command

```
start
```
