# Setting up Docker for Development/Production
Installing RGUKT-Quiz Software with a Docker file

# Getting started with Docker
1. Install DockerToolbox (https://www.docker.com/toolbox)
2. Install VirtualBox (https://www.virtualbox.org/wiki/Downloads)
3. Click "Docker Quickstart Terminal" (Created on Desktop, for windows users)
4. Run: docker pull vedavyas/rgukt-quizsoftware
5. Run: docker run -p 8080:80 -e ENVIRONMENT='production' -d --name=quiz_app vedavyas/rgukt-quizsoftware
6. Run: VBoxManage controlvm default natpf1 "flask_app,tcp,127.0.0.1,8080,,8080" (Make sure that VBoxManage executable is added to path)
7. Go to localhost:8080 in your browser and you should see the homepage of Quiz Software.

# Creating your own version of this repo
1. Fork this repository. If you are a collaborator of this repo skip forking and clone this repository.
2. Create an account at Dockerhub.com
3. Click the "Create" dropdown in the far top right corner (not the "Create Repository+" button)
4. Select "Create Automated Build"
5. Link your Github account, select your user, select the github repo, etc.
6. Click the "Trigger a build" button, go to the "Build Details" tab and you should see a new build for your container.

# Testing your docker container when there are changes
1. Make a change to your Flask application (white space changes or comments are easy to test).
2. Push your change to github.
3. Go to your dockerhub account, click on your automated build repository, and click the build details tab.
4. Once the build is finished, go to Docker terminal.
5. Run: docker pull vedavyas/rgukt-quizsoftware
6. Run: docker run -p 8080:80 -e ENVIRONMENT='production' -d --name=quiz_app vedavyas/rgukt-quizsoftware
7. Go to localhost:8080 in your browser and you should see your application.