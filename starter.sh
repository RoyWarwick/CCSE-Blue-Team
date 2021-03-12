#!/bin/bash

rm -r ./tmp > /dev/null
mkdir tmp

#mosquitto -p 1883 > /dev/null & #start mosquitto broker


mosquitto_sub -p 1883 -t 'agr/env' > ./tmp/env_incoming & #start listener for incoming environment data connections
python3 establish_connect.py env & #start the topic allocator for the environmental data

mosquitto_sub -p 1883 -t 'agr/phys' > ./tmp/phys_incoming & #start listener for incoming physical data connections
python3 establish_connect.py phys > /dev/null & #start the topic allocator for the physical security data


#mosquitto_sub -p 1883 -t '$SYS/broker/clients/connected' >> ./tmp/connected &


exit 0

