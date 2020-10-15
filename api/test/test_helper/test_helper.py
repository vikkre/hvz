import unittest

from base import app, db
import helper

from test.test_helper import person, town, person_has_town

Person = person.Person
Town = town.Town
PersonHasTown = person_has_town.PersonHasTown


person.init()
town.init()


class TestRestBase(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		app.testing = True

		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

		db.create_all()

		self.berlin = Town(name="Berlin", size=(3*1000*1000))
		self.hamburg = Town(name="Hamburg", size=(1.5*1000*1000))

		self.alice = Person(name="Alice", height_cm=150, weight=60)
		self.bob = Person(name="Bob", height_cm=210, weight=150)

		self.alice.towns.append(PersonHasTown(town=self.berlin, address="Haus 1"))
		self.bob.towns.append(PersonHasTown(town=self.berlin, address="Haus 2"))
		self.bob.towns.append(PersonHasTown(town=self.hamburg, address="Allee 5"))

		db.session.add(self.berlin)
		db.session.add(self.hamburg)

		db.session.add(self.alice)
		db.session.add(self.bob)

		db.session.commit()

		self.client = app.test_client()


	def tearDown(self):
		db.session.rollback()
		db.drop_all()


	def test_get_all_persons(self):
		expected = [
			self.alice.to_dict(), self.bob.to_dict()
		]

		response = self.client.get("/person")
		result = response.json
		self.assertCountEqual(expected, result)


	def test_get_all_towns(self):
		expected = [
			self.berlin.to_dict(), self.hamburg.to_dict()
		]

		response = self.client.get("/town")
		result = response.json
		self.assertCountEqual(expected, result)


	def test_get_by_id(self):
		expected = self.alice.to_dict()

		response = self.client.get("/person/" + str(self.alice.id))
		result = response.json

		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])


	def test_get_by_id_does_not_exist(self):
		response = self.client.get("/town/10")
		result = response.json

		self.assertEqual("failed", result["status"])
		self.assertEqual("not_found", result["error"])
		self.assertIsNone(result["data"])


	def test_post_town(self):
		data = {
			"name": "Kassel",
			"size": 200 * 1000
		}

		response = self.client.post("/town", json=data)
		result = response.json
		self.assertEqual("ok", result["status"])

		result = result["data"]
		data["id"] = result["id"]
		db_data = Town.query.get(data["id"])
		db_data = db_data.to_dict()
		self.assertCountEqual(data, db_data)


	def test_post_person(self):
		data = {
			"name": "mallory",
			"height_cm": 180,
			"weight": 80,
			"towns": [
				{
					"id": self.berlin.id,
					"address": "Bachweg 3"
				},
				{
					"id": self.hamburg.id,
					"address": "Nordallee 3"
				}
			]
		}

		response = self.client.post("/person", json=data)
		result = response.json
		self.assertEqual("ok", result["status"])

		result = result["data"]
		data["id"] = result["id"]
		db_data = Person.query.get(data["id"])
		db_data = db_data.to_dict()
		self.assertCountEqual(data, db_data)


	def test_post_person_no_towns(self):
		data = {
			"name": "mallory",
			"height_cm": 180,
			"weight": 80,
			"towns": []
		}

		response = self.client.post("/person", json=data)
		result = response.json
		self.assertEqual("ok", result["status"])

		result = result["data"]
		data["id"] = result["id"]
		db_data = Person.query.get(data["id"])
		db_data = db_data.to_dict()
		self.assertCountEqual(data, db_data)

	
	def test_post_missing_parameter(self):
		response = self.client.post("/person", json={})
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertEqual("missing_parameter", result["error"])
		self.assertIsNone(result["data"])


	def test_post_alredy_exits(self):
		data = {
			"name": "Berlin",
			"size": 3 * 1000 * 1000
		}

		response = self.client.post("/town", json=data)
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertEqual("alredy_exits", result["error"])
		self.assertIsNone(result["data"])


	def test_put_town(self):
		data = {
			"name": "Bierlin"
		}

		expected = self.berlin.to_dict()
		expected["name"] = "Bierlin"

		response = self.client.put("/town/" + str(self.berlin.id), json=data)
		result = response.json
		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])


	def test_put_none(self):
		data = {}
		expected = self.alice.to_dict()

		response = self.client.put("/person/" + str(self.alice.id), json=data)
		result = response.json
		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])


	def test_put_person(self):
		data = {
			"name": "Otto"
		}
		expected = self.alice.to_dict()
		expected["name"] = "Otto"

		response = self.client.put("/person/" + str(self.alice.id), json=data)
		result = response.json
		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])


	def test_put_person_towns(self):
		data = {
			"towns": [
				{
					"id": self.berlin.id,
					"address": "Bachweg 3"
				},
				{
					"id": self.hamburg.id,
					"address": "Nordallee 3"
				}
			]
		}
		expected = self.alice.to_dict()
		expected["towns"] = [
			{
				"town_id": self.berlin.id,
				"town_name": self.berlin.name,
				"address": "Bachweg 3"
			},
			{
				"town_id": self.hamburg.id,
				"town_name": self.hamburg.name,
				"address": "Nordallee 3"
			}
		]

		response = self.client.put("/person/" + str(self.alice.id), json=data)
		result = response.json
		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])


	def test_put_not_found(self):
		data = {
			"name": "Otto"
		}

		response = self.client.put("/person/123", json=data)
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertEqual("not_found", result["error"])
		self.assertIsNone(result["data"])

	
	def test_put_already_exists(self):
		data = {
			"name": "Bob"
		}

		response = self.client.put("/person/" + str(self.alice.id), json=data)
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertEqual("already_exists", result["error"])
		self.assertIsNone(result["data"])


	def test_delete_town_fail(self):
		expected = self.berlin.to_dict()
		id = self.berlin.id

		response = self.client.delete("/town/" + str(id))
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertCountEqual("still_referenced", result["error"])

		db_data = Town.query.get(id)
		self.assertIsNotNone(db_data)


	def test_delete_person(self):
		expected = self.alice.to_dict()
		id = self.alice.id

		response = self.client.delete("/person/" + str(id))
		result = response.json
		self.assertEqual("ok", result["status"])
		self.assertCountEqual(expected, result["data"])

		db_data = Person.query.get(id)
		self.assertIsNone(db_data)

		berlin = Town.query.get(self.berlin.id)
		self.assertEqual(1, len(berlin.persons))


	def test_delete_not_found(self):
		response = self.client.delete("/person/123")
		result = response.json
		self.assertEqual("failed", result["status"])
		self.assertEqual("not_found", result["error"])
		self.assertIsNone(result["data"])
