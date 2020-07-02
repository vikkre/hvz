from app import app, db
from flask import request, jsonify
from dataclasses import dataclass
from sqlalchemy import exc
from recipe_has_product import RecipeHasProduct


class Recipe(db.Model):
	__tablename__ = "recipe"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	text = db.Column(db.Text, nullable=True)
	recipe_has_product = db.relationship("RecipeHasProduct", cascade="all,delete")

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'text': self.text,
			'required_products': [req_product.to_dict() for req_product in self.recipe_has_product]
		}

	@staticmethod
	def from_dict(dict):
		return Recipe(**dict)

	def __repr__(self):
		return f'<Recipe {self.id}>'


@dataclass
class RecipeResult:
	recipe: Recipe = None
	status: str = None
	error: str = None

	def __init__(self, recipe=None):
		self.recipe = recipe

	def to_dict(self):
		recipe = None if self.recipe is None else self.recipe.to_dict()
		return {'recipe': recipe, 'status': self.status, 'error': self.error}


@app.route('/recipes', methods=['GET'])
def get_recipes():
	return jsonify([recipe.to_dict() for recipe in Recipe.query.all()])


@app.route('/recipes/<id>', methods=['GET'])
def get_recipes_by_id(id):
	recipe_result = RecipeResult()

	try:
		recipe_result.recipe = Recipe.query.get(id)

		if recipe_result.recipe is None:
			recipe_result.status = "failed"
			recipe_result.error = "recipe_not_found"
		else:
			recipe_result.status = 'ok'

	except exc.DataError:
		recipe_result.status = "failed"
		recipe_result.error = "id_wrong_format"

	return jsonify(recipe_result.to_dict())


@app.route('/recipes', methods=['POST'])
def post_recipes():
	recipe = request.json.copy()
	required_products = recipe.pop("required_products")

	recipe_result = RecipeResult(Recipe.from_dict(recipe))
	db.session.add(recipe_result.recipe)

	try:
		db.session.commit()
	except exc.IntegrityError:
		db.session.rollback()
		recipe_result.status = 'failed' 
		recipe_result.error = "recipe_alredy_exits"
	else:
		for required_product_dict in required_products:
			required_product_dict["recipe_id"] = recipe_result.recipe.id
			required_product = RecipeHasProduct.from_dict(required_product_dict)
			db.session.add(required_product)
		
		try:
			db.session.commit()
		except exc.IntegrityError:
			db.session.rollback()

			db.session.delete(recipe_result.recipe)
			db.session.commit()

			recipe_result.status = 'failed' 
			recipe_result.error = "product_does_not_exist"
		else:
			recipe_result.status = 'ok'

	return jsonify(recipe_result.to_dict())


@app.route('/recipes/<id>', methods=['PUT'])
def put_recipes(id):
	recipe_result = RecipeResult()

	try:
		recipe_update = request.json
		recipe_result.recipe = Recipe.query.get(id)

		if recipe_result.recipe is None:
			recipe_result.status = "failed"
			recipe_result.error = "recipe_not_found"
		else:
			if "name" in recipe_update:
				recipe_result.recipe.name = recipe_update["name"]
			if "text" in recipe_update:
				recipe_result.recipe.text = recipe_update["text"]
			
			if "required_products" in recipe_update:
				for required_product in recipe_result.recipe.recipe_has_product:
					db.session.delete(required_product)
				for required_product_dict in recipe_update["required_products"]:
					required_product_dict["recipe_id"] = recipe_result.recipe.id
					required_product = RecipeHasProduct.from_dict(required_product_dict)
					db.session.add(required_product)

			recipe_result.status = 'ok'
			db.session.commit()

	except exc.IntegrityError:
		db.session.rollback()

		recipe_result.status = "failed"
		recipe_result.error = "product_does_not_exist"
	except exc.DataError:
		recipe_result.status = "failed"
		recipe_result.error = "id_wrong_format"

	return jsonify(recipe_result.to_dict())


@app.route('/recipes/<id>', methods=['DELETE'])
def delete_recipes(id):
	recipe_result = RecipeResult()

	try:
		recipe_result.recipe = Recipe.query.get(id)

		if recipe_result.recipe is None:
			recipe_result.status = "failed"
			recipe_result.error = "recipe_not_found"
		else:
			db.session.delete(recipe_result.recipe)

			db.session.commit()
			recipe_result.status = 'ok'

	except exc.DataError:
		recipe_result.status = "failed"
		recipe_result.error = "id_wrong_format"

	return jsonify(recipe_result.to_dict())
