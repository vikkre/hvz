from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
import datetime


menu_has_recipe = db.Table('menu_has_recipe', db.Model.metadata,
	db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
	db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

class Menu(db.Model):
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	recipes = db.relationship("Recipe", secondary=menu_has_recipe)
