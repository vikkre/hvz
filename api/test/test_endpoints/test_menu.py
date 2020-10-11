import unittest

from base import app, db
from endpoint.product import Product
# from endpoint.menu import Menu, init
from endpoint.menu import Menu


# init()


class TestMenu(unittest.TestCase):
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


	def test_todo(self):
		self.assertTrue(False)
