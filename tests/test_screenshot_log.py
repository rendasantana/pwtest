import pytest
from datetime import datetime

@pytest.mark.parametrize("url, expected_title", [
    ("https://playwright.dev", "Playwright"),
    ("https://w3schools.com", "W3Schools")
])
def test_open_page_and_screenshot(page, url, expected_title):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n[INFO] Membuka halaman: {url}")

    # Gunakan DOMContentLoaded agar lebih cepat dan aman
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    title = page.title()
    print(f"[INFO] Judul halaman: {title}")

    screenshot_path = f"reports/screenshots/{expected_title}_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    print(f"[INFO] Screenshot disimpan di: {screenshot_path}")

    # Verifikasi judul sesuai dengan yang diharapkan
    assert expected_title in title, f"Judul halaman tidak sesuai: {title}"
