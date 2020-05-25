#!/bin/bash

# crontab
# @reboot /home/pi/weather-reporter/pi/show_weather.sh >> /home/pi/weather-reporter/log

cleanup() {
    echo "Cleaning stuff up $(date)" >> log
    sudo pkill demo
    exit
}


pushd /home/pi/weather-reporter/pi
image_file="weather.ppm"
if [ ! -f $image_file ]; then
    echo "File not found! $(date)" >> log
    exit 1
fi

delay_milliseconds=18

trap cleanup EXIT
while true; do
    wget -N http://206.189.229.207/static/weather.ppm
    # curl http://server/folder/file1.html > file1.html
    if [ $? -eq 0 ];
    then
        echo "wget succeeded $(date)"
        sudo pkill demo
	    sudo rpi-rgb-led-matrix/examples-api-use/demo -D 1 $image_file --led-no-hardware-pulse --led-rows=16 --led-cols=32 -m $delay_milliseconds --led-daemon --led-brightness=10
    else
        echo "wget failed - file was likely not modified $(date)"
    fi
    sleep 2m
done

popd
