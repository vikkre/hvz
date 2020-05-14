from flask import request
import pytest

from app import app, db
from products import Product


@pytest.fixture
def client_app():
	db.drop_all()
	db.create_all()

	ret = app.test_client()

	return ret


@pytest.fixture
def client_products():
	db.drop_all()
	db.create_all()

	milch = Product(name='Milch', amount=5)
	burger = Product(name='Burger', amount=50)

	db.session.add(milch)
	db.session.add(burger)
	db.session.commit()

	expected = [
		milch.to_dict(),
		burger.to_dict()
	]

	ret = app.test_client()
	ret.expected = expected

	return ret
