import pytest
from playwright.sync_api import sync_playwright
import os
import datetime

@pytest.mark.screenshotfail
def test_screenshot_on_fail():
    screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 🧭 Akses halaman
            page.goto("https://example.com")
            page.wait_for_timeout(1000)

            # ❌ Simulasikan kegagalan (assert salah)
            heading = page.locator("h1").inner_text()
            assert "Playwright" in heading, "Judul tidak sesuai yang diharapkan!"

        except AssertionError as e:
            # 📸 Screenshot otomatis
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(screenshot_dir, f"fail_{timestamp}.png")
            page.screenshot(path=file_path, full_page=True)
            print(f"❌ Test gagal! Screenshot disimpan di: {file_path}")
            raise e

        finally:
            browser.close()
