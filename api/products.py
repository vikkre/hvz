from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc

import helper


class Product(db.Model):
	__tablename__ = "product"
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

	def set_value(self, value_name, value):
		if value_name == "name":
			self.name = value
		if value_name == "amount":
			self.amount = value
		if value_name == "required_amount":
			self.required_amount = value

	def get_needed_amount(self):
		return max(self.required_amount - self.amount, 0)

	@staticmethod
	def from_dict(dict):
		return Product(**dict)

	def __repr__(self):
		return f'<Product {self.name}, amount={self.amount}, required_amount={self.required_amount}>'


@dataclass
class ProductResult:
	data: Product = None
	status: str = None
	error: str = None

	def __init__(self, data=None):
		self.data = data

	def to_dict(self):
		data = None if self.data is None else self.data.to_dict()
		return {'product': data, 'status': self.status, 'error': self.error}


@app.route('/products', methods=['GET'])
def get_products():
	return helper.get_all(Product)


@app.route('/products/<id>', methods=['GET'])
def get_products_by_id(id):
	return helper.get_by_id(id, Product, ProductResult)


@app.route('/products', methods=['POST'])
def post_products():
	return helper.post(request.json, Product, ProductResult)


@app.route('/products/<id>', methods=['PUT'])
def put_products(id):
	return helper.put_by_id(id, request.json, Product, ProductResult)


@app.route('/products/<id>', methods=['DELETE'])
def delete_products(id):
	return helper.delete_by_id(id, Product, ProductResult)
