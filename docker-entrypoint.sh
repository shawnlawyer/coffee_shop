#!/bin/bash

export TERM=xterm

if [ ! -d 'logs' ]; then

    mkdir -p logs
    mkdir -p logs/nginx
    mkdir -p logs/app

fi

cd backend

#python3 migrate.py db upgrade

cd  $HOME

sudo cp $HOME/docker/nginx-dev.conf /etc/nginx/nginx.conf

screen -dmS BACKEND bash -c 'flask run --host=0.0.0.0'

cd frontend

npm install

screen -dmS FRONTEND bash -c 'ionic serve --address=0.0.0.0 --disableHostCheck'

cd $HOME

sudo nginx

tail -f /dev/null
