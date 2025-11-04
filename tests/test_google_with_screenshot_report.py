import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright

# Direktori laporan screenshot
REPORT_DIR = "reports/screenshots"
os.makedirs(REPORT_DIR, exist_ok=True)

@pytest.fixture(scope="session")
def browser_context():
    """Fixture Playwright browser"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """Ambil screenshot otomatis saat test gagal"""
    yield
    outcome = request.node.rep_call
    if outcome.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(REPORT_DIR, f"{test_name}_{timestamp}.png")

        # Dapatkan page dari fixture kalau tersedia
        page = request.node.funcargs.get("page")
        if page:
            page.screenshot(path=screenshot_path)
            # Tambahkan screenshot ke laporan pytest-html
            if hasattr(request.config, "_html"):
                extra = getattr(request.config, "_html").extras
                extra.append(pytest_html.extras.image(screenshot_path, mime_type="image/png"))
            print(f"📸 Screenshot disimpan: {screenshot_path}")
        else:
            print("⚠️ Tidak ada page untuk di-screenshot")

def pytest_runtest_makereport(item, call):
    """Hook pytest untuk akses status test (pass/fail)"""
    if "screenshot_on_failure" in item.fixturenames:
        if call.when == "call":
            item.rep_call = call

def test_google_search(browser_context):
    """Test pencarian Google (dengan screenshot jika gagal)"""
    page = browser_context.new_page()
    page.goto("https://www.google.com/?hl=en")

    page.fill("textarea[name='q']", "Playwright Python")
    page.keyboard.press("Enter")
    page.wait_for_selector("text=Playwright")  # Pastikan hasil muncul

    # ❌ Bikin error sengaja supaya screenshot muncul
    assert page.is_visible("text=Hasil Tidak Ada")

    page.close()
