#TODO: Use db fixture!
import pytest
from .database import Database


def db_for_shopping_list():
    db = Database()
    db.truncate()
    db.insert_4_dummy_products_for_shopping_list()


def test_shopping_list_only_shows_needed_products(shopping_list_page):
    db_for_shopping_list()
    shopping_list_page.visit(reload=True)
    assert len(shopping_list_page.product_rows) == 3


def test_shopping_list_mark_products_in_cart(shopping_list_page):
    db_for_shopping_list()
    page = shopping_list_page
    page.visit(reload=True)
    page.product_rows.parts.product_name.click()
    assert page.product_rows.parts.product_name.has_class("inCart")


def test_shopping_list_shows_number_bought(shopping_list_page):
    db_for_shopping_list()
    page = shopping_list_page
    page.visit(reload=True)
    assert page.product_rows.parts.number_bought.value == "5"


def test_shopping_list_can_decrease_number_bought(shopping_list_page):
    db_for_shopping_list()
    page = shopping_list_page
    page.visit(reload=True)
    assert page.product_rows[1].parts.number_bought.value == "1"
    page.product_rows[1].parts.decrease_bought.click()
    page.product_rows[1].parts.decrease_bought.click()
    assert page.product_rows[1].parts.number_bought.value == "0"


def test_shopping_list_can_increase_number_bought(shopping_list_page):
    db_for_shopping_list()
    page = shopping_list_page
    page.visit(reload=True)
    page.product_rows[1].parts.increase_bought.click()
    page.product_rows[1].parts.increase_bought.click()
    page.product_rows[1].parts.increase_bought.click()
    assert page.product_rows[1].parts.number_bought.value == "4"


def test_shopping_list_shows_number_required(shopping_list_page):
    db_for_shopping_list()
    page = shopping_list_page
    page.visit(reload=True)
    page.window_size_tablet()
    assert page.product_rows[1].parts.required_amount.value == "10"


def test_shopping_list__hides_number_required_on_mobile_phone(shopping_list_page):
    db_for_shopping_list()
    shopping_list_page.visit(reload=True)

    shopping_list_page.window_size_tablet()
    assert shopping_list_page.product_rows.parts.required_amount.visible

    shopping_list_page.window_size_phone()
    assert not shopping_list_page.product_rows.parts.required_amount.visible


def test_shopping_list_with_lots_of_products():
    database = Database()
    database.truncate()
    for i in range(1, 51):
        database.insert_product(
            name=f"Product-{i:02d}", amount=i, required_amount=i+3)
