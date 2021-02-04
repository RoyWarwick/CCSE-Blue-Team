import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT22
sensor_pin = 4

running = True

file = open('sensor_readings.txt', 'w')
file.write('time and date, temperature (C),temperature (F), humidity\n')

while running:

    try:
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
        temperature_f = temperature * 9/5.0 + 32
        if humidity is not None and temperature is not None:
            print('Temperature = ' + str(temperature) +','+ 'Temperature Fahrenheit = ' + str(temperature_f) +',' + 'Humidity = ' + str(humidity))
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', ' + str(temperature) + ', '+ str(temperature_f)+',' + str(humidity) + '\n')
            time.sleep(1)

        else:
            print('Failed to get reading. Try again!')
            time.sleep(1)

    except KeyboardInterrupt:
        print ('Program stopped')
        running = False
        file.close()

