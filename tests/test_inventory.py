import pytest
from playwright.sync_api import expect


def test_six_products_listed(inventory):
    expect(inventory.items).to_have_count(6)


@pytest.mark.parametrize(
    "option, key, reverse",
    [("az", str.lower, False), ("za", str.lower, True)],
)
def test_sort_by_name(inventory, option, key, reverse):
    inventory.sort_by(option)
    names = inventory.item_names()
    assert names == sorted(names, key=key, reverse=reverse)


@pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)])
def test_sort_by_price(inventory, option, reverse):
    inventory.sort_by(option)
    prices = inventory.item_prices()
    assert prices == sorted(prices, reverse=reverse)


def test_every_product_has_a_positive_price(inventory):
    assert all(p > 0 for p in inventory.item_prices())
