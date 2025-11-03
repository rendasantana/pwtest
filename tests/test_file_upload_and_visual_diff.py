from playwright.sync_api import sync_playwright, expect
import pytest
import os
from PIL import Image, ImageChops

BASE_URL = "https://the-internet.herokuapp.com/upload"
UPLOAD_FILE = "tests/sample_upload.png"  # pastikan file ini ada
VISUAL_BASELINE_DIR = "visual_baseline"
VISUAL_RESULT_DIR = "visual_result"
VISUAL_DIFF_DIR = "visual_diff"

# Buat folder jika belum ada
for folder in [VISUAL_BASELINE_DIR, VISUAL_RESULT_DIR, VISUAL_DIFF_DIR]:
    os.makedirs(folder, exist_ok=True)


def compare_images(baseline_path, result_path, diff_path):
    """Bandingkan 2 gambar dan simpan diff jika berbeda"""
    base = Image.open(baseline_path).convert("RGB")
    result = Image.open(result_path).convert("RGB")

    diff = ImageChops.difference(base, result)
    if diff.getbbox():
        diff.save(diff_path)
        return False  # ada perbedaan
    return True  # identik


def test_file_upload_and_visual_diff(record_property):
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

        # 4️⃣ Screenshot hasil upload
        result_path = f"{VISUAL_RESULT_DIR}/result_upload.png"
        page.screenshot(path=result_path, full_page=True)
        record_property("result_screenshot", result_path)

        # 5️⃣ Visual regression check
        baseline_path = f"{VISUAL_BASELINE_DIR}/result_upload.png"
        diff_path = f"{VISUAL_DIFF_DIR}/diff_upload.png"

        if not os.path.exists(baseline_path):
            # Belum ada baseline → buat baseline pertama
            page.screenshot(path=baseline_path, full_page=True)
            print(f"📸 Baseline dibuat: {baseline_path}")
        else:
            # Bandingkan screenshot dengan baseline
            same = compare_images(baseline_path, result_path, diff_path)
            if same:
                print("✅ Tampilan masih sama seperti baseline.")
            else:
                print(f"⚠️ Perbedaan visual terdeteksi! Diff disimpan di: {diff_path}")
                record_property("diff_image", diff_path)
                assert same, "Visual regression detected — tampilan berubah!"

        context.close()
        browser.close()
