from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
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
migrate = Migrate(app, db)

import products, recipes, recipe_has_product, menus


# db.create_all()
while True:
	try:
		with app.app_context():
			upgrade()
			print("Upgrade successful", flush=True)
		break
	except OperationalError:
		print("Connection to Database failed, retrying in", DB_CONNECTION_RETRY_WAIT_SECONDS, "seconds", flush=True)
		time.sleep(DB_CONNECTION_RETRY_WAIT_SECONDS)
	except Exception as e:
		raise e

@app.route('/')
def index():
	return "Hello World!\n"
