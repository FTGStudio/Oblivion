#!/bin/sh

sudo cp dormire.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/dormire.service
sudo systemctl daemon-reload
sudo systemctl enable dormire.service 
