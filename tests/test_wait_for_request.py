import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.waitrequest
def test_wait_for_request():
    file_path = f"file://{os.getcwd()}/pages/wait_for_request.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buka halaman lokal
        page.goto(file_path)

        # Tunggu request dikirim ke endpoint tertentu
        with page.expect_request("**/posts") as request_info:
            page.click("#sendBtn")

        request = request_info.value
        print(f"✅ Request terkirim ke: {request.url}")
        print(f"📦 Method: {request.method}")
        print(f"📤 Body: {request.post_data}")

        # Pastikan UI menampilkan hasil
        expect(page.locator("#status")).to_have_text("✅ Request terkirim!")
        expect(page.locator("#result")).to_contain_text("ID data baru")

        browser.close()
