#!/bin/bash


docker run --name prod \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_USER=usr \
    -e POSTGRES_DB=prod \
    -p 5432:5432 \
    -d postgres


echo "PGUSER=usr PGPASSWORD=pass psql -h localhost -p 5432 prod"

sleep 1


SQLALCHEMY_URL='postgresql://usr:pass@localhost:5432/prod' alembic upgrade head