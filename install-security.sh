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
echo "This installation script requires the IPv4 addresses of both units for routing packets and a pre-shared key that will be used for internet protocol security."
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
touch log
chmod 755 log
touch root.sh
chmod 711 root.sh

# Get files from github
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/sensor?raw=true -O sensor
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/off?raw=true -O off
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/alarm?raw=true -O alarm
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/PINs?raw=true -O PINs
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/MatrixKeypad?raw=true -O MatrixKeypad
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/return.sh?raw=true -O return.sh
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/openssl.cnf?raw=true -O x509/openssl.cnf
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/mosquitto.conf?raw=true -O /etc/mosquitto/mosquitto.conf

# Set appropriate file permissions
chmod 711 sensor off alarm MatrixKeypad return.sh
chmod 744 PINs x509/openssl.cnf

# Create TLS files
openssl genrsa -out /etc/mosquitto/certs/sec.key 4096
cat openssl.cnf | perl -p -e 's/<local-IP>/'$LOCAL'/' > openssl.cnf
echo -ne "\n\n\n\n\n\n\n\n\n" | openssl req -out /usr/security/x509/sec.csr -key /etc/mosquitto/certs/sec.key -new -config /usr/security/x509/openssl.cnf &> /dev/null
echo "A certificate signing request (/usr/security/x509/sec.csr) has been created."
echo "A certificate authority must be trusted by both this unit and its aggregator; the certificate of which must be stored locally as /usr/security/x509/ca.crt"
echo "The certificate signing request must be signed by that certificate authority and the certifiate stored locally as /usr/security/x509/sec.crt"
echo -n "Press enter one this is done..."
read

# Create the root.sh file
echo "#\!/bin/bash" > root.sh
echo "cd /usr/security" >> root.sh
echo "service ipsec start" >> root.sh
echo "/usr/security/MatrixKeypad $LOCAL & disown" >> root.sh
echo "/usr/security/sensor $LOCAL & disown" >> root.sh
echo "/usr/security/return.sh & disown" >> root.sh
echo "mosquitto_sub -t \"security\" --cafile /etc/mosquitto/certs/ca.crt --cert /etc/mosquitto/certs/server.crt --key /etc/mosquitto/certs/server.key -p 8883 -h \"$LOCAL\" >> log & disown" >> root.sh
echo "exit 0" >> root.sh

# Ensure files are executed at startup
echo "#\!/bin/bash" > /etc/rc.local
echo "/usr/security/root.sh" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local

exit 0

