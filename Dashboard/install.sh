#DONT RUN THE SCRIPT USING SUDO IT MESSES WITH THE PIP INSTALLS
sudo apt install git
sudo apt install python3
sudo apt install python3-virtualenv
sudo chown -R $USER Dashboard
cd Dashboard
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
