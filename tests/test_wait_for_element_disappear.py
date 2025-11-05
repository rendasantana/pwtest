import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.waitdisappear
def test_wait_for_element_disappear():
    file_path = f"file://{os.getcwd()}/pages/wait_element_disappear.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buka halaman lokal
        page.goto(file_path)

        # Klik tombol untuk memulai loading
        page.click("#loadBtn")

        # Pastikan teks "Loading..." muncul dulu
        loading = page.locator("#loading")
        expect(loading).to_be_visible()

        # Tunggu sampai loading hilang
        page.wait_for_selector("#loading", state="hidden", timeout=10000)

        # Pastikan hasil muncul
        result = page.locator("#result")
        expect(result).to_have_text("Data berhasil dimuat ✅")

        print("✅ Elemen loading hilang, data berhasil dimuat!")

        browser.close()
