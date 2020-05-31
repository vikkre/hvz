from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from page import Page
import time

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
    p.set_new_product_required_amount('2')
    p.click_add_new_product()
    time.sleep(2)
    new_rows_count = len(p.product_row_elements)
    assert new_rows_count == (old_rows_count + 1)


def test_delete_product(selenium):
    selenium.get(PAGE_URL)
    p = Page(selenium)
    p.set_new_product_name(f'test-product {datetime.now().timestamp()}')
    p.set_new_product_amount('1')
    p.set_new_product_required_amount('2')
    p.click_add_new_product()
    time.sleep(3)
    old_rows_count = len(p.product_row_elements)
    p.click_delete_product(0)
    time.sleep(3)
    p.click_confirm_delete()
    time.sleep(3)
    new_rows_count = len(p.product_row_elements)
    assert new_rows_count == (old_rows_count - 1)


def test_modify_product(selenium):
    selenium.get(PAGE_URL)
    p = Page(selenium)
    initial_name = f'test-product {datetime.now().timestamp()}'
    p.set_new_product_name(initial_name)
    p.set_new_product_amount('1')
    p.set_new_product_required_amount('2')
    p.click_add_new_product()
    time.sleep(2)
    index = p.get_product_index_by_name(initial_name)
    new_name = f'test-product {datetime.now().timestamp()}'
    p.change_product_name(index, new_name)
    p.change_product_amount(index, 2)
    p.change_product_required_amount(index, 3)
    p.click_save_product(index)
    time.sleep(2)
    new_index = p.get_product_index_by_name(new_name)
    stored_name = p.get_product_name(new_index)
    stored_amount = p.get_product_amount(new_index)
    stored_required_amount = p.get_product_required_amount(new_index)

    assert stored_name == new_name
    assert stored_amount == 2
    assert stored_required_amount == 3
