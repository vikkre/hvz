from base import db
import helper
from run_once import run_once

import endpoint.product as product
import relation.recipe_has_product as recipe_has_product


class Recipe(db.Model):
	__tablename__ = "recipe"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	text = db.Column(db.Text, nullable=True)
	products = db.relationship("RecipeHasProduct", cascade="all,save-update,delete-orphan", back_populates="recipe")
	menus = db.relationship("MenuHasRecipe", back_populates="recipe")


	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"text": self.text,
			"products": [{
				"id": product.product_id,
				"name": product.product.name,
				"amount": product.amount
			} for product in self.products]
		}


	@staticmethod
	def from_dict(data):
		name = data["name"]
		text = data["text"]
		products = data["products"]

		recipe = Recipe(name=name, text=text)

		recipe.insert_products(products)

		return recipe


	def set_value(self, value_name, value):
		if value_name == "name":
			self.name = value
		elif value_name == "text":
			self.text = value
		elif value_name == "products":
			self.products.clear()
			self.insert_products(value)


	def __repr__(self):
		return f"<Recipe {self.id}, name={self.name}>"

	
	def insert_products(self, products):
		for product_dict in products:
			product_entry = product.Product.query.get(product_dict["id"])
			amount = product_dict["amount"]

			recipe_has_product_instance = recipe_has_product.RecipeHasProduct(product=product_entry, amount=amount)
			self.products.append(recipe_has_product_instance)


@run_once
def init():
	helper.RestBase("/recipe", Recipe)
