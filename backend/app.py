from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@database/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import products

@app.route('/')
def index():
    return "Hello World\n"
