### Docker base specific
# See http://phusion.github.io/baseimage-docker/ for info in phusion
# See https://github.com/phusion/baseimage-docker/releases
# for the latest releases
FROM phusion/passenger-customizable:1.0.1

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

RUN apt-get -y install python-pip
RUN pip install --upgrade pip
## pymc build requirements: gfortran, liblapack-dev, numpy
#RUN apt-get -y install python-pip gfortran liblapack-dev
#RUN pip install --upgrade pip numpy 

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /home/app
COPY sycofinder/ ./sycofinder
COPY static/ ./static
COPY README.md setup.py setup.json run.py  ./
RUN pip install -e .

# from now on run as user app, provided by passenger
RUN chown -R app:app /home/app
USER app

# expose default dash port
EXPOSE 8050

# Use baseimage-docker's init system.
#CMD ["/sbin/my_init"]
CMD ["python", "run.py"]

