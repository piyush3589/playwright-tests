from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_btn = page.get_by_test_id("continue")
        self.error = page.get_by_test_id("error")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_btn = page.get_by_test_id("finish")
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_info(self, first="Pi", last="Raut", postal="400601"):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_btn.click()

    def finish(self):
        self.finish_btn.click()
