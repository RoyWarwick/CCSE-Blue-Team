#!/bin/bash
#### MOVE forwarder DIRECTORY FROM forwarder-collector TO THIS MACHINE######
if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi

sudo apt install -y mosquitto
sudo apt install -y python3
sudo apt install -y strongswan libcharon-extra-plugins strongswan-pki
sudo apt install -y openssl


pip3 install tqdm




mv forwarder/tls-ca/mosquitto.conf /etc/mosquitto/mosquitto.conf 
chmod 644 mosquitto.conf

mv forwarder/tls-ca/server/forwarder-mqtt.crt /etc/mosquitto/certs/
mv forwarder/tls-ca/server/forwarder-mqtt.key /etc/mosquitto/certs/

chmod 644 /etc/mosquitto/certs/forwarder-mqtt.crt
chmod 644 /etc/mosquitto/certs/forwarder-mqtt.key

mv forwarder/tls-ca/root/ca.crt /etc/mosquitto/ca_certificates/

chmod 644 /etc/mosquitto/ca_certificates/ca.crt

mv forwarder/etc/ipsec.d/cacerts/ca.cert.pem /etc/ipsec.d/cacerts
mv forwarder/etc/ipsec.d/cacerts/security-ca.cert.pem /etc/ipsec.d/cacerts
mv forwarder/etc/ipsec.d/certs/vpn_forwarder.cert.pem /etc/ipsec.d/certs
mv forwarder/etc/ipsec.d/private/vpn_forwarder.key.pem /etc/ipsec.d/private
mv forwarder/etc/ipsec.conf /etc/
mv forwarder/etc/ipsec.conf.x509 /etc/
mv forwarder/etc/ipsec.secrets /etc/

mv forwarder/scripts/env_in_json.py .
mv forwarder/scripts/phys_in_json.py .
mv forwarder/scripts/installation_forwarder.sh .
mv forwarder/scripts/run.sh .
mv forwarder/script/tcp_client.py .

touch host_id
touch aggr_env_in.json
touch aggr_phys_in.json

chmod +x run.sh

echo "Installation and set-up complete."
