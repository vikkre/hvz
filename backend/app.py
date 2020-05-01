from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@database/test'
db = SQLAlchemy(app)

conn = db.engine.connect()

@app.route('/')
def index():
	return "Hello World\n"

@app.route('/dbversion')
def dbversion():
	return conn.execute("select version()").fetchall()[0][0] + "\n"
