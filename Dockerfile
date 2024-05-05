FROM jenkins/jenkins:latest

USER root
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Allure Command Line
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.29.0/allure-commandline-2.29.0.zip && \
    unzip allure-commandline-2.29.0.zip -d /opt && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure && \
    rm allure-commandline-2.29.0.zip

USER jenkins
