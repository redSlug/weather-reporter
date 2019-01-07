
# Messages API

An API for messages

- POST api/message
    - JSON payload with message, user

## Setup
- `python3 app.py`
- add `supervisord.conf` contents to  `/etc/supervisor/supervisord.conf`
- populate `/etc/nginx/sites-available/weather-reporter` with `sample_weather-reporter`
- [infra stuff](https://docs.google.com/presentation/d/1g8D7R-jyDUReKxFoGk_zN5-uWEcSOi6rIvGGKv4PAVI/edit#slide=id.g3d18660b80_0_10)

## After adding new dependencies
- `source  /home/bd/.virtualenvs/venv/bin/activate`
- `pip install -r requirements.txt`

## Useful Commands
`sudo supervisorctl start weather-reporter`

`systemctl status weather-reporter`

`curl --header "Content-Type: application/json" --request POST --data '{"message":"hey!","author":"me"}' http://localhost:5000/matrix/api/message`

`curl  http://localhost:5000/matrix/api/message`

`alembic revision --autogenerate -m "add author field to message"`

`alembic upgrade head`

`alembic downgrade -1`

`sqlite3 db`


# Troubleshooting

## weather-reporter.service not found
Loaded: not-found (Reason: No such file or directory)
Active: inactive (dead)

`sudo supervisorctl reread`
`sudo supervisorctl update`
`sudo supervisorctl start weather-reporter`

## 502 Bad Gateway nginx/1.10.3 (Ubuntu)

`mkdir -p ~/sites/weather-reporter/logs/nginx`
`sudo ln -s /etc/nginx/sites-available/weather-reporter /etc/nginx/sites-enabled/`
`sudo nginx -t`
`sudo service nginx restart`

`cd /home/bd/weather-reporter/server`
`/home/bd/.virtualenvs/venv/bin/gunicorn app:app`

## Thanks [Alex Simoes](http://alexandersimoes.com/hints/2015/10/28/deploying-flask-with-nginx-gunicorn-supervisor-virtualenv-on-ubuntu.html)

