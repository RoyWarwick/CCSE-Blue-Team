#!/bin/bash

rm -r ./tmp > /dev/null
mkdir tmp

mosquitto_sub -p 8883 --cafile ca.crt --cert server.crt --key server.key -h 192.168.0.2 -t 'agr/env' > ./tmp/env_incoming & #start listener for incoming environment data connections
python3 establish_connect.py env & #start the topic allocator for the environmental data
python3 compile.py

mosquitto_sub -p 8883 --cafile ca.crt --cert server.crt --key server.key -h 192.168.0.2 -t 'agr/phys' > ./tmp/phys_incoming & #start listener for incoming physical data connections
python3 establish_connect.py phys > /dev/null & #start the topic allocator for the physical security data

echo "Start Successful"

exit 0

