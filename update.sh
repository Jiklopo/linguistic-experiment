#!/bin/bash

echo 'Pulling'
git pull
echo '#############################'

echo 'Installing pip packages'
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt
echo '#############################'

echo 'Migrating'
venv/bin/python manage.py migrate
echo '#############################'

echo 'Compiling messages'
venv/bin/python manage.py compilemessages
echo '#############################'

echo 'Collecting static files'
venv/bin/python manage.py collectstatic --noinput
echo '#############################'

echo 'Restarting gunicorn service'
sudo systemctl restart gunicorn

echo 'Done.'
