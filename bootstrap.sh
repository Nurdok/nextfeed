#!/bin/bash

sudo apt-get install -y python-virtualenv
sudo apt-get install -y gunicorn
sudo apt-get install -y libpq-dev
sudo apt-get install -y python-dev

wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

pushd /vagrant
virtualenv --distribute venv
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
popd

