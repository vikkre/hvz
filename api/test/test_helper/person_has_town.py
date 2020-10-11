from base import db


class PersonHasTown(db.Model):
	__tablename__ = "person_has_town"
	person_id = db.Column(db.Integer, db.ForeignKey("person.id"), primary_key=True)
	town_id = db.Column(db.Integer, db.ForeignKey("town.id"), primary_key=True)
	address = db.Column(db.String(100), nullable=False)
	person = db.relationship("Person", back_populates="towns")
	town = db.relationship("Town", back_populates="persons")


	def to_dict(self):
		return {
			"person_id": self.person_id,
			"town_id": self.town_id,
			"address": self.address
		}


	@staticmethod
	def from_dict(data):
		address = data["address"]

		return PersonHasTown(address=address)


	def __repr__(self):
		return f"<PersonHasTown ({self.person_id},{self.town_id}), address={self.address}>"
