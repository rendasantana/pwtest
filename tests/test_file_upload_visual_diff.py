import os
from playwright.sync_api import sync_playwright, expect
from PIL import Image, ImageChops, ImageDraw

def compare_images(baseline_path, new_path, diff_path):
    """Bandingkan dua gambar dan buat visual diff."""
    baseline = Image.open(baseline_path).convert("RGB")
    new = Image.open(new_path).convert("RGB")

    diff = ImageChops.difference(baseline, new)

    # Tandai area perbedaan dengan kotak merah
    bbox = diff.getbbox()
    if bbox:
        draw = ImageDraw.Draw(new)
        draw.rectangle(bbox, outline="red", width=5)
        new.save(diff_path)
        print(f"⚠️ Perbedaan ditemukan. File diff disimpan di: {diff_path}")
        return False
    else:
        print("✅ Tidak ada perbedaan visual ditemukan.")
        return True


def test_file_upload_visual_diff(snapshot_dir="tests-output/screenshots"):
    os.makedirs(snapshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman upload
        page.goto("https://the-internet.herokuapp.com/upload", timeout=60000)

        # 2️⃣ Pastikan file ada
        file_path = os.path.abspath("tests/sample_upload.png")
        assert os.path.exists(file_path), f"❌ File tidak ditemukan: {file_path}"
        print(f"✅ File ditemukan di: {file_path}")

        # 3️⃣ Upload file
        page.set_input_files("#file-upload", file_path)
        page.click("#file-submit")

        # 4️⃣ Verifikasi teks konfirmasi
        expect(page.locator("h3")).to_have_text("File Uploaded!")

        # 5️⃣ Screenshot hasil upload
        new_path = os.path.join(snapshot_dir, "uploaded_result.png")
        baseline_path = os.path.join(snapshot_dir, "baseline_uploaded.png")
        diff_path = os.path.join(snapshot_dir, "diff_uploaded.png")

        page.screenshot(path=new_path, full_page=True)

        # 6️⃣ Bandingkan hasil dengan baseline
        if not os.path.exists(baseline_path):
            page.screenshot(path=baseline_path, full_page=True)
            print("✅ Baseline dibuat pertama kali.")
        else:
            is_same = compare_images(baseline_path, new_path, diff_path)
            assert is_same, "❌ Visual difference detected!"

        browser.close()
