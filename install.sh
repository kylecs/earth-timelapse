#!/bin/bash
echo "Installing dependencies for earth-timelapse on debian based systems"
apt-get install python-pip
pip install requests
apt-get install imagemagick
echo "Dependencies installed"
