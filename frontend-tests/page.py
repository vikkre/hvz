class Page():
    def __init__(self, driver):
        self.driver: webdriver = driver 
        driver.implicitly_wait(2)

    @property
    def title(self):
        return self.driver.title

    @property
    def product_list_element(self):
        pl = self.driver.find_element_by_id('product_list')
        return pl

    @property
    def product_row_elements(self):
        pl = self.product_list_element
        rows = pl.find_elements_by_tag_name('tr')
        return rows

    @property
    def new_product_element(self):
        return self.driver.find_element_by_id('newProduct')

    @property
    def new_product_name_element(self):
        return self.new_product_element.find_element_by_name('name')

    def set_new_product_name(self, new_name):
        self.new_product_name_element.send_keys(new_name)

    def click_add_new_product(self):
        self.new_product_element.find_element_by_id("product_add").click()
