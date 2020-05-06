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

    def to_dict(self):
        return {'product':self.product.to_dict(), 'status': self.status, 'error': self.error}


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
