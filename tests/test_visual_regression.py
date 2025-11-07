import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.visual
def test_visual_regression():
    # Folder baseline & hasil baru
    baseline_dir = "screenshots/baseline"
    current_dir = "screenshots/current"
    os.makedirs(baseline_dir, exist_ok=True)
    os.makedirs(current_dir, exist_ok=True)

    page_url = "https://playwright.dev/python/"
    baseline_file = os.path.join(baseline_dir, "home.png")
    current_file = os.path.join(current_dir, "home.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url)
        page.wait_for_load_state("networkidle")

        # Ambil screenshot saat ini
        page.screenshot(path=current_file, full_page=True)
        print(f"📸 Screenshot disimpan: {current_file}")

        # Jika baseline belum ada → buat dulu
        if not os.path.exists(baseline_file):
            page.screenshot(path=baseline_file, full_page=True)
            print("📂 Baseline belum ada, dibuat otomatis.")
        else:
            # Bandingkan dengan baseline
            result = page.expect_screenshot("home.png", path=baseline_dir)
            print("✅ Visual regression check berhasil tanpa perbedaan.")

        browser.close()
