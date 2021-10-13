### Dockerfile for SyCoFinder
# Based on https://github.com/materialscloud-org/tools-barebone/Dockerfile
# See http://phusion.github.io/baseimage-docker/ for info in phusion
# See https://hub.docker.com/r/phusion/passenger-customizable
# for the latest releases
FROM phusion/passenger-customizable:2.0.0

MAINTAINER Leopold Talirz <leopold.talirz@gmail.com>

# If you're using the 'customizable' variant, you need to explicitly opt-in
# for features. Uncomment the features you want:
#
#   Build system and git.
RUN /pd_build/utilities.sh && \
    /pd_build/python.sh 

### Installation
RUN apt-get update \
    && apt-get -y install \
    python3-pip \
    apache2 \
    libapache2-mod-wsgi-py3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean all

# Setup apache
# enable wsgi module, disable default apache site, enable our site
ADD ./.apache/apache-site.conf /etc/apache2/sites-available/app.conf
RUN a2enmod wsgi && \
    a2dissite 000-default && a2ensite app

# Run this as root to replace the version of pip
RUN pip3 install --upgrade pip setuptools wheel

# Activate apache at startup
RUN mkdir /etc/service/apache
ADD ./.apache/apache_run.sh /etc/service/apache/run

## pymc build requirements: gfortran, liblapack-dev, numpy
#RUN apt-get -y install python-pip gfortran liblapack-dev
#RUN pip install --upgrade pip numpy 

# from now on run as user app, provided by passenger
USER app
ENV HOME /home/app
WORKDIR /home/app

# Add wsgi file for app
COPY ./.apache/app.wsgi app.wsgi

COPY sycofinder/ ./sycofinder
COPY README.md setup.py setup.json  ./
RUN pip install --user --no-warn-script-location -e .

# go back to root user for startup
USER root
RUN chown -R app:app /home/app

# run apache server (via baseimage-docker's init system)
EXPOSE 80
CMD ["/sbin/my_init"]
