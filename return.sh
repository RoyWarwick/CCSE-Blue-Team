#!/bin/bash

while true
do
    if [ "$(tail -1 < /usr/security/log | grep P)" != "" ]
    then
        mosquitto_pub -m "R" -t "security" -p 8883 --cafile certs/ca.crt --cert certs/sec.crt --key certs/sec.key -h "192.168.1.66"
    fi
    sleep 0.1
done
