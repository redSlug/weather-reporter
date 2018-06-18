
# Messages API

An API for messages

- POST api/message
    - JSON payload with message, user

## Setup

- install docker
- `./tools/setup_db.sh` *you might have to run this twice if you see an error
- `python app.py`

## Useful Commands

`curl --header "Content-Type: application/json" --request POST --data '{"message":"hey!","author":"me"}' http://localhost:5000/matrix/api/message`

`curl  http://localhost:5000/matrix/api/message`

`alembic revision --autogenerate -m "add author field to message"`

`alembic upgrade head`

`alembic downgrade -1`

`PGUSER=usr PGPASSWORD=pass psql -h localhost -p 5432 prod`
