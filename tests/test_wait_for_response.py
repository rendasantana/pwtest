import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.waitresponse
def test_wait_for_response():
    file_path = f"file://{os.getcwd()}/pages/wait_for_response.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buka halaman lokal
        page.goto(file_path)

        # Jalankan aksi klik tombol
        with page.expect_response("**/posts/1") as response_info:
            page.click("#fetchBtn")

        # Ambil response
        response = response_info.value
        assert response.ok
        data = response.json()

        # Verifikasi hasil tampil di halaman
        expect(page.locator("#status")).to_have_text("✅ Data diterima!")
        expect(page.locator("#result")).to_contain_text(data["title"])

        print(f"✅ Respon diterima: {data['title']}")
        browser.close()
