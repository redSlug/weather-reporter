#!/bin/bash

APP_DIR="/var/app/weather-reporter"
cd $APP_DIR
git pull
pip3 install -r requirements.txt
export DB_URL="sqlite:///db"
cd $APP_DIR/server
alembic upgrade head