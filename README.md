# CCSE-Blue-Team
# Installation instructions
Make sure you're using a fresh install ubuntu machine

### Type the following into the terminal
1. wget https://github.com/RoyWarwick/CCSE-Blue-Team/blob/GUI/install.sh?raw=true -O install_script
2. chmod +x install_script
3. ./install_script 
#### follow the installation wizards for the dependencies (if any)
+  Once completed, go to your browser of choice and write **localhost:5000** in the url
+ It's worth noting once you run the install script it will start hosting the website immediately.


##How to host the website once installation has already taken place
In the directory that you used to install the project use the following commands in the terminal
1. cd CCSE-Blue-Team
2. source ./venv/bin/activate
3. python3 server.py
###This will start hosting the website locally
+  Type **localhost:5000** in the url of the browser of your choice