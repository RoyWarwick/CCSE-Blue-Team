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

Step 0.1) Requires aggregator to be already running

Step 1) run install.sh as sudo (Internet required) (Might take a while, it is updating and upgrading the tools)
sudo ./install.sh

Step 2) Hopefully it works.
install.sh makes the Pi reboot.
The Environment.py script should automatically run on startup.
The Py script is listening for a topic to publish to.
The LEDs should light up if thresholds are passed even if a topis is not specified. 
When it is received, it should start publishing to aggregator and displaying values and information to terminal.

Troubleshooting:
1) If DHT sensor does not work with the library installed from the install.sh script, please download it from this link ( https://github.com/adafruit/Adafruit_Python_DHT ) and run the setup.py from there. 
2) If the Environment.py does not start upon rebooting, please run it manually. (can check if it is running with    ps -aef | grep python   )
