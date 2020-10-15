import unittest

from base import app
from endpoint.root import init


init()


class TestRoot(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		app.testing = True

		self.client = app.test_client()

	
	def test_get(self):
		expected = "Hello World!\n"

		response = self.client.get("/")
		result = response.data.decode("utf-8")
		self.assertEqual(expected, result)
