
# to run:
#    * docker build --tag imdea-control-python .
#    * docker run --interactive --rm --tty imdea-control-python bash

FROM ubuntu:16.04

MAINTAINER svg153
# version

# GLOBAL ENV VARS
# https://github.com/phusion/baseimage-docker/issues/58
ENV DEBIAN_FRONTEND noninteractives

RUN apt-get update > /dev/null 2>&1
RUN apt-get install -y sudo apt-utils > /dev/null 2>&1

RUN mkdir -p /home/user
WORKDIR /home/user

# COPY files
ADD ./install.sh .
ADD ./control.py .
ADD ./.credentials.template .
ADD ./.credentials .

RUN chmod +x ./install.sh
RUN ./install.sh

RUN python ./control.py -b 100

RUN rm ./.credentials
