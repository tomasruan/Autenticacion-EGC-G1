#!/usr/bin/env bash

if [ "$TRAVIS_BRANCH" = "master" ]
	then
		docker build -t login_egc .

		export DOCKER_ID_USER=$DOCKER_USER

		docker login --username=$DOCKER_USER --password=$DOCKER_PASSWORD

		docker tag login_egc $DOCKER_ID_USER/login_egc

		docker push $DOCKER_ID_USER/login_egc

fi

if [ "$TRAVIS_BRANCH" = "develop" ]
	then
		echo "No es la rama master."

fi