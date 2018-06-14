
# Messages API

An API for messages

- POST api/message
    - JSON payload with message, user

## Setup

- install docker
- `./tools/setup_db.sh` *you might have to run this twice if you see an error
- `python app.py`

## Useful Commands

`curl --header "Content-Type: application/json" --request POST --data '{"email":"happy@happy.com","first_name":"Happy"}' http://localhost:5000/api/loyalty/create_new_user`

`curl --header "Content-Type: application/json" --request POST --data '{"user_id":"5","amount":"1000"}' http://localhost:5000/api/loyalty/create_new_transfer`

`curl http://localhost:5000/api/loyalty/user/5/transfers`

`alembic revision --autogenerate -m "Add users and transfers tables"`

`alembic upgrade head`

`alembic downgrade -1`

`PGUSER=usr PGPASSWORD=pass psql -h localhost -p 5432 prod`
