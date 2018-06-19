#!/bin/bash

apt-get update
apt-get install -y git python3-pip
apt-get install sqlite -y
APP_DIR="/var/app/weather-reporter"
mkdir -p $APP_DIR
git clone https://github.com/redSlug/weather-reporter.git $APP_DIR
cd $APP_DIR
pip3 install -r requirements.txt