#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This installation script requires root privilages to run"
  exit
fi


apt install strongswan libcharon-extra-plugins strongswan-pki -y




curl -LJO https://raw.githubusercontent.com/RoyWarwick/CCSE-Blue-Team/collector_collector/submission






mv submission/collector/etc/ipsec.d/cacerts/ca.cert.pem /etc/ipsec.d/cacerts
mv submission/collector/etc/ipsec.d/cacerts/security-ca.cert.pem /etc/ipsec.d/cacerts
mv submission/collector/etc/ipsec.d/certs/vpn_collector.cert.pem /etc/ipsec.d/certs
mv submission/collector/etc/ipsec.d/private/vpn_collector.key.pem /etc/ipsec.d/private
mv submission/collector/etc/ipsec.conf /etc/
mv submission/collector/etc/ipsec.conf.x509 /etc/
mv submission/collector/etc/ipsec.secrets /etc/

sysctl -p
service ipsec start

echo "Install successful"