"""Offline stand-in for https://www.saucedemo.com (same URLs, same data-test hooks).

Used with `pytest --mock` so the suite runs in CI without depending on a third-party site.
Stdlib only. Not a perfect clone: just enough behaviour for the flows we test.
"""
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PRODUCTS = [
    ("Sauce Labs Backpack", 29.99, "sauce-labs-backpack"),
    ("Sauce Labs Bike Light", 9.99, "sauce-labs-bike-light"),
    ("Sauce Labs Bolt T-Shirt", 15.99, "sauce-labs-bolt-t-shirt"),
    ("Sauce Labs Fleece Jacket", 49.99, "sauce-labs-fleece-jacket"),
    ("Sauce Labs Onesie", 7.99, "sauce-labs-onesie"),
    ("Test.allTheThings() T-Shirt (Red)", 15.99, "test.allthethings()-t-shirt-(red)"),
]

SCRIPT = r"""
const PRODUCTS = __PRODUCTS__;
const USERS = {standard_user:'ok', locked_out_user:'locked', problem_user:'ok', performance_glitch_user:'ok'};
const PASSWORD = 'secret_sauce';
const $ = (s) => document.querySelector(s);
const cart = () => JSON.parse(localStorage.getItem('cart') || '[]');
const setCart = (c) => localStorage.setItem('cart', JSON.stringify(c));
const loggedIn = () => !!localStorage.getItem('user');
const money = (n) => '$' + n.toFixed(2);
const find = (id) => PRODUCTS.find(p => p[2] === id);
const page = location.pathname;

if (page !== '/' && !loggedIn()) {
  localStorage.setItem('flash', "Epic sadface: You can only access '" + page + "' when you are logged in.");
  location.replace('/');
}

function header(title) {
  return `<div class="header"><button id="react-burger-menu-btn" onclick="document.getElementById('menu').hidden=false">Open Menu</button>
  <div id="menu" hidden><a id="logout_sidebar_link" href="#" onclick="localStorage.removeItem('user');localStorage.removeItem('cart');location.href='/'">Logout</a></div>
  <span class="app_logo">Swag Labs</span>
  <a class="shopping_cart_link" data-test="shopping-cart-link" href="/cart.html">${cart().length ? `<span class="shopping_cart_badge" data-test="shopping-cart-badge">${cart().length}</span>` : ''}Cart</a>
  <span class="title" data-test="title">${title}</span></div>`;
}

const app = $('#app');

if (page === '/') {
  app.innerHTML = `<form id="f"><input data-test="username" placeholder="Username"><input data-test="password" type="password" placeholder="Password">
    <div data-test="error-container"></div><input type="submit" data-test="login-button" id="login-button" value="Login"></form>`;
  const flash = localStorage.getItem('flash');
  if (flash) { localStorage.removeItem('flash'); showErr(flash); }
  function showErr(m) { $('[data-test=error-container]').innerHTML = `<h3 data-test="error">${m}</h3>`; }
  $('#f').onsubmit = (e) => {
    e.preventDefault();
    const u = $('[data-test=username]').value, p = $('[data-test=password]').value;
    if (!u) return showErr('Epic sadface: Username is required');
    if (!p) return showErr('Epic sadface: Password is required');
    if (!(u in USERS) || p !== PASSWORD) return showErr('Epic sadface: Username and password do not match any user in this service');
    if (USERS[u] === 'locked') return showErr('Epic sadface: Sorry, this user has been locked out.');
    localStorage.setItem('user', u); location.href = '/inventory.html';
  };
}

if (page === '/inventory.html') {
  const render = (sort) => {
    const items = [...PRODUCTS];
    if (sort === 'az') items.sort((a, b) => a[0].localeCompare(b[0]));
    if (sort === 'za') items.sort((a, b) => b[0].localeCompare(a[0]));
    if (sort === 'lohi') items.sort((a, b) => a[1] - b[1]);
    if (sort === 'hilo') items.sort((a, b) => b[1] - a[1]);
    const inCart = cart();
    app.innerHTML = header('Products') +
      `<select data-test="product-sort-container" onchange="render(this.value)">
        ${[['az','Name (A to Z)'],['za','Name (Z to A)'],['lohi','Price (low to high)'],['hilo','Price (high to low)']].map(o => `<option value="${o[0]}" ${o[0]===sort?'selected':''}>${o[1]}</option>`).join('')}</select>
      <div data-test="inventory-list">` + items.map(p => `<div class="inventory_item" data-test="inventory-item">
        <div data-test="inventory-item-name">${p[0]}</div><div data-test="inventory-item-price">${money(p[1])}</div>
        ${inCart.includes(p[2]) ? `<button data-test="remove-${p[2]}" onclick="toggle('${p[2]}', '${sort}')">Remove</button>` : `<button data-test="add-to-cart-${p[2]}" onclick="toggle('${p[2]}', '${sort}')">Add to cart</button>`}</div>`).join('') + `</div>`;
  };
  window.render = render;
  window.toggle = (id, sort) => { const c = cart(); const i = c.indexOf(id); i < 0 ? c.push(id) : c.splice(i, 1); setCart(c); render(sort); };
  render('az');
}

if (page === '/cart.html') {
  app.innerHTML = header('Your Cart') + `<div data-test="cart-list">` + cart().map(id => { const p = find(id); return `<div class="cart_item" data-test="inventory-item">
    <div data-test="inventory-item-name">${p[0]}</div><div data-test="inventory-item-price">${money(p[1])}</div>
    <button data-test="remove-${id}" onclick="rm('${id}')">Remove</button></div>`; }).join('') +
    `</div><button data-test="continue-shopping" onclick="location.href='/inventory.html'">Continue Shopping</button>
     <button data-test="checkout" onclick="location.href='/checkout-step-one.html'">Checkout</button>`;
  window.rm = (id) => { setCart(cart().filter(x => x !== id)); location.reload(); };
}

if (page === '/checkout-step-one.html') {
  app.innerHTML = header('Checkout: Your Information') + `<form id="f"><input data-test="firstName" placeholder="First Name"><input data-test="lastName" placeholder="Last Name">
    <input data-test="postalCode" placeholder="Zip/Postal Code"><div id="err"></div>
    <button type="button" data-test="cancel" onclick="location.href='/cart.html'">Cancel</button><input type="submit" data-test="continue" value="Continue"></form>`;
  $('#f').onsubmit = (e) => {
    e.preventDefault();
    const f = $('[data-test=firstName]').value, l = $('[data-test=lastName]').value, z = $('[data-test=postalCode]').value;
    const m = !f ? 'First Name is required' : !l ? 'Last Name is required' : !z ? 'Postal Code is required' : '';
    if (m) { $('#err').innerHTML = `<h3 data-test="error">Error: ${m}</h3>`; return; }
    location.href = '/checkout-step-two.html';
  };
}

if (page === '/checkout-step-two.html') {
  const items = cart().map(find); const sub = items.reduce((s, p) => s + p[1], 0); const tax = Math.round(sub * 8) / 100;
  app.innerHTML = header('Checkout: Overview') + items.map(p => `<div class="cart_item" data-test="inventory-item"><div data-test="inventory-item-name">${p[0]}</div>
    <div data-test="inventory-item-price">${money(p[1])}</div></div>`).join('') +
    `<div data-test="subtotal-label">Item total: ${money(sub)}</div><div data-test="tax-label">Tax: ${money(tax)}</div>
     <div data-test="total-label">Total: ${money(sub + tax)}</div>
     <button data-test="cancel" onclick="location.href='/inventory.html'">Cancel</button>
     <button data-test="finish" onclick="setCart([]);location.href='/checkout-complete.html'">Finish</button>`;
}

if (page === '/checkout-complete.html') {
  app.innerHTML = header('Checkout: Complete!') + `<h2 data-test="complete-header">Thank you for your order!</h2>
    <button data-test="back-to-products" onclick="location.href='/inventory.html'">Back Home</button>`;
}
"""

import json

PAGES = {"/", "/inventory.html", "/cart.html", "/checkout-step-one.html",
         "/checkout-step-two.html", "/checkout-complete.html"}


def _html() -> bytes:
    script = SCRIPT.replace("__PRODUCTS__", json.dumps(PRODUCTS))
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>Swag Labs</title></head>"
            f"<body><div id='app'></div><script>{script}</script></body></html>").encode()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in PAGES:
            body, status = _html(), 200
        else:
            body, status = b"Not found", 404
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def start(host="127.0.0.1", port=0):
    server = ThreadingHTTPServer((host, port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://{host}:{server.server_address[1]}"


if __name__ == "__main__":
    s, url = start(port=8000)
    print("Mock site on", url)
    threading.Event().wait()
