# imagen con python
FROM python:3

# label del maintainer
LABEL maintainer="darwin.castillo@jalasoft.com"

# copy the code to /opt/app folder
COPY . /opt/app
WORKDIR /opt/app

# RUN apt-get install -y git
# check credentials
# RUN git clone repo (ssh)

# update system
RUN apt-get update

# install java always add -y option
RUN apt-get install -y default-jre
RUN java -version

# install allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure_2.29.0-1_all.deb
RUN dpkg -i allure_2.29.0-1_all.deb

# install/upgrade pip
RUN python3 -m pip install --upgrade pip

# install virtualenv librarary/package
RUN python3 -m pip install --user virtualenv

# create virtualenv for the framework
RUN python3 -m venv .venv

# activate virtual environment
RUN . .venv/bin/activate

# install requirements
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pylint booker_api/ --rcfile=.pylintrc
RUN python3 -m pytest booker_api/rooms/test_rooms.py booker_api/bookings/test_bookings.py booker_api/brandings/test_brandings.py booker_api/messages/test_messages.py booker_api/reports/test_reports.py -v -s --alluredir reports/allure/results
