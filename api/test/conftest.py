from flask import request
import pytest

from app import app, db
from products import Product
from test.create_test_data import create_test_data


@pytest.fixture(scope="function")
def client_app():
	db.drop_all()
	db.create_all()

	ret = app.test_client()

	return ret


@pytest.fixture(scope="function")
def client_products():
	expected = create_test_data()

	ret = app.test_client()
	ret.expected = expected

	return ret


def pytest_exception_interact(node, call, report):
	if report.failed:
		db.session.rollback()
