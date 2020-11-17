from .database import Database
from selenium.webdriver.common.action_chains import ActionChains


def db_for_recipe_list():
    database = Database()
    database.truncate()
    database.insert_2_recipes()


def test_add_new_recipe_from_list(recipe_list_page, recipe_edit_page):
    db_for_recipe_list()
    p = recipe_list_page
    p.window_size_phone()
    p.visit(reload=True)
    p.new_recipe.click()
    p.browser.is_element_present_by_text("Save", wait_time=5)
    recipe_edit_page.assert_is_current()

def test_enter_new_recipe_and_save(recipe_edit_page, recipe_list_page):
    p = recipe_edit_page
    p.visit(reload=True)
    p.recipe_name.type("product_test")
    p.recipe_text.type("preparation")
    p.save.click()
    p.browser.is_element_present_by_text("new_recipe", wait_time=5)
    recipe_list_page.assert_is_current()


