from .basepage import BasePage


class RecipeRow:
    def __init__(self, row_element):
        self.row_element = row_element

    @property
    def recipe_name(self):
        return self.row_element.find_by_name("recipe_name")

    @property
    def edit_recipe(self):
        return self.row_element.find_by_name("edit_recipe")

    @property
    def delete_recipe(self):
        return self.row_element.find_by_name("delete_recipe")


class RecipeListPage(BasePage):
    rel_path = "#/RecipeList"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    @property
    def recipe_rows(self):
        rows = self.browser.find_by_tag("tr")
        for r in rows:
            r.parts = RecipeRow(r)
        return rows

    @property
    def clear_search_btn(self):
        return self.browser.find_by_name("clear_search")

    @property
    def search_input(self):
        return self.browser.find_by_name("search_input")

    @property
    def new_product(self):
        return self.browser.find_by_name("new_product")

    @property
    def modal(self):
        return self.browser.find_by_css(".modal")

    @property
    def modal_ok(self):
        return self.browser.find_by_name("modal_ok")

    @property
    def modal_cancel(self):
        return self.browser.find_by_name("modal_cancel")
