from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from page import Page

PAGE_URL = 'http://web'


def test_page(selenium):
    selenium.get(PAGE_URL)
    p = Page(selenium)
    assert 'HVZ - Bestandsliste' in p.title


def test_products_list(selenium):
    selenium.get(PAGE_URL)
    p = Page(selenium)
    rows = p.product_row_elements
    assert len(rows) >= 0


def test_add_new_product(selenium):
    selenium.get(PAGE_URL)
    p = Page(selenium)
    old_rows_count = len(p.product_row_elements)
    p.set_new_product_name(f'test-product {datetime.now().timestamp()}')
    p.set_new_product_amount('1')
    p.click_add_new_product()
    new_rows_count = len(p.product_row_elements)
    assert new_rows_count == (old_rows_count + 1)


