if [[ $EUID != 0 ]]
then
    echo "This script must be run as the superuser." >&2
    echo "Exit status: 1" >&2
    exit 1
fi

sudo apt-get git
sudo apt install python3
git clone https://github.com/RoyWarwick/CCSE-Blue-Team.git?raw=true --branch GUI	#Downloads the project
sudo chown -R $USER CCSE-Blue-Team
cd CCSE-Blue-Team
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt




