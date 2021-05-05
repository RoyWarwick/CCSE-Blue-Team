sudo apt update
sudo apt install python3
sudo apt install postgresql
sudo service start postgresql
sudo -u postgres psql "-c alter user postgres with password 'password'"

pip3 install psycopg2
pip3 install tqdm
pip3 install Flask

sudo -u postgres -H -- psql "create role storage login password 'password'"
sudo -u postgres -H -- psql "create database farm owner 'storage'"

