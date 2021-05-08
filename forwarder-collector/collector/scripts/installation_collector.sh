#!/bin/bash
###MOVE collector DIRECTORY FROM forwarder-collector TO THIS MACHINE######
if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi


sudo apt install strongswan libcharon-extra-plugins strongswan-pki -y
sudo apt install python3 -y




mv collector/etc/ipsec.d/cacerts/ca.cert.pem /etc/ipsec.d/cacerts
mv collector/etc/ipsec.d/cacerts/security-ca.cert.pem /etc/ipsec.d/cacerts
mv collector/etc/ipsec.d/certs/vpn_collector.cert.pem /etc/ipsec.d/certs
mv collector/etc/ipsec.d/private/vpn_collector.key.pem /etc/ipsec.d/private
mv collector/etc/ipsec.conf /etc/
mv collector/etc/ipsec.conf.x509 /etc/
mv collector/etc/ipsec.secrets /etc/


echo "Installation complete"