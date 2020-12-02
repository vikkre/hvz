import os
import time

import pytest
from splinter import Browser

from .database import Database
from .pages import (ProductEditPage, ProductListPage, RecipeEditPage,
                    RecipeListPage, ShoppingListPage, StartPage)


def retry(f, extype=Exception, max_count=10, incr_factor=2):
    """
    Call the callable f. If an execption of type exttype occurs,
    sleep a while and retry.

    Retry up to max_count times.

    Multiply the current retry count by incr_factor to obtain the
    number of seconds to sleep.
    """
    retry_count = 0
    # result = None
    while True:
        try:
            # result = f()
            return f()
            # break
        except extype as e:
            retry_count += 1
            if (retry_count > max_count):
                raise e
            else:
                time.sleep(incr_factor * retry_count)
    # return result


@pytest.fixture(scope="session")
def base_url():
    return "http://hvz_web"


@pytest.fixture(scope="session")
def db():
    yield retry(lambda: Database())


@pytest.fixture(scope="session")
def browser():
    selenium_host = os.getenv("SELENIUM_HOST", "localhost")
    selenium_url = f"http://{selenium_host}:4444/wd/hub"
    with retry(lambda: Browser(driver_name="remote", command_executor=selenium_url)) as b:
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
