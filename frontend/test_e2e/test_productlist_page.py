from .database import Database


def db_with_2_products():
    database = Database()
    database.truncate()
    database.insert_2_dummy_products()


def test_contains_menu(product_list_page):
    p = product_list_page
    p.visit()
    assert p.menu_items != None
    assert len(p.menu_items) == 3


def test_display_all_rows_of_products(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    assert len(p.product_rows) == 2


def test_display_elements(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    assert p.product_rows.parts.product_name.text == "Burger"
    assert p.product_rows.parts.product_amount.value == "5"
    assert p.product_rows.parts.required_amount.text == "10"


def test_filter_products(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    p.search_input.type("burg")
    assert len(p.product_rows) == 1


def test_clear_filter(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    p.search_input.type("urg")
    p.clear_search_btn.click()
    assert len(p.product_rows) == 2


def test_change_amount(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    p.product_rows.parts.product_amount.fill(55)
    p.reload()
    assert p.product_rows.parts.product_amount.value == "55"


def test_delete_product(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    assert len(p.product_rows) == 2

    p.product_rows.parts.delete_product.click()
    assert p.modal.visible
    p.modal_ok.click()
    assert len(p.product_rows) == 1
    p.reload()
    assert len(p.product_rows) == 1


def test_cancel_delete_product(product_list_page):
    db_with_2_products()
    p = product_list_page
    p.visit(reload=True)
    assert len(p.product_rows) == 2

    p.product_rows.parts.delete_product.click()
    assert p.modal.visible
    p.modal_cancel.click()
    assert len(p.product_rows) == 2
    p.reload()
    assert len(p.product_rows) == 2
