
# Messages API

An API for messages

- POST api/message
    - JSON payload with message, user

## Setup

- `python3 app.py`

## Useful Commands

`curl --header "Content-Type: application/json" --request POST --data '{"message":"hey!","author":"me"}' http://localhost:5000/matrix/api/message`

`curl  http://localhost:5000/matrix/api/message`

`alembic revision --autogenerate -m "add author field to message"`

`alembic upgrade head`

`alembic downgrade -1`

`sqlite3 db`
