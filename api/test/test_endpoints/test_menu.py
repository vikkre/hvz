import unittest

from base import app, db

from endpoint.recipe import Recipe
from relation.menu_has_recipe import MenuHasRecipe
from endpoint.menu import Menu, init

import datetime


init()


class TestMenu(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		app.testing = True

		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

		db.create_all()

		self.apple_bread = Recipe(name="Apple Bread", text="put apple on bread")
		self.cut_apple = Recipe(name="Cut Apple", text="cut apple into slices")

		self.this_week_date = datetime.datetime.now()
		self.last_week_date = self.this_week_date - datetime.timedelta(days=7)

		self.this_week = Menu(date=self.this_week_date)
		self.last_week = Menu(date=self.last_week_date)

		self.this_week.recipes.append(MenuHasRecipe(recipe=self.apple_bread))
		self.last_week.recipes.append(MenuHasRecipe(recipe=self.apple_bread))
		self.last_week.recipes.append(MenuHasRecipe(recipe=self.cut_apple))

		db.session.add(self.apple_bread)
		db.session.add(self.cut_apple)

		db.session.add(self.last_week)
		db.session.add(self.this_week)

		db.session.commit()

		self.client = app.test_client()


	def tearDown(self):
		db.session.rollback()
		db.drop_all()


	def test_to_dict(self):
		expected = {
			"id": self.this_week.id,
			"date": self.this_week_date,
			"recipes": [
				{
					"id": self.apple_bread.id,
					"name": "Apple Bread"
				}
			]
		}

		self.assertCountEqual(expected, self.this_week.to_dict())


	def test_from_dict(self):
		data = {
			"recipes": [
				{
					"id": self.cut_apple.id
				}
			]
		}

		result = Menu.from_dict(data)
		db.session.add(result)
		db.session.commit()

		self.assertIsNotNone(result.date)
		self.assertEqual(data["recipes"][0]["id"], result.recipes[0].recipe_id)

	
	def test_from_dict_missing_key(self):
		self.assertRaises(KeyError, Recipe.from_dict, {})

	
	def test_set_value_relation(self):
		value = [
			{
				"id": self.cut_apple.id
			}
		]

		self.last_week.set_value("recipes", value)
		db.session.commit()

		self.assertEqual(1, len(self.last_week.recipes))
		self.assertEqual(self.cut_apple.id, self.last_week.recipes[0].recipe_id)
