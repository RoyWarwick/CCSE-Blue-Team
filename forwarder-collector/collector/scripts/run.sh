#!/bin/bash
#### MOVE collector DIRECTORY FROM forwarder-collector TO THIS MACHINE######

if [ "$EUID" -ne 0 ]
  then echo "This run script requires root privilages to run"
  exit
fi


sudo sysctl -p
sudo service ipsec start

echo "IPSEC tunnel are now set up."
