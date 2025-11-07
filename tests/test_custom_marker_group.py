import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.smoke
def test_open_example():
    """Latihan 44: Test kategori 'smoke'"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        assert "Example Domain" in page.title()
        browser.close()


@pytest.mark.regression
def test_open_playwright_site():
    """Latihan 44: Test kategori 'regression'"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://playwright.dev")
        assert "Playwright" in page.title()
        browser.close()


@pytest.mark.slow
def test_open_github():
    """Latihan 44: Test kategori 'slow'"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://github.com")
        assert "GitHub" in page.title()
        browser.close()
