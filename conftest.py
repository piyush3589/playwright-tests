"""Fixtures.

pytest-playwright already provides `page`, `--base-url`, `--headed`, `--browser`,
`--screenshot`, `--tracing`. We add:
  --mock   run against the bundled offline mock of saucedemo.com
and override `base_url` so that --mock starts the mock server automatically.
"""
import pytest

from mock_site.server import start
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

LIVE_URL = "https://www.saucedemo.com"
VALID_PASSWORD = "secret_sauce"


def pytest_addoption(parser):
    parser.addoption("--mock", action="store_true", help="use the offline mock site")


@pytest.fixture(scope="session")
def base_url(request):
    if request.config.getoption("--mock"):
        server, url = start()
        yield url
        server.shutdown()
    else:
        yield request.config.getoption("--base-url") or LIVE_URL


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright):
    # saucedemo marks elements with data-test (not Playwright's default data-testid)
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def inventory(page, login_page):
    """A browser that is already logged in as standard_user, on the inventory page."""
    login_page.login("standard_user", VALID_PASSWORD)
    inv = InventoryPage(page)
    inv.page.wait_for_url("**/inventory.html")
    return inv


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)
