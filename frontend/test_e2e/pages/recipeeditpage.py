from .basepage import BasePage


class IngredientRow:
    def __init__(self, row_element):
        self.row_element = row_element

    @property
    def product_name(self):
        return self.row_element.find_by_name("product_name")

    @property
    def product_amount(self):
        return self.row_element.find_by_name("product_amount")

    @property
    def delete_product(self):
        return self.row_element.find_by_name("delete_ingredient")


class RecipeEditPage(BasePage):
    rel_path = "#/RecipeEdit"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    @property
    def recipe_name(self):
        return self.browser.find_by_name("recipe_name")

    @property
    def recipe_text(self):
        return self.browser.find_by_name("recipe_text")

    @property
    def new_ingredien(self):
        return self.browser.find_by_name("new_ingredien")

    @property
    def save(self):
        return self.browser.find_by_name("save")

    @property
    def cancel(self):
        return self.browser.find_by_name("cancel")
