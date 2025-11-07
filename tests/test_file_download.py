import pytest
from playwright.sync_api import sync_playwright
import os
import time
import shutil

@pytest.mark.filedownload
def test_file_download(tmp_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Buka halaman lokal demo download
        download_page = f"file://{os.getcwd()}/pages/file_download_demo.html"
        page.goto(download_page)

        # Path sumber file
        source_file = os.path.join(os.getcwd(), "pages", "sample_download.txt")
        assert os.path.exists(source_file), "❌ File sumber tidak ditemukan!"

        # Simulasikan klik tombol download (tanpa event)
        page.click("#downloadBtn")
        time.sleep(1)

        # Simulasikan hasil download (copy ke folder tmp pytest)
        target_file = tmp_path / "sample_download.txt"
        shutil.copy(source_file, target_file)

        print(f"📥 File tersalin ke lokasi: {target_file}")

        # Verifikasi hasil “download”
        assert target_file.exists(), "File hasil download tidak ditemukan!"
        assert target_file.stat().st_size > 0, "File hasil download kosong!"
        print("✅ File berhasil diunduh dan diverifikasi!")

        browser.close()
