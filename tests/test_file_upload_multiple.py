import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.fileuploadmultiple
def test_file_upload_multiple(tmp_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Akses halaman HTML lokal
        upload_page = f"file://{os.getcwd()}/pages/file_upload_multiple.html"
        page.goto(upload_page)

        # Buat beberapa file dummy untuk diupload
        file1 = tmp_path / "test_file1.txt"
        file2 = tmp_path / "test_file2.txt"
        file3 = tmp_path / "test_file3.txt"
        for f in [file1, file2, file3]:
            f.write_text(f"Isi dari {f.name}")

        # Upload beberapa file
        page.set_input_files("#multiUpload", [str(file1), str(file2), str(file3)])

        # Verifikasi hasil upload
        uploaded_files = page.locator("#fileList li").all_inner_texts()
        expected_files = [f.name for f in [file1, file2, file3]]

        assert set(uploaded_files) == set(expected_files), f"❌ File upload tidak sesuai: {uploaded_files}"

        print("✅ Semua file berhasil diupload:", uploaded_files)

        context.close()
        browser.close()
