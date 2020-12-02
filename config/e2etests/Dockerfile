FROM python:3.8-alpine

WORKDIR /frontend

RUN apk add --no-cache \
  gcc \
  linux-headers \
  musl-dev \ 
  postgresql-dev

COPY ./frontend /frontend
RUN pip3 install  --disable-pip-version-check -r requirements.txt

CMD pytest -v | tee /frontend/pytest-results-$(date +%Y-%m-%d-%H-%M-%S).txt