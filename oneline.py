import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

running = True

file = open('sensor_readings.txt', 'w')
file.write('time and date, temperature (C), Humidity (%)\n')

while running:

    try:
        
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            print('Temperature = ' + str(temperature) +',' + 'Humidity = ' + str(humidity))
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', ' + str(temperature) + ', ' + str(humidity) + '\n')
            time.sleep(3)

        else:
            print('Failed to get reading. Try again!')
            time.sleep(2)

    except KeyboardInterrupt:
        print ('Program stopped')
        running = False
        file.close()



