
#libraries

import Adafruit_DHT
import RPi.GPIO as GPIO
import time

#GPIO setup

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

#DHT setup

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


while True:
 try:
    
#DHT read values and output them to terminal    
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        s = (time.strftime('%d/%m/%Y %H:%M:%S') + " " + "T={0:0.1f} H={1:0.1f}".format(temperature, humidity))
       # print(time.strftime('%d/%m/%Y %H:%M:%S') + " " + "T={0:0.1f} H={1:0.1f}".format(temperature, humidity))
        print (s)   
    else:
        print("Failed")
        
#temperature leds and print to terminal
        
    if temperature >= 23:
        print ("Temperature is higher than 23*")
        GPIO.output(17,GPIO.HIGH)    
    else: GPIO.output(17,GPIO.LOW)
    
    if temperature < 22:
        print ("Temperature is lower than 22*")
        GPIO.output(18,GPIO.HIGH)
    else: GPIO.output(18,GPIO.LOW)

#humidity leds and print to terminal
    
    if humidity >= 50:
        print ("Humidity is higher than 50%")
        GPIO.output(23,GPIO.HIGH)
    else: GPIO.output(23,GPIO.LOW)
    
    if humidity < 49:
        print ("Humidity is lower than 49%")
        GPIO.output(22,GPIO.HIGH)
    else: GPIO.output(22,GPIO.LOW)
    
    time.sleep(2)

 except KeyboardInterrupt:
	GPIO.cleanup()


