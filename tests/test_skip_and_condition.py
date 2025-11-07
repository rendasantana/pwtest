import pytest
import sys
from playwright.sync_api import sync_playwright

@pytest.mark.skip(reason="Belum siap untuk dijalankan (fitur masih dalam pengembangan)")
def test_feature_in_progress():
    """Latihan 45: contoh skip permanen"""
    assert False, "Test ini seharusnya dilewati"


@pytest.mark.skipif(sys.platform == "darwin", reason="Lewati test ini di macOS")
def test_skip_on_macos():
    """Latihan 45: skip berdasarkan OS"""
    assert True


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Butuh Python 3.10 atau lebih tinggi")
def test_requires_modern_python():
    """Latihan 45: skip jika versi Python terlalu rendah"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        assert "Example Domain" in page.title()
        browser.close()
