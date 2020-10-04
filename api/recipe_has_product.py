from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc


class RecipeHasProduct(db.Model):
	__tablename__ = "recipe_has_product"
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
	amount = db.Column(db.Integer, nullable=False)
	product = db.relationship("Product")

	def to_dict(self):
		return {
			'product_id': self.product_id,
			'product_name': self.product.name,
			'recipe_id': self.recipe_id,
			'amount': self.amount
		}

	@staticmethod
	def from_dict(dict):
		return RecipeHasProduct(**dict)

	def __repr__(self):
		return f'<RecipeHasProduct ({self.product_id},{self.recipe_id}), amount={self.amount}>'
