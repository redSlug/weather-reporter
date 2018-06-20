#!/bin/bash

apt-get update
apt-get install -y git python3-pip
apt-get install sqlite -y
APP_DIR="/var/app/weather-reporter"
mkdir -p $APP_DIR
git clone https://github.com/redSlug/weather-reporter.git $APP_DIR
cd $APP_DIR/server
pip3 install -r requirements.txt

# TODO (crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/job -with args") | crontab -

# TODO do key stuff differently later
echo "DARK_SKY_API_KEY=$1" > ~/.SECRET
echo "LAT=$2" >> ~/.SECRET
echo "LONG=$3" >> ~/.SECRET
# allow pi to ssh into production server to get display.ppm
PUB_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzQhcHbTj7O3CeSy/ckoUgQFcXfeZPOMzgfxLOt1qs/kUoj8xFO+gjQs52kElMVtyoMrtV4TmdJekfXrJRZGlbUH7PPkED81+YoBYCWXDECBEftNte2nRGiIIMLjzAAUaoAR9lUDQKXda2XRZ3BxM1GFfXDY4ALFx6h0MXPJb8ksl034B37VpbmV2zoJ9eZZZ6L0VfHyGGlDQQdqfKPsezs4KzUhuxN9QlaoRJonayj00MZBaUdRV35DhvdgEUZvc68wOxLT2QXPb11FYIe0e33+uffmfdQrXVXjXZHk6IAF5Y2wlPctTa1EX1JlqjcCSzIX9kRvD0wVcdHDklLI5v bd@Brads-MacBook-Pro.local"
mkdir -p "/home/bd/.ssh"
echo $PUB_KEY >> "/home/bd/.ssh/authorized_keys"