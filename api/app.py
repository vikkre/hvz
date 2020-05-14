from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
import os
import time


DB_CONNECTION_RETRY_WAIT_SECONDS = 5


app = Flask(__name__)
CORS(app)

database = os.environ["DATABASE"]
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin@database/" + database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


import products


try_connect = True
while try_connect:
    try:
        db.create_all()
        try_connect = False
    except OperationalError:
        print("Connection to Database failed, retrying in", DB_CONNECTION_RETRY_WAIT_SECONDS, "seconds")
        time.sleep(DB_CONNECTION_RETRY_WAIT_SECONDS)


@app.route('/')
def index():
    return "Hello World\n"
