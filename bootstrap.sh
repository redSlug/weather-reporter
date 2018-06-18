#!/bin/bash

echo "provisioning - initial server setup"

apt-get update
apt-get install -y git python3-pip
apt-get install sqlite -y

cd /vagrant

git clone https://github.com/redSlug/weather-reporter.git

cd /vagrant/weather-reporter

pip3 install -r requirements.txt

export DB_URL="sqlite:///db"

cd /vagrant/weather-reporter/server

alembic upgrade head

echo "done!"
