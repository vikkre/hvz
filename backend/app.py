from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dataclasses import dataclass


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@database/test'
db_override = getenv('SQLALCHEMY_DATABASE_URI')
if db_override:
    print('db_override: ', db_override)
    # 'postgresql://postgres:postgres@localhost/postgres'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_override
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'amount': self.amount}

    @staticmethod
    def from_dict(dict):
        return Product(**dict)

    def __repr__(self):
        return f'<Product {self.name}, amount={self.amount}>'


@dataclass
class ProductResult:
    product: Product = None
    status: str = None
    error: str = None

    def to_dict(self):
        return {'product':self.product.to_dict(), 'status': self.status, 'error': self.error}


db.drop_all()
db.create_all()

milch = Product(name='Milch, 1l', amount=5)
burger = Product(name='Burger', amount=50)

db.session.add(milch)
db.session.add(burger)
db.session.commit()


@app.route('/')
def index():
    return "Hello World\n"


@app.route('/dbversion')
def dbversion():
    return db.engine.execute("select version()").fetchall()[0][0] + "\n"


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        products = []
        for jp in request.json:
            pr = ProductResult(Product.from_dict(jp))
            products.append(pr)
            db.session.add(pr.product)
            try:
                db.session.commit()
                pr.status = 'ok'
            except Exception as e :
                db.session.rollback()
                pr.status = 'failed' 
                pr.error = str(e)
        return jsonify([p.to_dict() for p in products])
    else:
        return jsonify([p.to_dict() for p in Product.query.all()])
