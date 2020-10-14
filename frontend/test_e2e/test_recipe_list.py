from .database import Database


def db_for_recipe_list():
    database = Database()
    database.truncate()
    database.insert_2_recipes()


def test_recipe_list_shows_recipe_names(recipe_list_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    assert p.recipe_rows[0].parts.recipe_name.value == "Carbonara"
    assert p.recipe_rows[1].parts.recipe_name.value == "Zabaione"

def test_filter_by_name(recipe_list_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    p.search_input.type("car")
    assert len(p.recipe_rows) == 1
    assert p.recipe_rows[0].parts.recipe_name.value == "Carbonara"

def test_clear_filter(recipe_list_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    p.search_input.type("car")
    assert len(p.recipe_rows) == 1
    p.clear_search_btn.click()
    assert len(p.recipe_rows) == 2


def test_delete_recipe(recipe_list_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    p.recipe_rows[1].parts.delete_recipe.click()
    assert p.modal.visible
    p.modal_ok.click()
    assert len(p.recipe_rows) == 1
    p.reload()
    assert len(p.recipe_rows) == 1


def test_cancel_delete_recipe(recipe_list_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    p.recipe_rows[1].parts.delete_recipe.click()
    assert p.modal.visible
    p.modal_cancel.click()
    assert len(p.recipe_rows) == 2
    p.reload()
    assert len(p.recipe_rows) == 2