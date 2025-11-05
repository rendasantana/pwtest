import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.waitelement
def test_wait_for_element_appear():
    # Buat path absolut ke file HTML lokal
    file_path = f"file://{os.getcwd()}/pages/wait_element_appear.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buka halaman lokal
        page.goto(file_path)

        # Klik tombol untuk memunculkan elemen
        page.click("#loadBtn")

        # Tunggu sampai <p> muncul di dalam #loading
        page.wait_for_selector("#loading p", timeout=10000)

        # Verifikasi elemen tampil
        element = page.locator("#loading p")
        expect(element).to_be_visible()

        print("✅ Elemen berhasil muncul setelah delay!")

        browser.close()
