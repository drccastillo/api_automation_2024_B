FROM jenkins/jenkins:latest

# label del maintainer
LABEL maintainer="edwin.taquichiri@jalasoft.com"

# copy the code to /opt/app folder
COPY . /opt/app
WORKDIR /opt/app

USER root

# Instalar wget
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install java always add -y option
RUN apt-get update && \
    apt-get install -y wget default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure_2.29.0-1_all.deb
RUN dpkg -i allure_2.29.0-1_all.deb


USER jenkins
