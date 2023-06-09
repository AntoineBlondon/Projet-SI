#!/bin/bash
while true
do
	raspistill -n -rot 180 -o ./static/cam2.jpg -w 1920 -h 1080 -t 10
	sleep 4s
done