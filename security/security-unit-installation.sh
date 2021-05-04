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

START="$(dirname $(readlink -f $0))"

# Place files in correct place
cd /usr
rm -r security 2> /dev/null # Remove any previous installations
mkdir security
cd security
mkdir x509
touch root.sh
chmod 755 root.sh

# Place files in the correct places
cp $START/sensor sensor
cp $START/off off
cp $START/alarm alarm
cp $START/PINs PINs
cp $START/MatrixKeypad MatrixKeypad
cp $START/openssl.cnf openssl.cnf
cp $START/reg.sh reg.sh
cp $START/x509/ca.crt x509/ca.crt
cp $START/x509/sec.key /etc/mosquitto/certs/sec.key
cp $START/x509/sec.crt x509/sec.crt

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

