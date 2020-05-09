from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

database = os.environ["DATABASE"]
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin@database/" + database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import products

db.create_all()

@app.route('/')
def index():
    return "Hello World\n"
