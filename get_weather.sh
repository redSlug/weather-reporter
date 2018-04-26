#!/bin/bash

pushd /home/pi/weather-reporter
source ~/.SECRET
source venv/bin/activate
python get_weather.py $DARK_SKY_API_KEY $LAT $LONG
date >> log
popd



