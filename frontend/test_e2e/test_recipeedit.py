from .database import Database


def db_for_recipe_list():
    database = Database()
    database.truncate()
    database.insert_2_recipes()


def test_add_new_recipe(recipe_list_page, recipe_edit_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.visit(reload=True)
    p.new_recipe.click()
    p.browser.is_element_present_by_text("Save", wait_time=5)
    assert p.rel_path in p.current_url
    assert p.recipe_name.value == ""
    assert p.recipe_text.value == ""

