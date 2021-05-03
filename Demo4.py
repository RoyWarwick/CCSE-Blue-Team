#libraries

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import signal
import ssl
import re
import random

#GPIO setup

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT) # Red LED GPIO
GPIO.setup(18,GPIO.OUT) # Blue LED GPIO
GPIO.setup(22,GPIO.OUT) # Yellow LED GPIO
GPIO.setup(23,GPIO.OUT) # Green LED GPIO

# DHT setup

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4 # DHT sensor GPIO 
        
n=random.randint(-92233720368547758,92233720368547758)
#random integer to supply to aggregator for topic assignment

publish.single(topic="agr/env", payload=n, hostname="192.168.0.2", port=8883, tls={'ca_certs':"/etc/mosquitto/ca_certificates/env.crt",'certfile':"/etc/mosquitto/certs/env.csr",'keyfile':"/etc/mosquitto/certs/env.key",})
#send the random integer

# topic assignment
message = subscribe.simple("agr/env_response", hostname="192.168.0.2", port=8883,tls={'ca_certs':"/etc/mosquitto/ca_certificates/env.crt",'certfile':"/etc/mosquitto/certs/env.csr",'keyfile':"/etc/mosquitto/certs/env.key",})
        # subscribe to the aggregator topic
        # that assigns the correct sensor topic

inter = str(message.payload) # convert the message to string
t=inter.split("'") # split the topic from quotes

topicfinal=t[1] # use another variable to get the final topic from the list

# Loop of reading values from DHT, lighting LEDs, printing to terminal and publishing to aggregator
try:
 while True:

#DHT read T&H values and output them to terminal    
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN) # initiate T&H variables
                                                                         # using the DHT sensor
    if humidity is not None and temperature is not None:
        s = (time.strftime('%d/%m/%Y %H:%M:%S') + " " + "T={0:0.1f} H={1:0.1f}".format(temperature, humidity))
        #stores the date&time and T&H values in a single variable
        print (s)   
    else:
        print("Failed")
        
# temperature LEDs and print to terminal
        
    # Red LED if temperature is too high
    if temperature >= 23:
        print ("Temperature is higher than 23*")
        GPIO.output(17,GPIO.HIGH)    
    else: GPIO.output(17,GPIO.LOW)
    
    # Blue LED if temperature is too low
    if temperature < 22:
        print ("Temperature is lower than 22*")
        GPIO.output(18,GPIO.HIGH)
    else: GPIO.output(18,GPIO.LOW)

#humidity leds and print to terminal
    
    # Green LED if humidity is too high
    if humidity >= 50:
        print ("Humidity is higher than 50%")
        GPIO.output(23,GPIO.HIGH)
    else: GPIO.output(23,GPIO.LOW)
    
    # Yellow LED if humidity is too low
    if humidity < 49:
        print ("Humidity is lower than 49%")
        GPIO.output(22,GPIO.HIGH)
    else: GPIO.output(22,GPIO.LOW)
    
#publishing to aggregator on the topic received from the aggregator
    
    publish.single(topic=topicfinal, payload=s, hostname="192.168.0.2", port=8883, tls={'ca_certs':"/etc/mosquitto/ca_certificates/env.crt",'certfile':"/etc/mosquitto/certs/env.csr",'keyfile':"/etc/mosquitto/certs/server.key",})
    time.sleep(5)

#clean GPIO when program is interrupted

except:
    GPIO.cleanup()

finally:
    GPIO.cleanup()


