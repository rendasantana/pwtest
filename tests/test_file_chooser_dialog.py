import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.filechooser
def test_file_chooser_dialog(tmp_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Buka halaman demo upload
        upload_page = f"file://{os.getcwd()}/pages/file_upload_demo.html"
        page.goto(upload_page)

        # Path file yang mau diupload
        file_to_upload = os.path.join(os.getcwd(), "pages", "sample_upload.txt")
        assert os.path.exists(file_to_upload), "❌ File upload tidak ditemukan!"

        # Tangkap dialog file chooser saat tombol diklik
        with page.expect_file_chooser() as fc_info:
            page.click("#uploadButton")  # tombol upload di halaman demo
        file_chooser = fc_info.value

        # Pilih file secara otomatis
        file_chooser.set_files(file_to_upload)

        # Verifikasi hasil upload tampil di halaman
        uploaded_text = page.locator("#uploadedFileName")
        expect(uploaded_text).to_have_text("sample_upload.txt")

        print("✅ File chooser dialog berhasil di-handle dan file diupload!")

        context.close()
        browser.close()
