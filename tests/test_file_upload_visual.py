import os
from playwright.sync_api import sync_playwright, expect

def test_file_upload_and_visual(snapshot_dir="tests-output/screenshots"):
    os.makedirs(snapshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman upload
        page.goto(
            "https://the-internet.herokuapp.com/upload",
            timeout=60000,
            wait_until="domcontentloaded"
        )

        # 2️⃣ Pastikan file upload ada
        file_path = os.path.abspath("tests/sample_upload.png")
        assert os.path.exists(file_path), f"❌ File tidak ditemukan: {file_path}"

        print(f"✅ File ditemukan di: {file_path}")

        # 3️⃣ Upload file
        page.set_input_files("#file-upload", file_path)

        # 4️⃣ Klik tombol upload
        page.click("#file-submit")

        # 5️⃣ Verifikasi teks konfirmasi
        expect(page.locator("h3")).to_have_text("File Uploaded!")

        # 6️⃣ Ambil screenshot hasil upload
        screenshot_path = os.path.join(snapshot_dir, "uploaded_result.png")
        page.screenshot(path=screenshot_path, full_page=True)

        # 7️⃣ Visual regression (bandingkan dengan baseline)
        baseline_path = os.path.join(snapshot_dir, "baseline_uploaded.png")

        if not os.path.exists(baseline_path):
            page.screenshot(path=baseline_path, full_page=True)
            print("✅ Baseline dibuat pertama kali.")
        else:
            comparison = page.expect_screenshot_to_match_snapshot(name="uploaded_result.png")
            print("🔍 Hasil visual test:", comparison)

        browser.close()
