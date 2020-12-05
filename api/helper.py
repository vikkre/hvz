import flask
import sqlalchemy

import base


class Result:
	def __init__(self, data=None):
		self.data = data
		self.status = "OK"
		self.status_code = 200

	def to_dict(self):
		data = None if self.data is None else self.data.to_dict()

		return {
			"data": data,
			"status": self.status
		}

	def get_response(self):
		return self.to_dict(), self.status_code


class RestBase:
	def __init__(self, rule, table_class):
		self.table_class = table_class

		endpoint = rule.replace("/", "_")

		base.app.add_url_rule("{}".format(rule),      view_func=self.get_all,      methods=["GET"],    endpoint="get_all{}".format(endpoint)      )
		base.app.add_url_rule("{}/<id>".format(rule), view_func=self.get_by_id,    methods=["GET"],    endpoint="get_by_id{}".format(endpoint)    )
		base.app.add_url_rule("{}".format(rule),      view_func=self.post,         methods=["POST"],   endpoint="post{}".format(endpoint)         )
		base.app.add_url_rule("{}/<id>".format(rule), view_func=self.put_by_id,    methods=["PUT"],    endpoint="put_by_id{}".format(endpoint)    )
		base.app.add_url_rule("{}/<id>".format(rule), view_func=self.delete_by_id, methods=["DELETE"], endpoint="delete_by_id{}".format(endpoint) )


	def get_all(self):
		result = [data.to_dict() for data in self.table_class.query.all()]
		return flask.jsonify(result), 200


	def get_by_id(self, id):
		table_result = Result()

		table_result.data = self.table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "Not Found"
			table_result.status_code = 404

		return table_result.get_response()


	def post(self):
		data = flask.request.json

		try:
			table_result = Result()
			table_result.status = "Created"
			table_result.status_code = 201

			table_entry = self.table_class.from_dict(data)
			base.db.session.add(table_entry)

			base.db.session.commit()
			table_result.data = table_entry

		except KeyError:
			base.db.session.rollback()

			table_result.status = "Missing Parameter"
			table_result.status_code = 400

			table_result.data = None

		except sqlalchemy.exc.IntegrityError:
			base.db.session.rollback()
			
			table_result.status = "Already Exists"
			table_result.status_code = 400

			table_result.data = None

		return table_result.get_response()


	def put_by_id(self, id):
		data = flask.request.json
		table_result = Result()

		table_result.data = self.table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "Not Found"
			table_result.status_code = 404
		else:
			try:
				for value_name, value in data.items():
					table_result.data.set_value(value_name, value)

				base.db.session.commit()

			except sqlalchemy.exc.StatementError:
				base.db.session.rollback()
				
				table_result.status = "Already Exists"
				table_result.status_code = 400

				table_result.data = None

		return table_result.get_response()


	def delete_by_id(self, id):
		table_result = Result()

		table_result.data = self.table_class.query.get(id)

		result = table_result.get_response()

		if table_result.data is None:
			table_result.status = "Not Found"
			table_result.status_code = 404

			result = table_result.get_response()
		else:
			base.db.session.delete(table_result.data)

			try:
				base.db.session.commit()
			except AssertionError:
				base.db.session.rollback()

				table_result.status = "In Use"
				table_result.status_code = 400

				result = table_result.get_response()

		return result
