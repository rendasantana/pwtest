import pytest
from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# Pastikan folder reports ada
os.makedirs("reports/screenshots", exist_ok=True)

@pytest.fixture(scope="function")
def page_context(request):
    """Setup browser, ambil screenshot jika gagal, dan log hasil"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page  # di sini test dijalankan

        # ambil status test setelah selesai
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            with open("reports/test_log.txt", "a") as f:
                f.write(f"[{timestamp}] ❌ FAILED: {test_name}\nScreenshot: {screenshot_path}\n\n")
        else:
            with open("reports/test_log.txt", "a") as f:
                f.write(f"[{timestamp}] ✅ PASSED: {test_name}\n\n")

        browser.close()


def test_google_search(page_context):
    """Tes validasi pencarian dengan sengaja dibuat gagal"""
    page = page_context
    page.goto("https://duckduckgo.com/")
    page.fill("input[name='q']", "Playwright Python")
    page.keyboard.press("Enter")
    page.wait_for_selector("#links")
    # sengaja bikin gagal untuk uji screenshot
    assert page.is_visible("text=Hasil Tidak Ada")


def test_title(page_context):
    """Tes sederhana yang pasti lolos"""
    page = page_context
    page.goto("https://playwright.dev/python/")
    assert "Playwright" in page.title()
