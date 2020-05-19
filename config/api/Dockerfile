FROM python:3.7-alpine

WORKDIR /code

ARG SPECIAL_REQUIREMENTS

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev
COPY requirements/requirements.txt requirements.txt
COPY requirements/${SPECIAL_REQUIREMENTS} special_requirements.txt
RUN pip install -r requirements.txt -r special_requirements.txt

CMD ["flask", "run"]
