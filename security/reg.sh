#!/bin/bash

mosquitto_sub -t "arg/phys_response" -p 8883 --cafile /usr/security/x509/ca.crt --cert /usr/security/x509/sec.crt --key /etc/mosquitto/certs/sec.key -h $1 >> /usr/security/est &

RAND="$$$(date +%s)"

mosquitto_pub -t "agr/phys" -m "$RAND" -p 8883 --cafile /usr/security/x509/ca.crt --cert /usr/security/x509/sec.crt --key /etc/mosquitto/certs/sec.key -h $1

while true
do
    TMP=$(tail -1 < /usr/security/est | grep $RAND)
    if [ "$TMP" != "" ]
    then
        cut -d ' ' -f 2 <<< $TMP
        exit 0
    fi
    sleep 0.1
done
