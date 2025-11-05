import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.waitnavigation
def test_wait_for_navigation():
    base_path = f"file://{os.getcwd()}/pages/wait_navigation_start.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buka halaman awal
        page.goto(base_path)
        expect(page).to_have_title("Wait for Navigation - Start")

        # Klik tombol dan tunggu navigasi selesai
        with page.expect_navigation(timeout=5000):
            page.click("#goBtn")

        # Verifikasi halaman tujuan sudah terbuka
        expect(page).to_have_title("Halaman Tujuan")
        expect(page.locator("h2")).to_have_text("Selamat Datang di Halaman Tujuan 🎉")

        print("✅ Navigasi berhasil ke halaman tujuan!")

        browser.close()
