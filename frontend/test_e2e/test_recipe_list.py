import pytest
from .database import Database


def db_for_recipe_list():
    database = Database()
    database.truncate()
    database.insert_2_recipes()


def test_recipe_list_shows_recipe_names(recipe_list_page):
    db_for_recipe_list()
    page = recipe_list_page
    page.visit(reload=True)
    assert page.recipe_rows[0].parts.recipe_name.value == "Carbonara"
    assert page.recipe_rows[1].parts.recipe_name.value == "Zabaione"
