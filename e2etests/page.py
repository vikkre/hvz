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

    @property
    def new_product_required_amount_element(self):
        return self.new_product_element.find_element_by_name('required_amount')

    def set_new_product_name(self, new_name):
        self.new_product_name_element.send_keys(new_name)

    def set_new_product_amount(self, new_amount):
        self.new_product_amount_element.send_keys(new_amount)

    def set_new_product_required_amount(self, new_amount):
        self.new_product_required_amount_element.send_keys(new_amount)

    def click_add_new_product(self):
        self.new_product_element.find_element_by_id("product_add").click()

    def click_delete_product(self, index):
        rows = self.product_row_elements
        row_to_remove = rows[index]
        delete_link = row_to_remove.find_element_by_name("product_delete")
        delete_link.click()

    def click_confirm_delete(self):
        confirm_delete = self.driver.find_element_by_id("confirmDelete")
        confirm_delete.click()

    def get_product_index_by_name(self, name):
        for i, row in enumerate(self.product_row_elements):
            name_in_row = self.get_product_name(i)
            if name_in_row == name:
                return i
        return None

    def get_product_value(self, index, input_name):
        row = self.product_row_elements[index]
        input = row.find_element_by_name(input_name)
        return input.get_attribute("value")

    def get_product_name(self, index):
        return self.get_product_value(index, "name")

    def get_product_amount(self, index):
        return int(self.get_product_value(index, "amount"))

    def get_product_required_amount(self, index):
        return int(self.get_product_value(index, "required_amount"))

    def click_save_product(self, index):
        row = self.product_row_elements[index]
        btn = row.find_element_by_name("product_save")
        btn.click()

    def change_product_value(self, index, input_name, new_value):
        row = self.product_row_elements[index]
        input = row.find_element_by_name(input_name)
        input.clear()
        input.send_keys(new_value)

    def change_product_name(self, index, new_value):
        self.change_product_value(index, "name", new_value)

    def change_product_amount(self, index, new_value):
        self.change_product_value(index, "amount", new_value)

    def change_product_required_amount(self, index, new_value):
        self.change_product_value(index, "required_amount", new_value)
