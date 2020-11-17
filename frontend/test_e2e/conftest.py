import os

import pytest
from splinter import Browser

from .pages import (ProductEditPage, ProductListPage, RecipeListPage, RecipeEditPage,
                    ShoppingListPage, StartPage)


@pytest.fixture(scope="session")
def base_url():
    return "http://hvz_web"


@pytest.fixture(scope="session")
def browser():
    selenium_host = os.getenv("SELENIUM_HOST", "localhost")
    selenium_url = f"http://{selenium_host}:4444/wd/hub"
    with Browser(driver_name="remote", command_executor=selenium_url) as b:
        b.driver.set_window_size(360, 800)
        yield b


@pytest.fixture(scope="session")
def start_page(browser, base_url):
    return StartPage(browser, base_url)


@pytest.fixture(scope="session")
def product_list_page(browser, base_url):
    return ProductListPage(browser, base_url)


@pytest.fixture(scope="session")
def product_edit_page(browser, base_url):
    return ProductEditPage(browser, base_url)


@pytest.fixture(scope="session")
def shopping_list_page(browser, base_url):
    return ShoppingListPage(browser, base_url)


@pytest.fixture(scope="session")
def recipe_list_page(browser, base_url):
    return RecipeListPage(browser, base_url)


@pytest.fixture(scope="session")
def recipe_edit_page(browser, base_url):
    return RecipeEditPage(browser, base_url)
