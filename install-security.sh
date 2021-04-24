#!/bin/bash

# This file is for enabling a machine to act as a security unit.
echo
echo "#### Security Unit ####"
echo
echo "+---------------------+"
echo "| Installation Script |"
echo "+---------------------+"
echo

# User information
echo Requirements
echo ============
echo "This script ought to be run as the superuser on a Raspberry Pi with the correct hardware connected to the GPIO pins."
echo "The unit needs to be able to route IPv4 packets to an aggregator."
echo "This installation script requires the IPv4 addresses of both units for routing packets."
echo
echo Prompt
echo ======
echo "You may use a signal interrupt to exit, or"
echo -n "Press enter to continue..."
read

if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

echo -n "Provide local IPv4 address: "
read
LOCAL=$REPLY
echo -n "Provide foreign IPv4 address: "
read
FOREIGN=$REPLY

echo "Installation starting..."

# installation
apt update
apt-get install -y openssl strongswan apache2-utils mosquitto mosquitto-clients

# Place files in correct place
cd /usr
rm -r security 2> /dev/null # Remove any previous installations
mkdir security
cd security
mkdir x509
touch root.sh
chmod 755 root.sh

# Get files from github
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/sensor?raw=true -O sensor
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/off?raw=true -O off
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/alarm?raw=true -O alarm
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/PINs?raw=true -O PINs
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/MatrixKeypad?raw=true -O MatrixKeypad
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/openssl.cnf?raw=true -O openssl.cnf
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/reg.sh?raw=true -O reg.sh

# Set appropriate file permissions
chmod 755 sensor off alarm MatrixKeypad reg.sh
chmod 777 PINs

# Create TLS files
openssl genrsa -out /etc/mosquitto/certs/sec.key 4096
cat /usr/security/openssl.cnf | perl -p -e 's/<local-ip>/'$LOCAL'/' | tee /usr/security/x509/openssl.cnf
echo -ne "\n\n\n\n\n\n\n\n\n" | openssl req -out /usr/security/x509/sec.csr -key /etc/mosquitto/certs/sec.key -new -config /usr/security/x509/openssl.cnf
rm /usr/security/openssl.cnf
chmod 777 x509 x509/*
echo
echo "x509 Requirements"
echo "-----------------"
echo
echo "A certificate signing request (/usr/security/x509/sec.csr) has been created."
echo "A certificate authority must be trusted by both this unit and its aggregator; the certificate of which must be stored locally as /usr/security/x509/ca.crt"
echo "The certificate signing request must be signed by that certificate authority, using /usr/security/x509/openssl.cnf as the config file (see note 3 below), and the certifiate stored locally as /usr/security/x509/sec.crt"
echo
echo "Notes: 1) A certificate authority's keys may be generated using: "
echo "-----      openssl genrsa -out ca.key 4096"
echo "       2) A certificate authority may create a self-signed certificate using:"
echo "           openssl req -new -x509 -days 365 -key ca.key -out ca.crt"
echo "       3) A certificate authority may sign a certificate signing request with a config file 'openssl.cnf' using:"
echo "           openssl x509 -req -in sec.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out sec.crt -days 365 -extensions v3_req -extfile openssl.cnf"
echo
echo -n "Press enter one this is done..."
read

# Update mosquitto.conf
grep -v "^port" /etc/mosquitto/mosquitto.conf | grep -v "^cafile" | grep -v "^keyfile" | grep -v "^certfile" | grep -v "^require_certificate" > /etc/mosquitto/mosquitto.conf
echo "port 8883" >> /etc/mosquitto/mosquitto.conf
echo "cafile /usr/security/x509/ca.crt" >> /etc/mosquitto/mosquitto.conf
echo "keyfile /etc/mosquitto/certs/sec.key" >> /etc/mosquitto/mosquitto.conf
echo "certfile /usr/security/x509/sec.crt" >> /etc/mosquitto/mosquitto.conf
echo "require_certificate true" >> /etc/mosquitto/mosquitto.conf

# Create the root.sh file
echo "#\!/bin/bash" > root.sh
echo "cd /usr/security" >> root.sh
echo "TOPIC=$(/usr/security/reg.sh $LOCAL)" >> root.sh
echo "/usr/security/MatrixKeypad \"$LOCAL\" \$TOPIC & disown" >> root.sh
echo "/usr/security/sensor \"$LOCAL\" \$TOPIC & disown" >> root.sh
echo "exit 0" >> root.sh

# Ensure files are executed at startup
echo "#\!/bin/bash" > /etc/rc.local
echo "/usr/security/root.sh" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local

echo "Installation complete."
echo "Restart the machine to use it."

exit 0

