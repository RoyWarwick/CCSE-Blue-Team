#!/bin/bash

src="/usr/security/log"

while true
do
    if [ "$(tail -1 < $src | grep P)" != "" ]
    then
        mosquitto_pub -t "security" -m "R"
    fi
    sleep 0.1
done
