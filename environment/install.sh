#!/bin/bash

# This file is for enabling a machine to act as a security unit.
echo
echo "#### Environment Unit ####"
echo
sleep 0.3
echo "+---------------------+"
echo "| Installation Script |"
echo "+---------------------+"
echo
sleep 0.3

# Check if program is run as su
if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

sleep 0.3
echo "Installation starting..."
echo " "
sleep 1

echo "........................"
sleep 0.3
echo "Installing Update"
echo " "
sleep 0.3
# Updating RPi
apt-get update -y
echo " "
echo "Update downloaded"
echo "........................"

echo " "

echo "........................"
sleep 0.3
echo "Upgrading RPi"
sleep 0.3
echo " "
# Upgrading RPi
apt-get upgrade -y
echo " "
echo "Upgraded RPi"
echo "........................"

echo " "

echo "........................"
sleep 0.3
echo "Installing Mosquitto"
sleep 0.3
echo " "
# Installing mosquitto
apt-get install mosquitto -y 
echo " "
echo "Mosquitto installed"
echo "........................"

echo " "

echo "........................"
sleep 0.3
echo "Installing Pip3"
sleep 0.3
echo " "
# Installing Pip3"
apt-get install python3-pip -y
echo " "
echo "Pip3 installed"
echo "........................"

echo " "

echo "........................"
sleep 0.3
echo "Upgrading Pip3"
sleep 0.3
echo " "
# Upgrading Pip3
/usr/bin/python3 -m pip install --upgrade pip
echo " "
echo "Pip3 upgraded"
echo "........................"

echo " "

echo "........................"
sleep 0.3
echo "Installing PahoMQTT"
sleep 0.3
echo " "
# Installing PahoMQTT
pip3 install paho-mqtt
echo " "
echo "PahoMQTT installed"
echo "........................"

echo " "

echo "........................"
sleep 0.3
# Installing Adafruit DHT package
echo "Installing Adafruit DHT package"
echo " "
pip3 install Adafruit_Python_DHT 
sleep 0.3
echo " "
echo "Installed Adafruit DHT package"
echo "........................"

echo " "
echo " "
echo " "
echo " "

# Memorize the current directory
START="$(dirname $(readlink -f $0))"

# Change permissions for copying to the intended folders and executing
echo "........................"
echo "Changing permissions"
sleep 0.3
echo " "
chmod 777 ca.crt env.crt env.key
chmod 777 Environment.py
chmod 777 /etc/mosquitto/mosquitto.conf
chmod 777 /etc/rc.local
echo "Permissions changed"
echo "........................"

echo " "

# Copy certs and key 
echo "........................"
echo "Copying certificates and key"
sleep 0.3
echo " "
cp $START/ca.crt /etc/mosquitto/ca_certificates/ca.crt
cp $START/env.crt /etc/mosquitto/certs/env.crt
cp $START/env.key /etc/mosquitto/certs/env.key
echo "Files copied"
echo "........................"

echo " "

# Updating mosquitto.conf
echo "........................"
echo "Updating mosquitto.conf"
sleep 0.3
echo " "
echo "port 8883" >> /etc/mosquitto/mosquitto.conf
echo "cafile /etc/mosquitto/ca_certificates/ca.crt" >> /etc/mosquitto/mosquitto.conf
echo "certfile /etc/mosquitto/certs/env.crt" >> /etc/mosquitto/mosquitto.conf
echo "keyfile /etc/mosquitto/certs/env.key" >> /etc/mosquitto/mosquitto.conf
echo "require_certificate true" >> /etc/mosquitto/mosquitto.conf
echo "mosquitto.conf updated"
echo "........................"

echo " "

# Make Environment.py run on startup
echo "........................"
echo "Making Python script run at startup"
sleep 0.3
echo " "
head -n -1 /etc/rc.local > temp.txt
echo "python3 "$START"/Environment.py" >> temp.txt
echo "exit 0" >> temp.txt
mv temp.txt /etc/rc.local
chmod 777 /etc/rc.local
echo "Made Python script run at startup"
echo "........................"

echo " "
echo " "
echo "Installation finished"
sleep 1
echo " "
echo "Will restart in 3 seconds..."
sleep 3

#reboot
reboot

exit 0