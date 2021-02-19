#!/bin/bash

STARTPWD=$PWD

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
echo "Press enter to continue..."
read

if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

DST= # destination IP

echo "Installation starting..."

# installation
apt update
apt-get install strongswan apache2-utils mosquitto mosquitto-clients


# Place files in correct place - perhaps /usr/security
cd /usr
mkdir security
cd security
touch log
chmod 555 log
touch root.sh
chmod 777 root.sh

# Get files from github
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/sensor?raw=true -O sensor
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/off?raw=true -O off
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/alarm?raw=true -O alarm
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/PINs?raw=true -O PINs
wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/Security/MatrixKeypad?raw=true -O MatrixKeypad

# Create the root.sh file
echo "#!/bin/bash" > root.sh
echo "cd /home/pi" >> root.sh
echo "/home/pi/MatrixKeypad & disown" >> root.sh
echo "/home/pi/sensor & disown" >> root.sh
echo "mosquitto_sub -t \"security\" -h 127.0.0.1 >> log & disown" >> root.sh
echo "exit 0" >> root.sh

# Setup IPSec
echo -n "" > /etc/ipsec.secrets

# Ensure files are executed at startup

cd $STARTPWD

