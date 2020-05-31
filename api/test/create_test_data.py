from app import db
from products import Product


def create_test_data():
	db.drop_all()
	db.create_all()

	milch = Product(name='Milch', amount=5, required_amount=10)
	burger = Product(name='Burger', amount=50, required_amount=40)

	db.session.add(milch)
	db.session.add(burger)
	db.session.commit()

	return [
		milch.to_dict(),
		burger.to_dict()
	]

