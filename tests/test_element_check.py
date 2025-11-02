import pytest
from datetime import datetime
import time

@pytest.mark.parametrize("url, selector, expected_text", [
    ("https://playwright.dev", "a.getStarted_Sjon", "Get started"),
    ("https://www.w3schools.com", "#navbtn_tutorials", "Tutorials"),
])
def test_element_visible_and_text(page, url, selector, expected_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n[INFO] Membuka halaman: {url}")
    page.goto(url)
    page.wait_for_load_state("networkidle")

    try:
        time.sleep(2)  # beri jeda biar elemen tampil stabil

        element = page.locator(selector)
        element.wait_for(state="visible", timeout=15000)
        text = element.inner_text()
        print(f"[INFO] Elemen ditemukan: {selector}")
        print(f"[INFO] Teks elemen: {text}")
        assert expected_text.lower() in text.lower(), f"Teks tidak sesuai! Ditemukan: {text}"
    except Exception as e:
        print(f"[ERROR] {e}")
        screenshot_path = f"reports/screenshots/FAILED_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        raise AssertionError(f"Gagal memvalidasi elemen: {selector}")

    screenshot_path = f"reports/screenshots/SUCCESS_{timestamp}.png"
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"[INFO] Screenshot disimpan di: {screenshot_path}")
