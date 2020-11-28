FROM python:3.7-alpine

WORKDIR /code

ARG SPECIAL_REQUIREMENTS

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev
COPY config/api/requirements/requirements.txt requirements.txt
COPY config/api/requirements/${SPECIAL_REQUIREMENTS} special_requirements.txt
RUN pip install -r requirements.txt -r special_requirements.txt

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY ./config/api/app.ini /code
COPY ./api /code
RUN rm -rf /code/test

CMD ["flask", "run"]
