import flask, flask_sqlalchemy, flask_migrate, flask_cors
import sqlalchemy

import os, time


app = flask.Flask(__name__)
flask_cors.CORS(app)

database = os.environ["DATABASE"]
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin@database/" + database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = flask_sqlalchemy.SQLAlchemy(app)


def init_db():
	migrate = flask_migrate.Migrate(app, db)

	while True:
		try:
			with app.app_context():
				flask_migrate.upgrade()
				print("Upgrade successful", flush=True)
			break
		except sqlalchemy.exc.OperationalError:
			print("Connection to Database failed, retrying in", DB_CONNECTION_RETRY_WAIT_SECONDS, "seconds", flush=True)
			time.sleep(DB_CONNECTION_RETRY_WAIT_SECONDS)