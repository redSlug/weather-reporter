
# Messages API

An API for messages

- POST api/message
    - JSON payload with message, user

## Setup

- `python3 app.py`
- `/etc/supervisor/conf.d/weather-reporter.conf`
- `/etc/nginx/sites-available/weather-reporter`
- [infra stuff](https://docs.google.com/presentation/d/1g8D7R-jyDUReKxFoGk_zN5-uWEcSOi6rIvGGKv4PAVI/edit#slide=id.g3d18660b80_0_10)

## After adding new dependencies
- `source  /home/bd/.virtualenvs/venv/bin/activate`
- `pip install -r requirements.txt`

## Useful Commands
`sudo supervisorctl start weather-reporter`

`curl --header "Content-Type: application/json" --request POST --data '{"message":"hey!","author":"me"}' http://localhost:5000/matrix/api/message`

`curl  http://localhost:5000/matrix/api/message`

`alembic revision --autogenerate -m "add author field to message"`

`alembic upgrade head`

`alembic downgrade -1`

`sqlite3 db`

