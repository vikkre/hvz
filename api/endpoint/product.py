import sqlalchemy

from base import db
import helper
from run_once import run_once

import endpoint.menu as menu


class Product(db.Model):
	__tablename__ = "product"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	required_amount = db.Column(db.Integer, nullable=False, server_default="0")
	recipes = db.relationship("RecipeHasProduct", back_populates="product")

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"amount": self.amount,
			"required_amount": self.required_amount,
			"needed_amount": self.get_needed_amount()
		}


	@staticmethod
	def from_dict(data):
		name = data["name"]
		amount = data["amount"]
		required_amount = data["required_amount"]
		
		return Product(name=name, amount=amount, required_amount=required_amount)


	def set_value(self, value_name, value):
		if value_name == "name":
			self.name = value
		elif value_name == "amount":
			self.amount = value
		elif value_name == "required_amount":
			self.required_amount = value


	def __repr__(self):
		return f"<Product {self.id}, name={self.name}, amount={self.amount}, required_amount={self.required_amount}>"


	def get_needed_amount(self):
		menus = menu.Menu.query.order_by(sqlalchemy.desc("date")).limit(1)
		try:
			current_menu = menus[0]
			need = 0

			for recipe in current_menu.recipes:
				for product in recipe.recipe.products:
					if product.product_id == self.id:
						need += product.amount

			return max(self.required_amount - self.amount + need, 0)
		except IndexError:
			return max(self.required_amount - self.amount, 0)


@run_once
def init():
	helper.RestBase("/product", Product)
