#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi

apt install -y mosquitto
apt install -y python3


curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Aggregator/starter.sh
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Aggregator/establish_connect.py
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Aggregator/env_parser.py
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Aggregator/phys_parser.py
#curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Aggregator/mosquitto.conf
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Security/x509/agg.crt
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Security/x509/agg.key
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/Security/x509/ca.crt

chmod u+x starter.sh

chmod 644 mosquitto.conf
mv mosquitto.conf /etc/mosquitto/mosquitto.conf 

mv agg.crt /etc/mosquitto/certs/
mv agg.key /etc/mosquitto/certs/

chmod 644 /etc/mosquitto/certs/agg.crt
chmod 644 /etc/mosquitto/certs/agg.key

mv ca.crt /etc/mosquitto/ca_certificates/

chmod 644 /etc/mosquitto/ca_certificates/ca.crt

service start mosquitto


echo "Install successful"
