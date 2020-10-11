from base import db, app
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc, orm
import datetime

from endpoint.recipe import Recipe


menu_has_recipe = db.Table('menu_has_recipe', db.Model.metadata,
	db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
	db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

class Menu(db.Model):
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	recipes = db.relationship("Recipe", secondary=menu_has_recipe, lazy="dynamic")

	def to_dict(self):
		return {
			'id': self.id,
			'date': self.date,
			'recipes': [{"recipe_id": recipe.id} for recipe in self.recipes]
		}

	@staticmethod
	def from_dict(dict):
		return Menu(**dict)

	def __repr__(self):
		return f'<Menu {self.id}, date={self.date}>'


@dataclass
class MenuResult:
	menu: Menu = None
	status: str = None
	error: str = None

	def __init__(self, menu=None):
		self.menu = menu

	def to_dict(self):
		menu = None if self.menu is None else self.menu.to_dict()
		return {'menu': menu, 'status': self.status, 'error': self.error}


@app.route('/menus', methods=['GET'])
def get_menus():
	return jsonify([menu.to_dict() for menu in Menu.query.all()])


@app.route('/menus/<id>', methods=['GET'])
def get_menus_by_id(id):
	menu_result = MenuResult()

	try:
		menu_result.menu = Menu.query.get(id)

		if menu_result.menu is None:
			menu_result.status = "failed"
			menu_result.error = "menu_not_found"
		else:
			menu_result.status = 'ok'

	except exc.DataError:
		menu_result.status = "failed"
		menu_result.error = "id_wrong_format"

	return jsonify(menu_result.to_dict())


@app.route('/menus', methods=['POST'])
def post_menus():
	menu = request.json.copy()
	recipes = menu.pop("recipes")

	menu_result = MenuResult(Menu.from_dict(menu))
	db.session.add(menu_result.menu)
	
	try:
		for recipes_dict in recipes:
			recipe = Recipe.query.get(recipes_dict["recipe_id"])
			menu_result.menu.recipes.append(recipe)

		db.session.commit()

		menu_result.status = 'ok'
	except orm.exc.FlushError:
		db.session.rollback()

		menu_result.menu = None
		menu_result.status = 'failed' 
		menu_result.error = "recipe_does_not_exist"

	return jsonify(menu_result.to_dict())


@app.route('/menus/<id>', methods=['PUT'])
def put_menus(id):
	menu_result = MenuResult()

	try:
		menu_update = request.json
		menu_result.menu = Menu.query.get(id)

		if menu_result.menu is None:
			menu_result.status = "failed"
			menu_result.error = "menu_not_found"
		else:
			if "recipes" in menu_update:
				for recipe in menu_result.menu.recipes:
					menu_result.menu.recipes.remove(recipe)
				for recipes_dict in menu_update["recipes"]:
					recipe = Recipe.query.get(recipes_dict["recipe_id"])
					menu_result.menu.recipes.append(recipe)

			menu_result.status = 'ok'
			db.session.commit()

	except exc.IntegrityError:
		db.session.rollback()

		menu_result.status = "failed"
		menu_result.error = "recipe_does_not_exist"
	except exc.DataError:
		menu_result.status = "failed"
		menu_result.error = "id_wrong_format"

	return jsonify(menu_result.to_dict())


@app.route('/menus/<id>', methods=['DELETE'])
def delete_menus(id):
	menu_result = MenuResult()

	try:
		menu_result.menu = Menu.query.get(id)

		if menu_result.menu is None:
			menu_result.status = "failed"
			menu_result.error = "menu_not_found"
		else:
			db.session.delete(menu_result.menu)

			db.session.commit()
			menu_result.status = 'ok'

	except exc.DataError:
		menu_result.status = "failed"
		menu_result.error = "id_wrong_format"

	return jsonify(menu_result.to_dict())
