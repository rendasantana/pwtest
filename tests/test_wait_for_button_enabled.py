import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.waitbutton
def test_wait_for_button_enabled():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.lambdatest.com/selenium-playground/dynamic-data-loading-demo")

        # Pastikan tombol ada
        button = page.locator("#save")
        expect(button).to_be_visible()

        # Simulasikan: tombol dinonaktifkan dulu
        page.evaluate("document.querySelector('#save').disabled = true")
        expect(button).to_be_disabled()

        # Setelah 3 detik, tombol diaktifkan
        page.evaluate("setTimeout(() => document.querySelector('#save').disabled = false, 3000)")

        # Tunggu sampai tombol aktif
        page.wait_for_function("!document.querySelector('#save').disabled")

        # Verifikasi tombol aktif
        expect(button).to_be_enabled()

        # Klik tombol setelah aktif
        button.click()
        print("✅ Tombol berhasil diklik setelah aktif")

        browser.close()
