#!/bin/bash

# This file is for enabling a machine to act as a security unit.
echo
echo "#### Security Unit ####"
echo
echo "+---------------------+"
echo "| Installation Script |"
echo "+---------------------+"
echo

if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

LOCAL="192.168.0.4"
FOREIGN="192.168.0.2"

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
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/x509/ca.crt?raw=true -O x509/ca.crt
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/x509/sec.key?raw=true -O /etc/mosquitto/certs/sec.key
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/x509/sec.crt?raw=true -O x509/sec.crt

# Set appropriate file permissions
chmod 755 sensor off alarm MatrixKeypad reg.sh
chmod 777 PINs

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
echo "Restarting..."
reboot
exit 0

