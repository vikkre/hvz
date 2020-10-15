from endpoint import root, product, recipe, menu
from relation import recipe_has_product, menu_has_recipe


def init_endpoints():
	init_list = [root, product, recipe, menu]
	for entry in init_list:
		entry.init()
