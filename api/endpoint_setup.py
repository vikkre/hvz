from endpoint import root, product, recipe, menu
from relation import recipe_has_product


def init_endpoints():
	init_list = [root, product]
	for entry in init_list:
		entry.init()
