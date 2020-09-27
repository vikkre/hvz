from test_e2e.pages.producteditpage import ProductEditPage
import pytest
from splinter import Browser

from .pages import StartPage, ProductListPage, ShoppingListPage, RecipeListPage

from .database import Database
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import shutil


def pytest_addoption(parser):
    parser.addoption("--showbrowser", action="store_const", const=True)


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost"


def set_non_standard_firefox_path(kwargs):
    """
    Use the path to the firefox binary if it can be found in the path.
    If not, rely on the selenium implementation to get the default path.
    This turned out to be necessary on a system where firefox was 
    installed with scoop. 
    """
    path = shutil.which("firefox")
    if path:
        print(f"\nprint: Found firefox at {path}")
        binary = FirefoxBinary(path)
        kwargs["firefox_binary"] = binary


@pytest.fixture(scope="session")
def browser(pytestconfig):
    headless = not pytestconfig.getoption("showbrowser")
    kwargs = {}
    if headless:
        kwargs["headless"] = True
        set_non_standard_firefox_path(kwargs)

    with Browser(**kwargs) as b:
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

