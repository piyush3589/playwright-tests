from playwright.sync_api import Page

from .base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort = page.get_by_test_id("product-sort-container")

    def open(self):
        self.page.goto("/inventory.html")
        return self

    def item_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def item_prices(self) -> list[float]:
        return [float(t.replace("$", "")) for t in self.prices.all_inner_texts()]

    def sort_by(self, value: str):
        """value: az | za | lohi | hilo"""
        self.sort.select_option(value)

    def add(self, product_id: str):
        self.page.get_by_test_id(f"add-to-cart-{product_id}").click()

    def remove(self, product_id: str):
        self.page.get_by_test_id(f"remove-{product_id}").click()
