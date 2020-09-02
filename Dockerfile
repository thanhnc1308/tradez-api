FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/code
RUN mkdir /opt/requirements
WORKDIR /opt/code

ADD requirements /opt/requirements
# apparmor and apturl are Ubuntu packages. They must be installed via apt
#RUN apt install -y apparmor apturl python-brlapi python-commandnotfound && pip3 install -r /opt/requirements/development.txt
RUN pip3 install -r /opt/requirements/development.txt