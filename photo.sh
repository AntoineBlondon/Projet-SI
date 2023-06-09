#!/bin/bash
# Prend des photos avec la caméra indéfiniment avec un temps d'attente de 0.5s entre les prises
while true
do
	raspistill -n -rot 90 -o /partage/img/cam1.jpg -w 1920 -h 1080 -t 500
	sleep 0.5s
done