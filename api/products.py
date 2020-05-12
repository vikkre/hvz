from app import app, db
from flask import request, jsonify
from dataclasses import dataclass


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

    def __init__(self, product):
        self.product = product

    def to_dict(self):
        return {'product':self.product.to_dict(), 'status': self.status, 'error': self.error}


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([p.to_dict() for p in Product.query.all()])


@app.route('/products', methods=['POST'])
def post_products():
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
            pr.error = "product_alredy_exits"
    return jsonify([p.to_dict() for p in products])


@app.route('/products', methods=['PUT'])
def put_products():
    products = []
    for product_update in request.json:
        product_result = ProductResult(Product.query.get(product_update["id"]))
        products.append(product_result)

        if "name" in product_update:
            product_result.product.name = product_update["name"]
        if "amount" in product_update:
            product_result.product.amount = product_update["amount"]

        db.session.commit()
        product_result.status = 'ok'

    return jsonify([p.to_dict() for p in products])


@app.route('/products', methods=['DELETE'])
def delete_products():
    products = []
    for product_update in request.json:
        product_result = ProductResult(Product.query.get(product_update["id"]))
        db.session.delete(product_result.product)

        db.session.commit()
        product_result.status = 'ok'
        products.append(product_result)

    return jsonify([p.to_dict() for p in products])
