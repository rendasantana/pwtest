import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.iframe
def test_handle_iframe():
    file_path = f"file://{os.getcwd()}/pages/iframe_demo.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(file_path)

        # Pilih frame
        frame = page.frame(name="demoFrame")  # pakai id frame sebagai name
        assert frame is not None, "Frame tidak ditemukan"

        # Klik tombol di dalam frame
        frame.locator("#frameBtn").click()

        # Verifikasi teks muncul
        frame.locator("#frameResult").wait_for(state="visible", timeout=5000)
        result_text = frame.locator("#frameResult").inner_text()
        assert result_text == "Tombol di iFrame berhasil diklik!"
        print(f"✅ Hasil di iFrame: {result_text}")

        browser.close()
