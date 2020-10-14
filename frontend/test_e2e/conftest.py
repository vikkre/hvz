from test_e2e.pages.producteditpage import ProductEditPage
import pytest
from splinter import Browser

from .pages import StartPage, ProductListPage, ShoppingListPage, RecipeListPage


@pytest.fixture(scope="session")
def base_url():
    return "http://hvz_web"


@pytest.fixture(scope="session")
def browser():
    with Browser(driver_name="remote") as b:
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
