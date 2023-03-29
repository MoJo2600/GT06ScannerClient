#!/bin/bash
set -e
set -x

rm -rf venv/
sudo mkdir -p /opt/gpstracker
sudo cp -Rfv gpstracker/ /opt/
cd /opt/gpstracker
sudo python3 -m venv venv
sudo ./venv/bin/pip3 install -r requirements.txt
sudo cp systemd/gpstracker.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable gpstracker
sudo systemctl start gpstracker