# Install python image from docker hub
FROM python:3.9-alpine3.13
LABEL maintainer="cogent4it.com"
# allows not to buffer output and just display on console, better performance
ENV PYTHONUNBUFFERED 1

# copy requirements.txt local file to docker image location so that it can install packages
COPY ./requirements.txt /tmp/requirements.txt
# copy the requirements.dev.txt setting as well
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copy local app directory to docker app location
COPY ./app /app
# this is docker app directory based on that we run command and other operation
WORKDIR /app
# port at which the app is exposed in docker
EXPOSE 8000

# from line under run, it is a single run command. To break into mulitple lines, we use "&& \". Further, it does not
# contains multiple layers
# python -m venv /py && \:- create a virtual env. where we can install dependencies
# /py/bin/pip install --upgrade pip && \ :- upgrade packages using pip
# /py/bin/pip install -r /tmp/requirements.txt && \ :- install packages specified in requirements.txt resides in tmp directory
# rm -rf /tmp && \ :- remove the tmp directory
# adduser \ :- add new user in order to avoid root user, don't run app under root user to secure it. user name is: django-user
# By defult the dev arg is false, when we run docker-compose, it will be changed to true for local development
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # adding shell script, if dev arg is true, install requirements.dev.txt packages as well
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
# configure env. variable inside image, when we run any command, we don't have to specify complete path, so we defined here
ENV PATH="/py/bin:$PATH"
# declare user
USER django-user