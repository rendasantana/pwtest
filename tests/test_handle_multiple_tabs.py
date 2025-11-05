import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.multipletabs
def test_handle_multiple_tabs_local():
    base_path = f"file://{os.getcwd()}/pages/multi_tabs_demo.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(base_path)
        print("Tab utama dibuka")

        # Locator pasti visible
        link = page.locator("#openTab")
        link.wait_for(state="visible", timeout=5000)

        # Klik link dan tunggu tab baru
        with context.expect_page() as new_page_info:
            link.click()
        new_page = new_page_info.value

        new_page.wait_for_load_state()
        assert "Tab Baru" in new_page.title()
        print(f"Tab baru terbuka: {new_page.url}")

        page.bring_to_front()
        print("Kembali ke tab utama")

        browser.close()
