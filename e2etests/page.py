class Page():
    def __init__(self, driver):
        self.driver = driver 
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
        rows = pl.find_elements_by_class_name('product_row')
        return rows

    @property
    def new_product_element(self):
        return self.driver.find_element_by_id('newProduct')

    @property
    def new_product_name_element(self):
        return self.new_product_element.find_element_by_name('name')

    @property
    def new_product_amount_element(self):
        return self.new_product_element.find_element_by_name('amount')

    def set_new_product_name(self, new_name):
        self.new_product_name_element.send_keys(new_name)

    def set_new_product_amount(self, new_amount):
        self.new_product_name_element.send_keys(new_amount)

    def click_add_new_product(self):
        self.new_product_element.find_element_by_id("product_add").click()
