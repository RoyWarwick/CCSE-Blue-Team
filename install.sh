#DONT RUN THE SCRIPT USING SUDO IT MESSES WITH THE PIP ISNTALLS
sudo apt-get git
sudo apt install python3
git clone https://github.com/RoyWarwick/CCSE-Blue-Team.git --branch GUI	#Downloads the project
sudo chown -R $USER CCSE-Blue-Team
cd CCSE-Blue-Team
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 server.py




