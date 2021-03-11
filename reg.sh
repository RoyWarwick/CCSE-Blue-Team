#!/bin/bash

mosquitto_sub -t "arg/phys_response" >> /usr/security/est &

RAND=$$

mosquitto_pub -t "agr/phys" -m "$RAND"
while true
do
    TMP=$(tail -1 < /usr/security/est | grep $RAND)
    if [ "$TMP" != "" ]
    then
        exit 0
    fi
    sleep 0.1
done
