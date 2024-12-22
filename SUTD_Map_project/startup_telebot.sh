#!/bin/bash

cp telebotstartup.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telebotstartup.service
sudo systemctl start telebotstartup.service
sudo systemctl status telebotstartup.service
