from base import db
from run_once import run_once

import helper
from test.test_helper import town, person_has_town

Town = town.Town
PersonHasTown = person_has_town.PersonHasTown


class Person(db.Model):
	__tablename__ = "person"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	height_cm = db.Column(db.Integer, nullable=False)
	weight = db.Column(db.Float, nullable=False)
	towns = db.relationship("PersonHasTown", cascade="all,save-update,delete-orphan", back_populates="person")


	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"height_cm": self.height_cm,
			"weight": self.weight,
			"towns": [{
				"town_id": town.town_id,
				"town_name": town.town.name,
				"address": town.address
			} for town in self.towns]
		}


	@staticmethod
	def from_dict(data):
		name = data["name"]
		height_cm = data["height_cm"]
		weight = data["weight"]
		towns = data["towns"]

		person = Person(name=name, height_cm=height_cm, weight=weight)

		person.insert_towns(towns)

		return person


	def set_value(self, value_name, value):
		if value_name == "name":
			self.name = value
		elif value_name == "height_cm":
			self.height_cm = value
		elif value_name == "weight":
			self.weight = value
		elif value_name == "towns":
			self.towns.clear()
			self.insert_towns(value)


	def __repr__(self):
		return f"<Person {self.name}, height_cm={self.height_cm}, weight={self.weight}>"

	
	def insert_towns(self, towns):
		for town in towns:
			town_entry = Town.query.get(town["id"])
			address = town["address"]

			person_has_town = PersonHasTown(town=town_entry, address=address)
			self.towns.append(person_has_town)


@run_once
def init():
	helper.RestBase("/person", Person, data_name="person")
