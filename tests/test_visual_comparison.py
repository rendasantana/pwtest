from playwright.sync_api import sync_playwright, expect
import os

def test_visual_comparison():
    # 📁 Folder penyimpanan hasil visual test
    baseline_folder = "reports/visual_baseline"
    diff_folder = "reports/visual_diff"
    os.makedirs(baseline_folder, exist_ok=True)
    os.makedirs(diff_folder, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman yang akan divalidasi
        page.goto("https://demo.playwright.dev/todomvc/")
        page.wait_for_selector(".new-todo")

        # 2️⃣ Ambil screenshot terbaru
        current_screenshot = f"{diff_folder}/current.png"
        page.screenshot(path=current_screenshot, full_page=True)

        # 3️⃣ Path baseline image
        baseline_image = f"{baseline_folder}/baseline.png"

        # 4️⃣ Jika baseline belum ada → simpan pertama kali
        if not os.path.exists(baseline_image):
            page.screenshot(path=baseline_image, full_page=True)
            print("✅ Baseline image dibuat pertama kali.")
        else:
            # 5️⃣ Bandingkan hasil baru dengan baseline
            comparison = page.expect_screenshot(
                "baseline.png",
                path=baseline_folder,
                max_diff_pixel_ratio=0.05
            )
            print("✅ Perbandingan visual berhasil:", comparison)

        browser.close()
