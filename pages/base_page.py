from playwright.sync_api import Page


class BasePage:
    """Shared bits: header cart badge, menu, navigation."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.title = page.get_by_test_id("title")

    def cart_count(self) -> int:
        return int(self.cart_badge.inner_text()) if self.cart_badge.count() else 0

    def open_cart(self):
        self.cart_link.click()

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("#logout_sidebar_link").click()
