import base
from run_once import run_once


@run_once
def init():
	base.app.add_url_rule("/", view_func=index)


def index():
	return "Hello World!\n"
