from base import db
import helper
from run_once import run_once

import datetime

import endpoint.recipe as recipe
import relation.menu_has_recipe as menu_has_recipe


class Menu(db.Model):
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	recipes = db.relationship("MenuHasRecipe", cascade="all,save-update,delete-orphan", back_populates="menu")


	def to_dict(self):
		return {
			"id": self.id,
			"date": self.date,
			"recipes": [{
				"id": recipe.recipe_id,
				"name": recipe.recipe.name
			} for recipe in self.recipes]
		}


	@staticmethod
	def from_dict(data):
		recipes = data["recipes"]

		menu = Menu()

		menu.insert_recipes(recipes)

		return menu

	
	def set_value(self, value_name, value):
		if value_name == "recipes":
			self.recipes.clear()
			self.insert_recipes(value)


	def __repr__(self):
		return f"<Menu {self.id}, date={self.date}>"


	def insert_recipes(self, recipes):
		for recipe_dict in recipes:
			recipe_entry = recipe.Recipe.query.get(recipe_dict["id"])

			menu_has_recipe_instance = menu_has_recipe.MenuHasRecipe(recipe=recipe_entry)
			self.recipes.append(menu_has_recipe_instance)


@run_once
def init():
	# deprecated: /menus
	helper.RestBase("/menus", Menu, data_name="menu")
	helper.RestBase("/menu", Menu, data_name="menu")
