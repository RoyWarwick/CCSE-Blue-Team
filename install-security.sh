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
echo -n "Provide pre-shared secret: "
read
SECRET=$REPLY

echo "Installation starting..."

# installation
apt update
apt-get install strongswan apache2-utils mosquitto mosquitto-clients

# Place files in correct place
cd /usr
rm -r security 2> /dev/null # Remove any previous installations
mkdir security
cd security
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

# Set appropriate file permissions
chmod 711 sensor off alarm MatrixKeypad
chmod 744 PINs

# Create the root.sh file
echo "#!/bin/bash" > root.sh
echo "cd /usr/security" >> root.sh
echo "service ipsec start" >> root.sh
echo "/usr/security/MatrixKeypad & disown" >> root.sh
echo "/usr/security/sensor & disown" >> root.sh
echo "mosquitto_sub -t \"security\" -h 127.0.0.1 >> log & disown" >> root.sh
echo "exit 0" >> root.sh

# Setup IPSec - adapted from Norris, P.
echo "$LOCAL $FOREIGN : PSK \"$SECRET\"" > /etc/ipsec.secrets

echo config setup > /etc/ipsec.conf
echo -e "\tcharonstart=yes" >> /etc/ipsec.conf
echo -e "\tcharondebug=\"dmn 3, mgr 3, ike 3, chd 3, job -1, cfg 3, knl 1, net 1, enc 2, lib -1\"">> /etc/ipsec.conf
echo -e "\tplutostart=yes">> /etc/ipsec.conf
echo -e "\tplutodebug=all">> /etc/ipsec.conf
echo -e "\tplutostderrlog=/var/log/pluto.log">> /etc/ipsec.conf
echo -e "\tnat_traversal=yes">> /etc/ipsec.conf
echo -e "\tvirtual_private=%v4:10.0.0.0/8,%v4:192.168.0.0/16,%v4:172.16.0.0/12">> /etc/ipsec.conf

echo conn vpn >> /etc/ipsec.conf
echo -e "\tauthby=secret">> /etc/ipsec.conf
echo -e "\tauto=start">> /etc/ipsec.conf
echo -e "\tkeyexchange=ikev2">> /etc/ipsec.conf
echo -e "\tike=aes256-sha1-modp1024">> /etc/ipsec.conf
echo -e "\tpfs=yes">> /etc/ipsec.conf
echo -e "\ttype=tunnel">> /etc/ipsec.conf

echo -e "\tleft=$LOCAL">> /etc/ipsec.conf
echo -e "\tleftsubnet=$LOCAL/32">> /etc/ipsec.conf
echo -e "\tright=$FOREIGN">> /etc/ipsec.conf
echo -e "\trightsubnet=$FOREIGN/32">> /etc/ipsec.conf

# Ensure files are executed at startup
echo "#\!/bin/bash" > /etc/rc.local
echo "/usr/security/root.sh" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local

cd $STARTPWD

