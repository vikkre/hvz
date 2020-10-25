from .basepage import BasePage


class ProductRow(object):
    def __init__(self, row_element):
        self.row_element = row_element
    
    @property
    def check(self):
        return self.row_element.find_by_name("check")
        
    @property
    def product_name(self):
        return self.row_element.find_by_name("product")
        
    @property
    def decrease_bought(self):
        return self.row_element.find_by_name("decrease_bought")
        
    @property
    def number_bought(self):
        return self.row_element.find_by_name("number_bought")
        
    @property
    def increase_bought(self):
        return self.row_element.find_by_name("increase_bought")
        
    @property
    def required_amount(self):
        return self.row_element.find_by_name("required_amount")

        
class ShoppingListPage(BasePage):
    rel_path = "#/ShoppingList"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    @property
    def product_rows(self):
        rows =  self.browser.find_by_name("product_row")
        for r in rows:
            r.parts = ProductRow(r)
        return rows