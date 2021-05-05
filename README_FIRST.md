For the pre-submission testing, Option A (Pre-defined Adressing Option) is desired for the network.

All of the files and documentation that are needed are here in this ("main") branch; this document provides installation instructions.


+---------------+
| Security Unit |
+---------------+

This component uses sensor 2 (the machine with private IPv4 address 192.168.0.4).
The machine must have GPIO pins connected to components in accordance with the diagram stored as "security/security unit circuit diagram.jpg".
The directory in this branch called "security" must be downloaded onto the machine and the "security-unit-installation.sh" file within that must be locally executed (as the superuser) as its installation script; this script requires no user input or output in order to sucessfully complete.
The script will finish by rebooting the machine and when it starts up again it will be a fully-automated unit.
This can be setup regardless of whether any other machines have been setup.


+------------------------------------+
| Environment Unit section beginning |
+------------------------------------+

This component uses sensor 1 (the machine with the private IPv4 address 192.168.0.1)

The RPi must be configured accordingly to the diagram.

Red LED	PIN 11 = GPIO 17 (Red color wire)
Blue LED	PIN 12 = GPIO 18 (Purple color wire)
Yellow LED 	PIN 15 = GPIO 22 (Yellow color wire)
Green LED	PIN 16 = GPIO 23 (Green color wire)
330Ω resistors used for each LED

DHT VCC = PIN 1 (Red color wire)
DHT DATA PIN 7 = GPIO 4 (Purple color wire)
DHT Ground  = PIN 6 (Black color wire)
10kΩ resistor used for DHT22

Breadboard Ground for LEDs = PIN 9 (Black color wire)

---------------------------------------------------------------------------------------------

install.sh takes care of: 
- updating & upgrading RPi
- installing mosquitto
- installing Pip3
- upgrading Pip3
- installing PahoMQTT
- installing Adafruit DHT package
- changing permissions of files that need to be modified/used/copied
- copying certificates and keys where they need to be for TLS to work
- modifying the mosquitt.conf file for TSL to work
- Running Py Script on startup by modifying /etc/rc.local by adding the Environment.py
- rebooting for any changes that need it for having effect

-----------------------------------------------------------------------------------------------

Environment.py works by:
- Sending securely a random number to aggregator to ask for a topic
- Subscribing securely to the aggregator's request topic and listening for any response.
- The response is stored and used later on as the topic for sending Temperature and Humidity values
Loop of:
- Temperature and Humidity values are obtained from the DHT22 sensor
- Printing Date,Time and Temperature and humidity Values
- Checking their values against thresholds (22 & 23 *C | 49 & 50 % Humidity)
- Action taken if thresholds are crossed: LEDs light up accordingly and message is output to the terminal that runs the script
- Publishing Date,Time and Temperature and humidity Values securely to the aggregator, using the topic obtained earlier

--------------------------------------------------------------------------------------------------

Installing and running steps:

Step 0.1) Requires aggregator to be already running
Step 0.2) sudo chmod -R 777 CCSE-Blue-Team/ to make sure the install script is runnable

Step 1) run install.sh as su (Internet required) (Might take a while)
sudo ./install.sh
RPi will reboot at the end

Step 2) Hopefully it works automated with the Environment.py script already running
The Py script is listening for a topic to publish to.
The LEDs should light up if thresholds are passed even if a topis is not specified. 
When it is received, it should start publishing to aggregator and displaying values and information to terminal.

------------------------------------------------------------------------------------------------------

Troubleshooting:
1) If DHT sensor does not work with the library installed from the install.sh script, please download it from this link ( https://github.com/adafruit/Adafruit_Python_DHT ) and run the setup.py from there. 
2) If the Environment.py does not start upon rebooting, please run it manually. (can check if it is running with    ps -aef | grep python   )


+---------------------------------+
| Environment Unit section ending |
+---------------------------------+


+------------+
| Aggregator |
+------------+

-This component has an expected I.P address of 192.168.0.4 consistant with the network architecture provided under option A.
-In order to install, pull the aggregator directory and it's contents from the Github Main branch.
-There are two files of interest within the aggregator directory, Installer.sh and Starter.sh

-installer.sh will distribute certificates and config files, as well as changing file permissions to enable the system to run.
-installer.sh does require root (sudo) permissions to run
-The installation process should only be run once.
-It may be required to alter the permissions of the Installation script to enable it to run, this can be achieved in the shell by 'chmod u+x installer.sh'

-starter.sh will start the Aggregator once it is installed.
-starter.sh can be run by a user of any privilage, but it is recommended to run it as an unprivilaged user.
-The agreggator must be started after the forwarder else there is a chance that data may be lost
