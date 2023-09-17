# pull official base image
FROM python:3.8.5-slim-buster

# set work directory
WORKDIR /service

# install nginx
RUN apt-get update && apt-get -y install nginx

# install pipenv
RUN pip install --upgrade pipenv

COPY nginx.conf /etc/nginx/nginx.conf

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile /service/Pipfile
COPY Pipfile.lock /service/Pipfile.lock
RUN pipenv install --system --deploy

# copy project
COPY . /service/

CMD ["/bin/bash", "/service/entrypoint.sh"]