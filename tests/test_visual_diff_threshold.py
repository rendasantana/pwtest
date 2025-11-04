import os
from datetime import datetime
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

BASELINE_DIR = "tests/baseline"
NEWSHOT_DIR = "tests/screenshots"
os.makedirs(BASELINE_DIR, exist_ok=True)
os.makedirs(NEWSHOT_DIR, exist_ok=True)

THRESHOLD = 0.02  # toleransi 2% perbedaan pixel

def compare_images(baseline_path, new_path, diff_path):
    """Bandingkan dua gambar dan buat diff visual"""
    baseline = Image.open(baseline_path).convert("RGB")
    new_image = Image.open(new_path).convert("RGB")

    # Hitung diff
    diff = ImageChops.difference(baseline, new_image)
    diff_bbox = diff.getbbox()

    if diff_bbox:
        # Hitung persentase pixel beda
        diff_pixels = sum(1 for px in diff.getdata() if px != (0, 0, 0))
        total_pixels = baseline.size[0] * baseline.size[1]
        diff_ratio = diff_pixels / total_pixels

        print(f"🔍 Perbedaan terdeteksi: {diff_ratio*100:.2f}%")

        if diff_ratio > THRESHOLD:
            diff.save(diff_path)
            print(f"❌ Visual berubah signifikan! Diff disimpan di {diff_path}")
            return False
        else:
            print("✅ Perbedaan kecil (masih dalam toleransi).")
            return True
    else:
        print("✅ Tidak ada perbedaan visual sama sekali.")
        return True


def test_visual_diff_threshold():
    """Tes visual regression dengan toleransi threshold"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman target
        page.goto("https://playwright.dev/python/")
        page.wait_for_load_state("domcontentloaded")

        # 2️⃣ Screenshot hasil baru
        new_path = os.path.join(NEWSHOT_DIR, "homepage_new.png")
        page.screenshot(path=new_path, full_page=True)

        # 3️⃣ Cek baseline
        baseline_path = os.path.join(BASELINE_DIR, "homepage.png")
        if not os.path.exists(baseline_path):
            page.screenshot(path=baseline_path, full_page=True)
            print("✅ Baseline pertama dibuat:", baseline_path)
            browser.close()
            return

        # 4️⃣ Bandingkan dengan baseline
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        diff_path = os.path.join(NEWSHOT_DIR, f"diff_homepage_{timestamp}.png")
        result = compare_images(baseline_path, new_path, diff_path)

        assert result, "Visual berbeda melebihi toleransi!"

        browser.close()
