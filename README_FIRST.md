For the pre-submission testing, Option A (Pre-defined Adressing Option) is desired for the network.

All of the files and documentation that are needed are here in this ("main") branch; this document provides installation instructions.

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

+---------------+
| Security Unit |
+---------------+

This component uses sensor 2 (the machine with private IPv4 address 192.168.0.4).
The machine must have GPIO pins connected to components in accordance with the diagram stored as "security/security unit circuit diagram.jpg".
The directory in this branch called "security" must be downloaded onto the machine and the "security-unit-installation.sh" file within that must be locally executed (as the superuser) as its installation script; this script requires no user input or output in order to sucessfully complete.
The script will finish by rebooting the machine and when it starts up again it will be a fully-automated unit.
** This component must either be setup after the aggregator or rebooted once the aggreagtor has been setup**

+-----------------------+
| Processor and Storage |
+-----------------------+
-This component holds an expected IP address of 192.168.255.2 consistent with the given network architecture (option A)
-Installation of this component is done by pulling all files provided within the "processor and storage" directory which will provide the relevant python code and with main files of interest: install.sh and start.sh

-install.sh will install all the relevant programs required to run the system, and will require root (use sudo) permissions to be executed
-install.sh will require internet connection
-install.sh will update all programs within the Linux environment and will further install/update Python libraries (including: psycopg2, tdqm, Flask)
-In addition, install.sh will setup the Postgres environment used as the storage component

-start.sh will start all processor and storage processes, and is recommended to be run in user mode, which will immediately startup tcp servers to receive files from the collector

NOTE: The .sh files may require a change in permissions to be able to execute them in a Linux environment, which can be done by: chmod +x <filename>.sh

+--------------------------------------+
| Processor and Storage section ending |
+--------------------------------------+

+---------------+
| Dashboard/GUI |
+---------------+

- This component holds an expected IP address of 192.168.255.3 consistent with the given network architecture (option A)
- Installation of this component is done by pulling all files provided within the "dashboard" directory which will provide the relevant python code and with main files of interest: install.sh and run.sh
- First thing in order is to change the permission of the .sh files into executables. This can be done via. 

**All of these commands should take place within the Dashboard Directory.**
```bash
chmod +x install.sh run.sh
```
- Now that is done you'll need internet access to run the following command. 	*This command should be run without sudo (However the command will require sudo privelleges for some of the execution)* 
```bash
./install.sh
```
- After that is complete you're area ready to run the server without an internet connection. This can be done via using.
```bash
./run.sh
```
- To exit/stop the server please just
```bash
CTRL + C
``` 
To break the command. 

+--------------------------------------+
|        Forwarder and Collector       |
+--------------------------------------+
-This component holds an expected IP addresses of 172.16.0.201/24,  192.168.0.254/24 for the forwarder, 172.16.0.202/24, 192.168.255.254/24 for the collector consistent, with the given network architecture (option A)
- The forwarder directory should be on forwarder machine, collector on the collector machine.
- When on each machine, the install scripts are in the scripts directory in each forwarder and collectory folder. Give the file permission by chmod +x installation_forwader.sh or chmod +x installation_collector.sh
- Now execute the install script on each machine.
./filename.sh
- Now there should be a run.sh in your home directory.
- Execute the run.sh files on both the forwarder and collector
./run.sh
- IPSEC will now be set up on both machines
- MQTT will have TLS compatability: listener and broker started on the forwarder machine
- The processes will run in background and constantly listening in on files sent to the machine via mqtt.
- Forwarder will parse the json file automatically and send it off to processor
- Forwarder machine will also send data to processor via tcp-client with IPSEC encryption.
