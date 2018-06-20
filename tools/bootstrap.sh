#!/bin/bash

apt-get update
apt-get install -y git python3-pip
apt-get install sqlite -y
APP_DIR="/var/app/weather-reporter"
mkdir -p $APP_DIR
git clone https://github.com/redSlug/weather-reporter.git $APP_DIR
cd $APP_DIR
pip3 install -r requirements.txt

# allow travis to ssh into production server
PUB_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzQhcHbTj7O3CeSy/ckoUgQFcXfeZPOMzgfxLOt1qs/kUoj8xFO+gjQs52kElMVtyoMrtV4TmdJekfXrJRZGlbUH7PPkED81+YoBYCWXDECBEftNte2nRGiIIMLjzAAUaoAR9lUDQKXda2XRZ3BxM1GFfXDY4ALFx6h0MXPJb8ksl034B37VpbmV2zoJ9eZZZ6L0VfHyGGlDQQdqfKPsezs4KzUhuxN9QlaoRJonayj00MZBaUdRV35DhvdgEUZvc68wOxLT2QXPb11FYIe0e33+uffmfdQrXVXjXZHk6IAF5Y2wlPctTa1EX1JlqjcCSzIX9kRvD0wVcdHDklLI5v bd@Brads-MacBook-Pro.local"
mkdir -p "/home/bd/.ssh"
echo $PUB_KEY >> "/home/bd/.ssh/authorized_keys"