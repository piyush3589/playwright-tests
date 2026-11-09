# UI Test Automation (Python + Playwright)

End-to-end UI tests for the demo shop [saucedemo.com](https://www.saucedemo.com), built with
**Playwright (Python) + Pytest** and the **Page Object Model**.

## What is covered (24 tests)

| Area | Examples |
|---|---|
| Login | valid login, 5 invalid-credential cases (parametrized), locked-out user, protected page redirects, logout |
| Inventory | product count, sort by name and price (A-Z, Z-A, low-high, high-low), prices positive |
| Cart | add/remove items, cart badge count, cart contents, empty cart |
| Checkout | full purchase flow, form validation (3 cases), order total = item total + 8% tax, cart cleared after order |

## Structure

```
pages/        # Page Objects: one class per page, no assertions inside
tests/        # test files, read like user stories
mock_site/    # offline stand-in for saucedemo (stdlib only) for fast, stable CI
conftest.py   # fixtures: base_url, logged-in `inventory` fixture, page objects, --mock option
.github/      # CI: runs the suite on every push and uploads report + traces
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                       # real saucedemo.com
pytest --mock                # offline mock site
pytest --headed --slowmo 500 # watch the browser
pytest -k checkout           # run a subset
pytest --browser firefox     # cross-browser
pytest --mock --html=report.html --self-contained-html
```

On failure a screenshot and a Playwright trace are saved to `test-results/`
(open a trace with `playwright show-trace test-results/<test>/trace.zip`).

## Design notes

- **Locators** use `data-test` attributes (`get_by_test_id`) rather than CSS/XPath, so tests survive layout changes.
- **No sleeps.** Playwright auto-waits, and assertions use `expect(...)` which retries.
- **Page Objects hold locators and actions; tests hold assertions.**
- **Mock mode** keeps CI independent of a third-party site. The mock was checked by injecting bugs
  (wrong tax rate, broken sort, locked user allowed): the tests fail on each, so they are actually testing something.
- Known limit: the mock mimics the flows above only, so run `pytest` (live) before trusting a result about the real site.

## Possible next steps

- Visual checks with `expect(page).to_have_screenshot()`
- Allure reports
- Tests for `problem_user` and `performance_glitch_user` (known-buggy demo users) to log real defects
