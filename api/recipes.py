from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc


class Recipe(db.Model):
	__tablename__ = "recipe"
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	recipe_has_product = db.relationship("RecipeHasProduct")
