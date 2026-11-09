from playwright.sync_api import expect

BACKPACK = "sauce-labs-backpack"
LIGHT = "sauce-labs-bike-light"


def test_add_item_updates_badge(inventory):
    inventory.add(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")
    inventory.add(LIGHT)
    expect(inventory.cart_badge).to_have_text("2")


def test_remove_from_inventory_clears_badge(inventory):
    inventory.add(BACKPACK)
    inventory.remove(BACKPACK)
    expect(inventory.cart_badge).to_have_count(0)


def test_cart_shows_added_items(inventory, cart_page):
    inventory.add(BACKPACK)
    inventory.add(LIGHT)
    inventory.open_cart()
    assert sorted(cart_page.item_names()) == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


def test_remove_item_in_cart(inventory, cart_page):
    inventory.add(BACKPACK)
    inventory.add(LIGHT)
    inventory.open_cart()
    cart_page.remove(BACKPACK)
    assert cart_page.item_names() == ["Sauce Labs Bike Light"]


def test_empty_cart_has_no_items(inventory, cart_page):
    inventory.open_cart()
    expect(cart_page.items).to_have_count(0)
