from playwright.sync_api import Page

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def open(self):
        self.page.goto("/")
        return self

    def login(self, user: str, password: str):
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
