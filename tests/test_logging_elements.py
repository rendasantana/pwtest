import os
from playwright.sync_api import sync_playwright, expect
import pytest

LOG_DIR = "tests-output/logs"
SCREENSHOT_DIR = "tests-output/element_screenshots"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def test_logging_elements_and_screenshot(record_property):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman
        page.goto("https://the-internet.herokuapp.com/add_remove_elements/")

        # 2️⃣ Tambah beberapa elemen
        for _ in range(3):
            page.click("button[onclick='addElement()']")

        # 3️⃣ Ambil semua tombol "Delete"
        delete_buttons = page.locator("button.added-manually")
        count = delete_buttons.count()
        print(f"🧩 Jumlah tombol Delete: {count}")
        record_property("delete_button_count", count)

        # 4️⃣ Screenshot setiap tombol Delete
        for i in range(count):
            btn = delete_buttons.nth(i)
            text = btn.inner_text()
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"delete_button_{i+1}.png")
            btn.screenshot(path=screenshot_path)
            print(f"📸 Screenshot tombol '{text}' disimpan di: {screenshot_path}")

        # 5️⃣ Hapus satu tombol dan log hasil
        delete_buttons.first.click()
        remaining = page.locator("button.added-manually").count()
        print(f"🧹 Sisa tombol setelah hapus: {remaining}")
        record_property("remaining_after_delete", remaining)

        # 6️⃣ Simpan log hasil ke file
        log_file = os.path.join(LOG_DIR, "element_log.txt")
        with open(log_file, "w") as f:
            f.write(f"Total tombol awal: {count}\n")
            f.write(f"Sisa tombol setelah hapus: {remaining}\n")

        print(f"🗒️ Log hasil disimpan di: {log_file}")
        record_property("log_file", log_file)

        browser.close()
