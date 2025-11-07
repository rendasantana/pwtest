import pytest
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

@pytest.mark.screenshotsteps
def test_screenshot_steps():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Buat folder untuk simpan screenshot per step
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_path = os.path.join("reports", f"screenshots_{timestamp}")
        os.makedirs(folder_path, exist_ok=True)

        def capture_step(name):
            path = os.path.join(folder_path, f"{name}.png")
            page.screenshot(path=path)
            print(f"📸 Screenshot disimpan: {path}")

        # Step 1: Buka halaman Playwright
        page.goto("https://playwright.dev/python/")
        capture_step("01_homepage")

        # Step 2: Klik link "Get started"
        page.get_by_role("link", name="Get started").click()
        capture_step("02_get_started")

        # Step 3: Scroll ke bawah dan ambil screenshot dokumentasi
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(1000)
        capture_step("03_scrolled_doc")

        # Step 4: Cari teks tertentu
        content = page.text_content("body")
        assert "Playwright for Python" in content, "❌ Konten tidak ditemukan!"
        capture_step("04_validation_passed")

        print("✅ Semua step berjalan lancar!")
        context.close()
        browser.close()
