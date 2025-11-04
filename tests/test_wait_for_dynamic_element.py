import pytest
import re
from playwright.sync_api import sync_playwright, expect

@pytest.mark.dynamic
def test_wait_for_dynamic_element():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # 1️⃣ Buka halaman dynamic loading dari Herokuapp
        page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
        expect(page).to_have_title(re.compile("The Internet"))
        print("✅ Halaman dynamic loading terbuka")

        # 2️⃣ Klik tombol 'Start' untuk memulai loading
        page.click("button")
        print("🕒 Proses loading dimulai...")

        # 3️⃣ Tunggu sampai elemen #finish muncul
        page.wait_for_selector("#finish", state="visible", timeout=10000)

        # 4️⃣ Verifikasi bahwa teks “Hello World!” muncul
        message = page.inner_text("#finish")
        assert "Hello World!" in message
        print(f"✅ Pesan muncul: {message}")

        browser.close()
