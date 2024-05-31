
# `Dotaverse`

Dotaverse is a free web service for predicting Dota 2 pro match results based on open stats.
___

## *Project Status*

***Completed v0.0.1 &#10003;***
___
## Functionality
- Database [models](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/model)
- Alembic [migrations](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/migration)
- Celery [worker](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/celery)
- FastAPI [routing](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/router)
- Pydantic [schemas](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/schema)
- Parsing/DB/Redis [services](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/service)
- Most used [utils](https://github.com/Segfaul/dotaverse/tree/3cdf5692221e116a4048fac5fa58d767e991febd/backend/api/util)
- React [GA](https://github.com/Segfaul/dotaverse/blob/3cdf5692221e116a4048fac5fa58d767e991febd/frontend/src/main.tsx) & [i18n](https://github.com/Segfaul/dotaverse/blob/3cdf5692221e116a4048fac5fa58d767e991febd/frontend/src/components/plugin/i18n.ts) modules
- Docker compose [.dev](https://github.com/Segfaul/dotaverse/blob/3cdf5692221e116a4048fac5fa58d767e991febd/docker-compose.dev.yml) & [.prod](https://github.com/Segfaul/dotaverse/blob/3cdf5692221e116a4048fac5fa58d767e991febd/docker-compose.prod.yml)
- Github actions [CI/CD pipeline](https://github.com/Segfaul/dotaverse/blob/3cdf5692221e116a4048fac5fa58d767e991febd/.github/workflows/ci.yml)

## Technologies and Frameworks
- [Python 3.11.6](https://www.python.org/downloads/release/python-3116/)
- [FastAPI 0.108](https://fastapi.tiangolo.com/)
- [Uvicorn 0.25.0](https://www.uvicorn.org/settings/)
- [Gunicorn 22.0.0](https://docs.gunicorn.org/en/stable/settings.html)
- [SQLAlchemy 2.0.25](https://docs.sqlalchemy.org/en/20/)
- [Alembic 1.13.1](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic 2.5.3](https://docs.pydantic.dev/latest/)
- [Celery 5.3.6](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
- Redis 7.2.5
- RabbitMQ 3.13.2
- PostgreSQL 16
- Node 18.19.1
- Vite 4.4.5
- React 18.2.0
- TypeScript 5.0.2
- Docker 26.1.3
- Docker Compose 2.27.0
- [Pytest 8.1.1](https://doc.pytest.org/en/latest/announce/release-8.1.1.html)
- Nginx 1.25
- Certbot
- CI/CD
___

## Development

1. Clone the repository to the local machine

    ```shell
    git clone https://github.com/Segfaul/dotaverse.git
    ```

2. Specify .env (**DEBUG=False** to use PostgreSQL, **SECRET_KEY** for JWT AUTH)

    ```shell
    # Global .env (DEBUG, SECRET_KEY)
    cp .env.example .env
    nano .env

    # Frontend .env (GA_KEY, BACKEND_URL)
    cp frontend/.env.example frontend/.env
    nano frontend/.env
    ```

3. Build images and run app in dev mode

    ```shell
    docker compose -f docker-compose.dev.yml up -d --build
    ```

4. Checkout http://127.0.0.1:3000 (Vite), http://127.0.0.1:8000 (Uvicorn)
    
    ```shell
    # Also add new admin user to your app
    docker exec -it dotaverse_app_dev-backend-1 bash
    python -m backend.config.admin --username admin --password password
    Admin ${username} created successfully.
    exit
    ```

5. Stop/Down the app

    ```shell
    # Without removing containers
    docker compose -f docker-compose.dev.yml stop

    # Removing containers
    docker compose -f docker-compose.dev.yml down

    # Removing containers and docker volumes (not local ones)
    docker compose -f docker-compose.dev.yml down -v
    ```
___

## Production

1. Specify .env

    ```shell
    # Force to use PostgreSQL
    DEBUG=False
    ...
    # Specify proxy to run background tasks for parsing data
    PROXY='http://login:paswword@ip:port'
    ...
    # Specify postgres db_name and db_password
    POSTGRES_DB='dotaverse'
    POSTGRES_USER='postgres'
    POSTGRES_PASSWORD='password'
    POSTGRES_HOST='127.0.0.1'
    POSTGRES_PORT=5432
    ...
    # Specify origins & server params for your own domain
    ALLOWED_ORIGINS='http://localhost:3000,http://127.0.0.1:3000'
    SERVER_NAME=localhost.localdomain
    SERVER_EMAIL=example@example.com
    ```

2. Specify nginx.conf

    ```shell
    # Nginx root for ssl_certificate doesn't support .env variables
    nano nginx/nginx.conf

    # Specify those roots strictly with your server_name
    ssl_certificate /etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${SERVER_NAME}/privkey.pem;

    # Example
    ssl_certificate /etc/letsencrypt/live/lhost.ldomain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lhost.ldomain/privkey.pem;
    ```

3. Build images and run app in prod mode

    ```shell
    docker compose -f docker-compose.prod.yml up -d --build
    ```

4. Open ${SERVER_NAME} in your browser

    ```shell
    # In case of any issues also checkout logs
    cat logs-data/dotaverse.log | tail -15
    ```

5. Stop/Down the app

    ```shell
    # Without removing containers
    docker compose -f docker-compose.dev.yml stop

    # Removing containers
    docker compose -f docker-compose.dev.yml down

    # Removing containers and docker volumes (not local ones)
    docker compose -f docker-compose.dev.yml down -v
    ```
___