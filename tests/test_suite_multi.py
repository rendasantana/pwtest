import pytest
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# 🔹 Daftar halaman yang akan diuji otomatis
test_data = [
    {"url": "https://playwright.dev", "expected": "Playwright"},
    {"url": "https://w3schools.com", "expected": "W3Schools"},
    {"url": "https://python.org", "expected": "Python"},
]

@pytest.mark.parametrize("data", test_data)
def test_multiple_sites(page, data):
    """Test beberapa website dan simpan hasilnya ke log"""
    url = data["url"]
    expected = data["expected"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"🌐 Membuka: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    title = page.title()
    logger.info(f"📄 Judul halaman: {title}")

    try:
        assert expected in title, f"Judul tidak sesuai (diharapkan: {expected})"
        logger.info(f"✅ [PASS] {url} - Judul cocok.")
    except AssertionError as e:
        # Hanya ambil screenshot kalau gagal
        screenshot_path = screenshot_dir / f"{expected}_FAILED_{timestamp}.png"
        page.screenshot(path=str(screenshot_path))
        logger.error(f"❌ [FAIL] {url} - {e}")
        logger.error(f"📸 Screenshot gagal disimpan di: {screenshot_path}")
        raise

    logger.info("-" * 60)
