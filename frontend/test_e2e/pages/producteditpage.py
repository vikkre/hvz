from .basepage import BasePage


class ProductEditPage(BasePage):
    rel_path = "#/ProductEdit"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    @property
    def product_name(self):
        return self.browser.find_by_name("product_name")

    @property
    def product_amount(self):
        return self.browser.find_by_name("product_amount")

    @property
    def product_required_amount(self):
        return self.browser.find_by_name("product_required_amount")

    @property
    def save(self):
        return self.browser.find_by_name("save")

    @property
    def cancel(self):
        return self.browser.find_by_name("cancel")

    @property
    def modal(self):
        return self.browser.find_by_css(".modal")

    @property
    def modal_ok(self):
        return self.browser.find_by_name("modal_ok")

    @property
    def modal_cancel(self):
        return self.browser.find_by_name("modal_cancel")
