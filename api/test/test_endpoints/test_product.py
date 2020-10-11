import unittest

from base import app, db
from endpoint.product import Product
import endpoint_setup


class TestProduct(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		app.testing = True

		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

		db.create_all()

		self.apple = Product(name="apple", amount=10, required_amount=5)
		self.bread = Product(name="bread", amount=0, required_amount=2)

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
		self.assertEqual(2, bread_needed_amount)
