import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parallel
@pytest.mark.parametrize("url", [
    "https://example.com",
    "https://playwright.dev",
    "https://github.com",
    "https://google.com"
])
def test_parallel_example(url):
    """Latihan 43: Menjalankan beberapa test URL secara paralel"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        print(f"✅ Membuka: {url} | Judul: {title}")
        assert title != "", f"❌ Halaman {url} tidak memiliki title!"
        browser.close()
