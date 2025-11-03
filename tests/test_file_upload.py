import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

# setup logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_file_upload(record_property):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        logs = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        def log(msg):
            logger.info(msg)
            logs.append(msg)
            print(msg)

        log("🔹 Membuka halaman upload...")
        page.goto("https://the-internet.herokuapp.com/upload", timeout=60000)
        log("✅ Halaman upload terbuka.")

        upload_input = page.locator("#file-upload")
        expect(upload_input).to_be_visible()
        log("✅ Input upload terlihat di halaman.")

        dummy_file_path = os.path.abspath("uploads/sample.txt")
        os.makedirs("uploads", exist_ok=True)
        with open(dummy_file_path, "w") as f:
            f.write("Hello from Playwright automation!")

        log(f"📄 File dummy dibuat: {dummy_file_path}")

        upload_input.set_input_files(dummy_file_path)
        page.locator("#file-submit").click()

        success_msg = page.locator("h3")
        expect(success_msg).to_have_text("File Uploaded!")
        log("✅ Upload berhasil diverifikasi!")

        screenshot_path = os.path.join(screenshot_dir, f"upload_success_{timestamp}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        log(f"📸 Screenshot hasil upload disimpan di: {screenshot_path}")

        record_property("Log Detail", "\n".join(logs))

        browser.close()
