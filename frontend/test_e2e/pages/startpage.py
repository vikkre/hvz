from .basepage import BasePage


class StartPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
