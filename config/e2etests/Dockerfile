FROM python:3.8-alpine

WORKDIR /code

RUN apk add --no-cache \
  gcc \
  linux-headers \
  musl-dev \ 
  postgresql-dev

COPY ./frontend/requirements.txt /code
RUN pip3 install -r requirements.txt
