#!/bin/bash
#### MOVE forwarder DIRECTORY FROM forwarder-collector TO THIS MACHINE######

if [ "$EUID" -ne 0 ]
  then echo "This run script requires root privilages to run"
  exit
fi



sudo sysctl -p
sudo service ipsec start

sudo service mosquitto start

mosquitto_sub -p 8883 --cafile /etc/mosquitto/ca_certificates/ca.crt --cert /etc/mosquitto/certs/forwarder-broker.crt --key /etc/mosquitto/certs/forwarder-broker.key -h 192.168.0.254 -t "fwd/aggr_env_in" -N > aggr_env_in.json &

mosquitto_sub -p 8883 --cafile /etc/mosquitto/ca_certificates/ca.crt --cert /etc/mosquitto/certs/forwarder-broker.crt --key /etc/mosquitto/certs/forwarder-broker.key -h 192.168.0.254 -t "fwd/aggr_phys_in" -N > aggr_phys_in.json &

python3 env_in_json.py &
python3 phys_in_json.py &

echo "Mosquitto MQTT and IPSEC are now up and running."
