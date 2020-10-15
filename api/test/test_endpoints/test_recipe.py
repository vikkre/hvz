import unittest

from base import app, db

from endpoint.recipe import Recipe, init
from relation.recipe_has_product import RecipeHasProduct
from endpoint.product import Product


init()


class TestRecipe(unittest.TestCase):
	def setUp(self):
		app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
		app.config["TESTING"] = True
		app.testing = True

		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

		db.create_all()

		self.apple = Product(name="Apple", amount=10, required_amount=5)
		self.bread = Product(name="Bread", amount=0, required_amount=2)

		self.apple_bread = Recipe(name="Apple Bread", text="put apple on bread")
		self.cut_apple = Recipe(name="Cut Apple", text="cut apple into slices")

		self.apple_bread.products.append(RecipeHasProduct(product=self.apple, amount=2))
		self.apple_bread.products.append(RecipeHasProduct(product=self.bread, amount=1))
		self.cut_apple.products.append(RecipeHasProduct(product=self.apple, amount=1))

		db.session.add(self.apple)
		db.session.add(self.bread)

		db.session.add(self.apple_bread)
		db.session.add(self.cut_apple)

		db.session.commit()

		self.client = app.test_client()


	def tearDown(self):
		db.session.rollback()
		db.drop_all()


	def test_to_dict(self):
		expected = {
			"id": self.cut_apple.id,
			"name": "Cut Apple",
			"text": "cut apple into slices",
			"products": [
				{
					"id": self.apple.id,
					"name": "Apple",
					"amount": 1
				}
			]
		}

		self.assertCountEqual(expected, self.cut_apple.to_dict())


	def test_from_dict(self):
		data = {
			"name": "Bread Slice",
			"text": "slice bread",
			"products": [
				{
					"id": self.bread.id,
					"amount": 1
				}
			]
		}

		result = Recipe.from_dict(data)
		db.session.add(result)
		db.session.commit()

		self.assertEqual(data["name"], result.name)
		self.assertEqual(data["text"], result.text)
		self.assertEqual(data["products"][0]["id"], result.products[0].product_id)
		self.assertEqual(data["products"][0]["amount"], result.products[0].amount)

	
	def test_from_dict_missing_key(self):
		self.assertRaises(KeyError, Recipe.from_dict, {})


	def test_set_value(self):
		value = "Apple CUT"

		self.cut_apple.set_value("text", value)
		self.assertEqual(value, self.cut_apple.text)

	
	def test_set_value_relation(self):
		value = [
			{
				"id": self.bread.id,
				"amount": 2
			}
		]

		self.cut_apple.set_value("products", value)
		db.session.commit()

		self.assertEqual(1, len(self.cut_apple.products))
		self.assertEqual(self.bread.id, self.cut_apple.products[0].product_id)
		self.assertEqual(2, self.cut_apple.products[0].amount)
