#DONT RUN THE SCRIPT USING SUDO IT MESSES WITH THE PIP INSTALLS
sudo apt install git
sudo apt install python3
sudo apt install python3-virtualenv
git clone https://github.com/RoyWarwick/CCSE-Blue-Team.git --branch GUI	#Downloads the project
sudo chown -R $USER CCSE-Blue-Team
cd CCSE-Blue-Team
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 server.py




