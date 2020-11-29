from base import db
from run_once import run_once

import helper
import test.test_helper.person_has_town


class Town(db.Model):
	__tablename__ = "town"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	size = db.Column(db.Integer, nullable=False)
	persons = db.relationship("PersonHasTown", back_populates="town")


	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"size": self.size
		}


	@staticmethod
	def from_dict(data):
		name = data["name"]
		size = data["size"]

		return Town(name=name, size=size)


	def set_relations(self, data):
		pass


	def set_value(self, value_name, value):
		if value_name == "name":
			self.name = value
		elif value_name == "size":
			self.size = value


	def __repr__(self):
		return f"<Town {self.name}, size={self.size}>"


@run_once
def init():
	helper.RestBase("/town", Town)
