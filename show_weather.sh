#!/bin/bash

cleanup() {
    echo "Cleaning stuff up" >> log
    sudo pkill demo
    popd
    exit
}

pushd /home/pi/weather-reporter
image_file="images/weather.ppm"
if [ ! -f $image_file ]; then
    echo "File not found!" >> log
    exit 1
fi

last_modified=`date +%s`  # initialized to current time
delay_milliseconds=18

trap cleanup EXIT
while true; do
    modified=`date +%s -r $image_file`
    if [ $modified -eq $last_modified ]; then
	echo -n "." >> log
    else
	echo "Detected file changes" >> log
	sudo pkill demo
	sudo rpi-rgb-led-matrix/examples-api-use/demo -D 1 $image_file --led-no-hardware-pulse --led-rows=16 --led-cols=32 -m $delay_milliseconds --led-daemon --led-brightness=10
	last_modified=$modified
    fi
    sleep 1
done
