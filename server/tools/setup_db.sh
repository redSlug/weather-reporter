#!/bin/bash


docker run --name prod \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_USER=user \
    -e POSTGRES_DB=prod \
    -p 5432:5432 \
    -d postgres


echo "PGUSER=user PGPASSWORD=pass psql -h localhost -p 5432 prod"

sleep 1


SQLALCHEMY_URL='postgresql://user:pass@localhost:5432/prod' alembic upgrade head