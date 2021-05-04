Step 0.1) Requires aggregator to be already running

Step 1) run install.sh as sudo (Internet required) (Might take a while, it is updating and upgrading the tools)
sudo ./install.sh

Step 2) Hopefully it works.
Install.sh makes the Pi reboot.
The Environment.py script should automatically run on startup.
The Py script is listening for a topic to publish to.
The LEDs should light up if thresholds are passed even if a topis is not specified. 
When it is received, it should start publishing to aggregator and displaying values and information to terminal.