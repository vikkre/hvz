import functools

def test_is_loadable(start_page):
    start_page.visit()
    assert start_page.title == "HVZ"


def test_contains_menu(start_page):
    start_page.visit()
    assert start_page.burger.visible
    start_page.burger.click()

    assert start_page.menu_items[0].html == "Product List"
    assert start_page.menu_items[1].html == "Shopping List"
    assert start_page.menu_items[2].html == "Recipe List"


def test_has_home_button(start_page):
    start_page.visit()
    assert start_page.home_button != None
    assert "HVZ" in start_page.home_button.html


def test_contains_register_button(start_page):
    start_page.visit()
    assert "Register" in functools.reduce(
        lambda a, b: a+b.html, start_page.buttons, "")


def test_contains_login_button(start_page):
    start_page.visit()
    assert "Log in" in functools.reduce(
        lambda a, b: a+b.html, start_page.buttons, "")


def test_navigates_to_productlist(start_page):
    start_page.visit()
    start_page.burger.click()
    product_list_link = next(filter(lambda item: item.html == "Product List", 
    start_page.menu_items))
    product_list_link.click()
    assert "ProductList" in start_page.current_url

def test_navigation_hides_menu(start_page):
    start_page.visit()
    start_page.burger.click()
    product_list_link = next(filter(lambda item: item.html == "Shopping List", 
    start_page.menu_items))
    product_list_link.click()
    assert start_page.browser.is_text_not_present("Shopping List")


