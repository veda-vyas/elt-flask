# Setting up Docker for Development/Production
Installing RGUKT-Quiz Software with a Docker file

# Getting started with Docker
## Install DockerToolbox (https://www.docker.com/toolbox)
## Install VirtualBox (https://www.virtualbox.org/wiki/Downloads)
## Click "Docker Quickstart Terminal" (Created on Desktop, for windows users)
## Run: docker pull vedavyas/rgukt-quizsoftware
## Run: docker run -p 8080:80 -e ENVIRONMENT='production' -d --name=quiz_app vedavyas/rgukt-quizsoftware
## Run: VBoxManage controlvm default natpf1 "flask_app,tcp,127.0.0.1,8080,,8080" (Make sure that VBoxManage executable is added to path)
## Go to localhost:8080 in your browser and you should see the homepage of Quiz Software.

# Creating your own version of this repo
## Fork this repository. If you are a collaborator of this repo skip forking and clone this repository.
## Create an account at Dockerhub.com
## Click the "Create" dropdown in the far top right corner (not the "Create Repository+" button)
## Select "Create Automated Build"
## Link your Github account, select your user, select the github repo, etc.
## Click the "Trigger a build" button, go to the "Build Details" tab and you should see a new build for your container.

# Testing your docker container when there are changes
## Make a change to your Flask application (white space changes or comments are easy to test).
## Push your change to github.
## Go to your dockerhub account, click on your automated build repository, and click the build details tab.
## Once the build is finished, go to Docker terminal.
## Run: docker pull vedavyas/rgukt-quizsoftware
## Run: docker run -p 8080:80 -e ENVIRONMENT='production' -d --name=quiz_app vedavyas/rgukt-quizsoftware
## Go to localhost:8080 in your browser and you should see your application.