#!/bin/bash

APP_DIR="/var/app/weather-reporter/server"
cd $APP_DIR
git pull
pip3 install -r requirements.txt
export DB_URL="sqlite:///db"
alembic upgrade head