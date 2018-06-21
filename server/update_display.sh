#!/bin/bash

source /home/bd/.virtualenvs/venv/bin/activate
source ~/.SECRET
APP_DIR="/home/bd/weather-reporter/server"
cd $APP_DIR
python client/get_calendar.py
python client/get_weather.py
