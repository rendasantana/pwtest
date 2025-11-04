import pytest
import re
from playwright.sync_api import sync_playwright, expect

@pytest.mark.navigation
def test_wait_for_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # 1️⃣ Buka halaman utama
        page.goto("https://www.w3schools.com/")
        expect(page).to_have_title(re.compile("W3Schools"))
        print("✅ Halaman utama terbuka")

        # 2️⃣ Klik link dan tunggu navigasi ke halaman HTML
        with page.expect_navigation(url=re.compile(".*/html/.*"), wait_until="domcontentloaded", timeout=60000):
            page.get_by_role("link", name="Learn HTML").click()

        print("✅ Navigasi berhasil ke halaman HTML")

        # 3️⃣ Verifikasi halaman tujuan
        expect(page).to_have_url(re.compile(".*/html/.*"))
        heading = page.locator("h1.with-bookmark")
        expect(heading).to_be_visible()
        print("✅ Halaman HTML Tutorial tampil dengan heading utama")

        browser.close()
