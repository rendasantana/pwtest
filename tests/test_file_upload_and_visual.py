from playwright.sync_api import sync_playwright, expect
import pytest
import os

BASE_URL = "https://the-internet.herokuapp.com/upload"
UPLOAD_FILE = "tests/sample_upload.png"  # pastikan file ini ada
VISUAL_BASELINE_DIR = "visual_baseline"
VISUAL_DIFF_DIR = "visual_diff"

# Buat folder baseline dan diff jika belum ada
os.makedirs(VISUAL_BASELINE_DIR, exist_ok=True)
os.makedirs(VISUAL_DIFF_DIR, exist_ok=True)

def test_file_upload_and_visual_check(record_property):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1️⃣ Kunjungi halaman upload
        page.goto(BASE_URL)
        record_property("url", page.url)
        expect(page).to_have_title("The Internet")

        # 2️⃣ Upload file
        file_input = page.locator("#file-upload")
        file_input.set_input_files(UPLOAD_FILE)
        page.click("#file-submit")

        # 3️⃣ Verifikasi hasil upload sukses
        expect(page.locator("h3")).to_have_text("File Uploaded!")
        uploaded_filename = page.locator("#uploaded-files").inner_text()
        assert uploaded_filename == os.path.basename(UPLOAD_FILE)
        record_property("uploaded_file", uploaded_filename)

        # 4️⃣ Ambil screenshot hasil upload
        screenshot_path = f"{VISUAL_DIFF_DIR}/result_upload.png"
        page.screenshot(path=screenshot_path, full_page=True)
        record_property("screenshot", screenshot_path)

        # 5️⃣ Visual regression test
        baseline_path = f"{VISUAL_BASELINE_DIR}/result_upload.png"

        if not os.path.exists(baseline_path):
            # Jika belum ada baseline → simpan sebagai baseline
            page.screenshot(path=baseline_path, full_page=True)
            print(f"Baseline image dibuat di: {baseline_path}")
        else:
            # Bandingkan dengan baseline
            comparison = page.expect_screenshot(path="result_upload.png", full_page=True)
            comparison.to_match_snapshot("result_upload.png")

        context.close()
        browser.close()
