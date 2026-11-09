import re

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


def test_valid_login_lands_on_inventory(page, login_page):
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize(
    "user, password, message",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("standard_user", "wrong", "do not match any user"),
        ("nobody", "secret_sauce", "do not match any user"),
        ("locked_out_user", "secret_sauce", "locked out"),
    ],
    ids=["no-username", "no-password", "bad-password", "unknown-user", "locked-user"],
)
def test_invalid_login_shows_error(page, login_page, user, password, message):
    login_page.login(user, password)
    expect(login_page.error).to_contain_text(message)
    expect(page).not_to_have_url(re.compile(r"/inventory\.html$"))


def test_protected_page_redirects_to_login(page, login_page):
    page.goto("/inventory.html")
    expect(login_page.error).to_contain_text("You can only access '/inventory.html'")


def test_logout_returns_to_login(page, inventory):
    inventory.logout()
    expect(page.get_by_test_id("login-button")).to_be_visible()
