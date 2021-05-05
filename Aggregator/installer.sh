#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi

chmod u+x starter.sh

chmod 644 mosquitto.conf
mv mosquitto.conf /etc/mosquitto/mosquitto.conf 

mv agg.crt /etc/mosquitto/certs/
mv agg.key /etc/mosquitto/certs/

chmod 644 /etc/mosquitto/certs/agg.crt
chmod 644 /etc/mosquitto/certs/agg.key

mv ca.crt /etc/mosquitto/ca_certificates/

chmod 644 /etc/mosquitto/ca_certificates/ca.crt


echo "Install successful"
