from app import db

import flask
import sqlalchemy


def get_all(table_class):
	return flask.jsonify([data.to_dict() for data in table_class.query.all()])


def get_by_id(id, table_class, table_result_class):
	table_result = table_result_class()

	try:
		table_result.data = table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"
		else:
			table_result.status = 'ok'

	except sqlalchemy.exc.DataError:
		table_result.status = "failed"
		table_result.error = "id_wrong_format"

	return table_result.to_dict()


def post(data, table_class, table_result_class):
	table_entry = table_class.from_dict(data)
	table_result = table_result_class(table_entry)
	db.session.add(table_result.data)

	try:
		db.session.commit()
		table_result.status = 'ok'
	except sqlalchemy.exc.IntegrityError as error:
		db.session.rollback()
		table_result.status = 'failed' 
		table_result.error = "alredy_exits"

	return table_result.to_dict()


def put_by_id(id, data, table_class, table_result_class):
	table_result = table_result_class()

	try:
		table_result.data = table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"
		else:
			for value_name, value in data.items():
				table_result.data.set_value(value_name, value)

			table_result.status = 'ok'
			db.session.commit()

	except sqlalchemy.exc.DataError:
		table_result.status = "failed"
		table_result.error = "id_wrong_format"

	return table_result.to_dict()


def delete_by_id(id, table_class, table_result_class):
	table_result = table_result_class()

	try:
		table_result.data = table_class.query.get(id)

		if table_result.data is None:
			table_result.status = "failed"
			table_result.error = "not_found"
		else:
			db.session.delete(table_result.data)

			db.session.commit()
			table_result.status = 'ok'

	except sqlalchemy.exc.DataError:
		table_result.status = "failed"
		table_result.error = "id_wrong_format"

	return table_result.to_dict()
