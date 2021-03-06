from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    required_amount = db.Column(db.Integer, nullable=False, server_default='0')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'required_amount': self.required_amount,
            'needed_amount': self.get_needed_amount()
        }

    def get_needed_amount(self):
        return max(self.required_amount - self.amount, 0)

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

    def __init__(self, product=None):
        self.product = product

    def to_dict(self):
        product = None if self.product is None else self.product.to_dict()
        return {'product': product, 'status': self.status, 'error': self.error}


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([p.to_dict() for p in Product.query.all()])


@app.route('/products/<id>', methods=['GET'])
def get_products_by_id(id):
    product_result = ProductResult()

    try:
        product_result.product = Product.query.get(id)

        if product_result.product is None:
            product_result.status = "failed"
            product_result.error = "product_not_found"
        else:
            product_result.status = 'ok'

    except exc.DatabaseError:
        product_result.status = "failed"
        product_result.error = "id_wrong_format"

    return jsonify(product_result.to_dict())


@app.route('/products', methods=['POST'])
def post_products():
    product_result = ProductResult(Product.from_dict(request.json))
    db.session.add(product_result.product)

    try:
        db.session.commit()
        product_result.status = 'ok'
    except exc.IntegrityError as error:
        db.session.rollback()
        product_result.status = 'failed' 
        product_result.error = "product_alredy_exits"

    return jsonify(product_result.to_dict())


@app.route('/products/<id>', methods=['PUT'])
def put_products(id):
    product_result = ProductResult()

    try:
        product_update = request.json
        product_result.product = Product.query.get(id)

        if product_result.product is None:
            product_result.status = "failed"
            product_result.error = "product_not_found"
        else:
            if "name" in product_update:
                product_result.product.name = product_update["name"]
            if "amount" in product_update:
                product_result.product.amount = product_update["amount"]
            if "required_amount" in product_update:
                product_result.product.required_amount = product_update["required_amount"]

            product_result.status = 'ok'
            db.session.commit()

    except exc.DatabaseError:
        product_result.status = "failed"
        product_result.error = "id_wrong_format"

    return jsonify(product_result.to_dict())


@app.route('/products/<id>', methods=['DELETE'])
def delete_products(id):
    product_result = ProductResult()

    try:
        product_result.product = Product.query.get(id)

        if product_result.product is None:
            product_result.status = "failed"
            product_result.error = "product_not_found"
        else:
            db.session.delete(product_result.product)

            db.session.commit()
            product_result.status = 'ok'

    except exc.DatabaseError:
        product_result.status = "failed"
        product_result.error = "id_wrong_format"

    return jsonify(product_result.to_dict())
