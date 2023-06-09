#!/bin/bash

smbclient -L 192.168.1.1 -Uclient%pi
sudo PASSWD='pi' mount -t cifs //192.168.1.1/pishare /home/pi/server/static/photos -o username=client,dir_mode=0777,file_mode=0777
. server/bin/activate
export FLASK_APP=app.py
flask run