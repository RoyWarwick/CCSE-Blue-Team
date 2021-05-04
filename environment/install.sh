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
if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

sleep 0.3
echo "Installation starting..."
echo " "
echo "........................"
sleep 0.3
echo "Installing Update"
sleep 0.3
apt-get update -y
echo "Update downloaded"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Upgrading"
sleep 0.3
apt-get upgrade -y
echo "Upgraded"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Installing Mosquitto"
sleep 0.3
apt-get install mosquitto -y 
echo "Mosquitto installed"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Installing Pip3"
sleep 0.3
apt-get install python3-pip -y
echo "Pip3 installed"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Upgrading Pip3"
sleep 0.3
/usr/bin/python3 -m pip install --upgrade pip
echo "Pip3 upgraded"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Installing PahoMQTT"
sleep 0.3
pip3 install paho-mqtt
echo "PahoMQTT installed"
echo "........................"
echo " "
echo "........................"
sleep 0.3
echo "Installing Adafruit DHT package"
pip3 install Adafruit_Python_DHT 
sleep 0.3
echo "Installing Adafruit DHT package"
echo "........................"

echo " "
echo " "
echo " "
echo " "

START="$(dirname $(readlink -f $0))"
echo $START

exit 0