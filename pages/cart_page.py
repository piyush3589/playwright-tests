from playwright.sync_api import Page

from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.checkout_btn = page.get_by_test_id("checkout")
        self.continue_shopping = page.get_by_test_id("continue-shopping")

    def open(self):
        self.page.goto("/cart.html")
        return self

    def item_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def remove(self, product_id: str):
        self.page.get_by_test_id(f"remove-{product_id}").click()

    def checkout(self):
        self.checkout_btn.click()
