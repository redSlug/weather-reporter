#!/bin/bash

# crontab -e
# @reboot /home/pi/weather-reporter/pi/game_of_life.sh

MAX_LOG_FILE_SIZE=250000000
INTERVAL_DELAY=17s
LED_DELAY_MS=18
LOG_FILE=/home/pi/weather-reporter/pi/log

function log_to_file {
    echo "$(date) $1" >> log
}

function cleanup {
    log_to_file "Clearing LED display"
    sudo pkill demo
    exit
}

function rotate_logs_if_needed {
    log_file_size=$(du -b log | tr -s '\t' ' ' | cut -d' ' -f1)

    if [ $log_file_size -gt $MAX_LOG_FILE_SIZE ];then
        log_to_file "Rotating log file of size $log_file_size bytes"
        mv $LOG_FILE "$LOG_FILE.backup"
        touch $LOG_FILE
    fi
}

function main {
    pushd /home/pi/weather-reporter/pi

    while true; do
        log_to_file "GOL"
        sudo pkill demo
        sudo rpi-rgb-led-matrix/examples-api-use/demo -D7 --led-no-hardware-pulse --led-rows=16 --led-cols=32 -m $LED_DELAY_MS --led-daemon --led-brightness=10
        rotate_logs_if_needed
        sleep $INTERVAL_DELAY
    done

    popd
}

trap cleanup EXIT
main
