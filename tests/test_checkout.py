import pytest
from playwright.sync_api import expect


def _go_to_checkout(inventory, cart_page, *product_ids):
    for pid in product_ids:
        inventory.add(pid)
    inventory.open_cart()
    cart_page.checkout()


def test_end_to_end_purchase(page, inventory, cart_page, checkout_page):
    _go_to_checkout(inventory, cart_page, "sauce-labs-backpack")
    checkout_page.fill_info()
    expect(checkout_page.total).to_be_visible()
    checkout_page.finish()
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
    # cart must be emptied after a successful order
    expect(checkout_page.cart_badge).to_have_count(0)


@pytest.mark.parametrize(
    "first, last, postal, message",
    [
        ("", "Raut", "400601", "First Name is required"),
        ("Pi", "", "400601", "Last Name is required"),
        ("Pi", "Raut", "", "Postal Code is required"),
    ],
    ids=["no-first", "no-last", "no-postal"],
)
def test_checkout_form_validation(inventory, cart_page, checkout_page, first, last, postal, message):
    _go_to_checkout(inventory, cart_page, "sauce-labs-backpack")
    checkout_page.fill_info(first, last, postal)
    expect(checkout_page.error).to_contain_text(message)


def test_order_total_is_item_total_plus_tax(inventory, cart_page, checkout_page):
    _go_to_checkout(inventory, cart_page, "sauce-labs-backpack", "sauce-labs-bike-light")
    checkout_page.fill_info()

    def amount(locator):
        return float(locator.inner_text().split("$")[1])

    subtotal, tax, total = amount(checkout_page.subtotal), amount(checkout_page.tax), amount(checkout_page.total)
    assert subtotal == pytest.approx(39.98)
    assert tax == pytest.approx(round(subtotal * 0.08, 2), abs=0.01)  # 8% tax
    assert total == pytest.approx(subtotal + tax, abs=0.01)
