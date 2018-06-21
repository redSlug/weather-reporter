#!/bin/bash

# crontab
# reboot /home/pi/weather-reporter/pi/show_weather.sh >> /home/pi/weather-reporter/log

cleanup() {
    echo "Cleaning stuff up" >> log
    sudo pkill demo
    exit
}

delay_milliseconds=18

trap cleanup EXIT
while true; do
    wget -N http://206.189.229.207/static/weather.ppm
    # curl http://server/folder/file1.html > file1.html
    if [ $? -eq 0 ];
    then
        echo "wget succeeded"
        sudo pkill demo
	    sudo rpi-rgb-led-matrix/examples-api-use/demo -D 1 $target --led-no-hardware-pulse --led-rows=16 --led-cols=32 -m $delay_milliseconds --led-daemon --led-brightness=10
    else
        echo "wget failed - file was likely not modified"
    fi
    sleep 2m
done