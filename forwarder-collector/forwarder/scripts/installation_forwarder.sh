#!/bin/bash
#### MOVE forwarder DIRECTORY FROM forwarder-collector TO THIS MACHINE######
if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi

sudo apt install -y mosquitto
sudoapt install -y python3
sudo apt install -y strongswan libcharon-extra-plugins strongswan-pki
sudo apt install -y openssl






chmod 644 mosquitto.conf
mv mosquitto.conf /etc/mosquitto/mosquitto.conf 

mv forwarder_collector/tls-ca/server/forwarder-mqtt.crt /etc/mosquitto/certs/
mv forwarder_collector/tls-ca/server/forwarder-mqtt.key /etc/mosquitto/certs/

chmod 644 /etc/mosquitto/certs/forwarder-mqtt.crt
chmod 644 /etc/mosquitto/certs/forwarder-mqtt.key

mv forwarder_collector/tls-ca/root/ca.crt /etc/mosquitto/ca_certificates/

chmod 644 /etc/mosquitto/ca_certificates/ca.crt

mv forwarder_collector/forwarder/etc/ipsec.d/cacerts/ca.cert.pem /etc/ipsec.d/cacerts
mv forwarder_collector/forwarder/etc/ipsec.d/cacerts/security-ca.cert.pem /etc/ipsec.d/cacerts
mv forwarder_collector/forwarder/etc/ipsec.d/certs/vpn_forwarder.cert.pem /etc/ipsec.d/certs
mv forwarder_collector/forwarder/etc/ipsec.d/private/vpn_forwarder.key.pem /etc/ipsec.d/private
mv forwarder_collector/forwarder/etc/ipsec.conf /etc/
mv forwarder_collector/forwarder/etc/ipsec.conf.x509 /etc/
mv forwarder_collector/forwarder/etc/ipsec.secrets /etc/

sudo sysctl -p
sudo service ipsec start

touch host_id

sudo service mosquitto start

mosquitto_sub -p 8883 --cafile /etc/mosquitto/ca_certificates/ca.crt --cert /etc/mosquitto/certs/forwarder-broker.crt --key /etc/mosquitto/certs/forwarder-broker.key -h 192.168.0.50 -t "fwd/aggr_in" -N > /tmp/aggr_env_in.json &

mosquitto_sub -p 8883 --cafile /etc/mosquitto/ca_certificates/ca.crt --cert /etc/mosquitto/certs/forwarder-broker.crt --key /etc/mosquitto/certs/forwarder-broker.key -h 192.168.0.50 -t "fwd/aggr_in" -N > /tmp/aggr_phys_in.json &

echo "Install successful"