import unittest

from base import app, db

from endpoint.product import Product
from endpoint.recipe import Recipe
from endpoint.menu import Menu
from relation.recipe_has_product import RecipeHasProduct
from relation.menu_has_recipe import MenuHasRecipe

import endpoint_setup
import datetime


class TestProduct(unittest.TestCase):
	def setUp(self):
		app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
		app.config["TESTING"] = True
		app.testing = True

		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

		db.create_all()

		self.apple = Product(name="apple", amount=10, required_amount=5)
		self.bread = Product(name="bread", amount=0, required_amount=2)

		self.apple_bread = Recipe(name="Apple Bread", text="put apple on bread")
		self.cut_apple = Recipe(name="Cut Apple", text="cut apple into slices")

		self.this_week_date = datetime.datetime.now()
		self.last_week_date = self.this_week_date - datetime.timedelta(days=7)

		self.this_week = Menu(date=self.this_week_date)
		self.last_week = Menu(date=self.last_week_date)

		self.apple_bread.products.append(RecipeHasProduct(product=self.apple, amount=2))
		self.apple_bread.products.append(RecipeHasProduct(product=self.bread, amount=3))
		self.cut_apple.products.append(RecipeHasProduct(product=self.apple, amount=15))

		self.this_week.recipes.append(MenuHasRecipe(recipe=self.apple_bread))
		self.last_week.recipes.append(MenuHasRecipe(recipe=self.apple_bread))
		self.last_week.recipes.append(MenuHasRecipe(recipe=self.cut_apple))

		db.session.add(self.apple)
		db.session.add(self.bread)

		db.session.commit()

		self.client = app.test_client()


	def tearDown(self):
		db.session.rollback()
		db.drop_all()


	def test_to_dict(self):
		expected = {
			"id": self.apple.id,
			"name": "apple",
			"amount": 10,
			"required_amount": 5,
			"needed_amount": 0
		}

		self.assertCountEqual(expected, self.apple.to_dict())


	def test_from_dict(self):
		data = {
			"name": "onion",
			"amount": 4,
			"required_amount": 5
		}

		result = Product.from_dict(data)
		self.assertEqual(data["name"], result.name)
		self.assertEqual(data["amount"], result.amount)
		self.assertEqual(data["required_amount"], result.required_amount)

	
	def test_from_dict_missing_key(self):
		self.assertRaises(KeyError, Product.from_dict, {})


	def test_set_value(self):
		value = 4

		self.bread.set_value("amount", value)
		self.assertEqual(value, self.bread.amount)

	
	def test_get_needed_amount(self):
		apple_needed_amount = self.apple.get_needed_amount()
		self.assertEqual(0, apple_needed_amount)

		bread_needed_amount = self.bread.get_needed_amount()
		self.assertEqual(5, bread_needed_amount)


	def test_get_needed_amount_no_menu(self):
		db.session.delete(self.this_week)
		db.session.delete(self.last_week)
		db.session.commit

		apple_needed_amount = self.apple.get_needed_amount()
		self.assertEqual(0, apple_needed_amount)

		bread_needed_amount = self.bread.get_needed_amount()
		self.assertEqual(2, bread_needed_amount)
