import flask
import sqlalchemy

import base


# deprecated: Result.data_name
# deprecated: Result.status
# deprecated: Result.error

# rename: Result.hvz_status to Result.status


class Result:
	def __init__(self, data_name, data=None):
		self.data_name = data_name
		self.data = data

		self.status = None
		self.error = None

		self.status_code = 200
		self.hvz_status = "OK"

	def to_dict(self):
		data = None if self.data is None else self.data.to_dict()

		return {
			self.data_name: data,
			"data": data,
			"status": self.status,
			"error": self.error,
			"hvz_status": self.hvz_status
		}

	def get_response(self):
		return self.to_dict(), self.status_code


class RestBase:
	def __init__(self, rule, table_class, data_name=""):
		self.table_class = table_class
		self.data_name = data_name

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
		table_result = Result(self.data_name)

		table_result.data = self.table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"

			table_result.status_code = 404
			table_result.hvz_status = "Not Found"
		else:
			table_result.status = "ok"

		return table_result.get_response()


	def post(self):
		data = flask.request.json

		try:
			table_result = Result(self.data_name)
			table_result.status_code = 201
			table_result.hvz_status = "Created"

			table_entry = self.table_class.from_dict(data)
			base.db.session.add(table_entry)

			base.db.session.commit()
			table_result.data = table_entry
			table_result.status = "ok"

		except KeyError:
			base.db.session.rollback()
			table_result.status = "failed"
			table_result.error = "missing_parameter"

			table_result.status_code = 400
			table_result.hvz_status = "Missing Parameter"

			table_result.data = None

		except sqlalchemy.exc.IntegrityError:
			base.db.session.rollback()
			table_result.status = "failed"
			table_result.error = "alredy_exits"

			table_result.status_code = 400
			table_result.hvz_status = "Already Exists"

			table_result.data = None

		return table_result.get_response()


	def put_by_id(self, id):
		data = flask.request.json
		table_result = Result(self.data_name)

		table_result.data = self.table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"

			table_result.status_code = 404
			table_result.hvz_status = "Not Found"
		else:
			try:
				for value_name, value in data.items():
					table_result.data.set_value(value_name, value)

				table_result.status = "ok"
				base.db.session.commit()

			except sqlalchemy.exc.StatementError:
				base.db.session.rollback()
				table_result.status = "failed"
				table_result.error = "already_exists"

				table_result.status_code = 400
				table_result.hvz_status = "Already Exists"

				table_result.data = None

		return table_result.get_response()


	def delete_by_id(self, id):
		table_result = Result(self.data_name)

		table_result.data = self.table_class.query.get(id)

		table_result.status = "ok"
		result = table_result.get_response()

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"

			table_result.status_code = 404
			table_result.hvz_status = "Not Found"

			result = table_result.get_response()
		else:
			base.db.session.delete(table_result.data)

			try:
				base.db.session.commit()
			except AssertionError:
				base.db.session.rollback()
				table_result.status = "failed"
				table_result.error = "still_referenced"
			
				table_result.status_code = 400
				table_result.hvz_status = "In Use"

				result = table_result.get_response()

		return result
