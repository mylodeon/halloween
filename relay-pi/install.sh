#!/usr/bin/env bash

# System requirements
apt-get update
apt-get upgrade
apt-get --yes install nodejs npm
npm install express
npm install rpi-gpio
npm install cors

cp relay-pi.service /lib/systemd/system/relay-pi.service
chmod 644 /lib/systemd/system/relay-pi.service
sudo systemctl enable relay-pi.service
sudo systemctl start relay-pi.service
