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
