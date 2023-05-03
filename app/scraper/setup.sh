#!/bin/sh
#install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#install python libraries
pip install lxml
python3 -m pip install requests
