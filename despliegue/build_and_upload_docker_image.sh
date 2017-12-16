#!/usr/bin/env bash

cd ..

docker build -t login_egc .

export DOCKER_ID_USER=$USER

docker login --username=$USER --password=$PASSWORD

docker tag login_egc $DOCKER_ID_USER/login_egc

docker push $DOCKER_ID_USER/login_egc