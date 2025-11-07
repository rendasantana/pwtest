import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.video
def test_video_record_on_fail(tmp_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=str(tmp_path))  # perbaikan di sini

        page = context.new_page()
        page.goto("https://example.com")

        # Simulasikan test gagal
        assert page.title() == "Playwright Example", "Judul tidak sesuai (test ini memang sengaja dibuat gagal)."

        context.close()
        browser.close()
