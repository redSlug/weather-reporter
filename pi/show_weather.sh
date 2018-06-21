#!/bin/bash

cleanup() {
    echo "Cleaning stuff up" >> log
    sudo pkill demo
    exit
}

delay_milliseconds=18
two_minutes=120000

trap cleanup EXIT
while true; do
    wget http://206.189.229.207/static/weather.ppm
    if [ $? -eq 0 ];
    then
        echo "scp succeeded"
        sudo pkill demo
	    sudo rpi-rgb-led-matrix/examples-api-use/demo -D 1 $target --led-no-hardware-pulse --led-rows=16 --led-cols=32 -m $delay_milliseconds --led-daemon --led-brightness=10
    else
        echo "scp failed"
    fi
    sleep $two_minutes
done