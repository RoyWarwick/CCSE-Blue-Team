#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi

apt install -y mosquitto
apt install -y python3
apt install strongswan libcharon-extra-plugins strongswan-pki -y




curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/forwarder_collector/submission
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/forwarder_collector/server
curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/forwarder_collector/mosquitto.conf




chmod 644 mosquitto.conf
mv mosquitto.conf /etc/mosquitto/mosquitto.conf 

mv submission/tls-ca/server/forwarder-mqtt.crt /etc/mosquitto/certs/
mv submission/tls-ca/server/forwarder-mqtt.key /etc/mosquitto/certs/

chmod 644 /etc/mosquitto/certs/forwarder-mqtt.crt
chmod 644 /etc/mosquitto/certs/forwarder-mqtt.key

mv submission/tls-ca/root/ca.crt /etc/mosquitto/ca_certificates/

chmod 644 /etc/mosquitto/ca_certificates/ca.crt

mv submission/forwarder/etc/ipsec.d/cacerts/ca.cert.pem /etc/ipsec.d/cacerts
mv submission/forwarder/etc/ipsec.d/cacerts/security-ca.cert.pem /etc/ipsec.d/cacerts
mv submission/forwarder/etc/ipsec.d/certs/vpn_forwarder.cert.pem /etc/ipsec.d/certs
mv submission/forwarder/etc/ipsec.d/private/vpn_forwarder.key.pem /etc/ipsec.d/private
mv submission/forwarder/etc/ipsec.conf /etc/
mv submission/forwarder/etc/ipsec.conf.x509 /etc/
mv submission/forwarder/etc/ipsec.secrets /etc/

echo "Install successful"