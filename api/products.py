from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc


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
        if self.product is None:
            product = None
        else:
            product = self.product.to_dict()

        return {'product':product, 'status': self.status, 'error': self.error}


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
        except exc.IntegrityError:
            db.session.rollback()
            pr.status = 'failed' 
            pr.error = "product_alredy_exits"
    return jsonify([p.to_dict() for p in products])


@app.route('/products', methods=['PUT'])
def put_products():
    products = []
    for product_update in request.json:
        if "id" not in product_update:
            product_result = ProductResult(None)
            product_result.status = "failed"
            product_result.error = "id_not_provided"
            products.append(product_result)
        else:
            product_result = ProductResult(Product.query.get(product_update["id"]))

            if product_result.product is None:
                product_result.status = "failed"
                product_result.error = "product_not_found"
            else:
                if "name" in product_update:
                    product_result.product.name = product_update["name"]
                if "amount" in product_update:
                    product_result.product.amount = product_update["amount"]

                db.session.commit()
                product_result.status = 'ok'
            
            products.append(product_result)

    return jsonify([p.to_dict() for p in products])


@app.route('/products', methods=['DELETE'])
def delete_products():
    products = []
    for product_update in request.json:
        if "id" not in product_update:
            product_result = ProductResult(None)
            product_result.status = "failed"
            product_result.error = "id_not_provided"
            products.append(product_result)
        else:
            product_result = ProductResult(Product.query.get(product_update["id"]))

            if product_result.product is None:
                product_result.status = "failed"
                product_result.error = "product_not_found"
            else:
                db.session.delete(product_result.product)

                db.session.commit()
                product_result.status = 'ok'
            
            products.append(product_result)

    return jsonify([p.to_dict() for p in products])
