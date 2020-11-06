import pytest
from .database import Database

def db_with_2_products():
    database = Database()
    database.truncate()
    database.insert_2_dummy_products()
    yield database


def test_contains_menu(product_list_page):
    product_list_page.visit()
    assert product_list_page.menu_items != None
    assert len(product_list_page.menu_items) == 3


def test_new_product_switches_to_empty_product_edit_page( product_list_page, product_edit_page):
    db_with_2_products()
    product_list_page.visit()
    product_list_page.new_product.click()
    product_list_page.browser.is_element_present_by_text("Save", wait_time=5)
    product_edit_page.assert_is_current()
    assert product_edit_page.product_name.value == ""
    assert product_edit_page.product_amount.value == "0"
    assert product_edit_page.product_required_amount.value == "0"
