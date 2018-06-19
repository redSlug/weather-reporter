#!/bin/bash

cd /home/pi/weather-reporter/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
echo "DARK_SKY_API_KEY=$1" > ~/.SECRET
echo "LAT=$2" >> ~/.SECRET
echo "LONG=$3" >> ~/.SECRET
make -C rpi-rgb-led-matrix/examples-api-use
./show_weather.sh