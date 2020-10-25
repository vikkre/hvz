class BasePage():
    rel_path = ""

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url + self.rel_path

    def visit(self, reload=False):
        self.browser.visit(self.base_url)
        if reload:
            self.reload()

    def window_size_tablet(self):
        self.browser.driver.set_window_size(800, 800)

    def window_size_phone(self):
        self.browser.driver.set_window_size(360, 640)

    def reload(self):
        self.browser.reload()

    @property
    def title(self):
        return self.browser.title

    @property
    def burger(self):
        return self.browser.find_by_css(".burger").first

    @property
    def menu_items(self):
        return self.browser.find_by_css(".navbar-start a.navbar-item")

    @property
    def home_button(self):
        return self.browser.find_by_css(".navbar-brand a.navbar-item")

    @property
    def buttons(self):
        return self.browser.find_by_css(".navbar-end .navbar-item a.button")

    @property
    def burger(self):
        return self.browser.find_by_css(".burger").first

    @property
    def current_url(self):
        return self.browser.url
