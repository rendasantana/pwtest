import os
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

# Buat folder baseline & hasil baru
BASELINE_DIR = "tests/baseline"
NEWSHOT_DIR = "tests/screenshots"
os.makedirs(BASELINE_DIR, exist_ok=True)
os.makedirs(NEWSHOT_DIR, exist_ok=True)

def test_visual_regression():
    """Tes visual regression antara tampilan lama & baru"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman target
        page.goto("https://playwright.dev/python/")
        page.wait_for_load_state("domcontentloaded")

        # 2️⃣ Screenshot per langkah
        step1_path = os.path.join(NEWSHOT_DIR, "step1_homepage.png")
        page.screenshot(path=step1_path, full_page=True)

        # 3️⃣ Verifikasi elemen utama ada
        expect(page.locator("text=Get started")).to_be_visible()

        # 4️⃣ Simpan screenshot hasil akhir
        new_screenshot = os.path.join(NEWSHOT_DIR, "homepage_new.png")
        page.screenshot(path=new_screenshot, full_page=True)

        # 5️⃣ Cek apakah baseline sudah ada
        baseline_path = os.path.join(BASELINE_DIR, "homepage.png")
        if not os.path.exists(baseline_path):
            # Simpan sebagai baseline pertama kali
            page.screenshot(path=baseline_path, full_page=True)
            print("✅ Baseline pertama dibuat:", baseline_path)
        else:
            # 6️⃣ Bandingkan dengan baseline
            print("🔍 Membandingkan tampilan baru dengan baseline...")
            try:
                page.expect_screenshot_to_match_snapshot(name="homepage.png")
                print("✅ Tidak ada perubahan visual.")
            except Exception as e:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                diff_path = os.path.join(NEWSHOT_DIR, f"diff_{timestamp}.png")
                page.screenshot(path=diff_path, full_page=True)
                print("❌ Perubahan visual terdeteksi! Diff disimpan:", diff_path)

        browser.close()
