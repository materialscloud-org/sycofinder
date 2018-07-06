### Docker base specific
# See http://phusion.github.io/baseimage-docker/ for info in phusion
# See https://github.com/phusion/baseimage-docker/releases
# for the latest releases
FROM phusion/passenger-customizable:0.9.34

MAINTAINER Leopold Talirz <leopold.talirz@gmail.com>


# If you're using the 'customizable' variant, you need to explicitly opt-in
# for features. Uncomment the features you want:
#
#   Build system and git.
#   Python support (2.7 and 3.x - it is 3.5.x in this ubuntu 16.04)
RUN /pd_build/utilities.sh && \
    /pd_build/python.sh 

### Installation
RUN apt-get update

# pymc build requirements: gfortran, liblapack-dev, numpy
RUN apt-get -y install python-pip gfortran liblapack-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --upgrade pip numpy 

WORKDIR /home/app
COPY maxdiv/ ./maxdiv
COPY README.md setup.py setup.json run.py  ./
# pymc: numpy already required at build time
RUN pip install -e .

# from now on run as user app, provided by passenger
RUN chown -R app:app /home/app
USER app

# expose default dash port
EXPOSE 8050

# Use baseimage-docker's init system.
#CMD ["/sbin/my_init"]
CMD ["python", "run.py"]

