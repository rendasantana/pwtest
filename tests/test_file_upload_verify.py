import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.fileupload
def test_file_upload_and_verify():
    file_path = f"file://{os.getcwd()}/pages/file_upload_demo.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(file_path)

        # Pilih file lokal untuk upload
        test_file = os.path.join(os.getcwd(), "pages", "sample_upload.txt")
        page.set_input_files("#fileInput", test_file)
        page.click("#uploadBtn")

        # Tunggu hasil muncul
        uploaded_name = page.locator("#uploadedFileName")
        uploaded_name.wait_for(state="visible")

        # Verifikasi nama file
        text_result = uploaded_name.inner_text()
        assert "sample_upload.txt" in text_result
        print(f"✅ File berhasil diupload: {text_result}")

        browser.close()
