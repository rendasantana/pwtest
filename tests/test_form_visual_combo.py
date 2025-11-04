from playwright.sync_api import sync_playwright, expect
import os
import time
import re


def test_form_visual_combo(record_property):
    base_url = "file://" + os.path.abspath("pages/form_test.html")
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # 📁 Folder hasil
    reports_dir = "reports/screenshots_combo"
    os.makedirs(reports_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman form
        page.goto(base_url, timeout=60000)
        page.wait_for_load_state("domcontentloaded")

        # 2️⃣ Isi form (First name + Last name)
        page.fill('input[name="firstname"]', "Renda")
        page.fill('input[name="lastname"]', "Santana")

        # 3️⃣ Screenshot sebelum submit
        before_path = f"{reports_dir}/before_submit_{timestamp}.png"
        page.screenshot(path=before_path, full_page=False)
        record_property("Before Submit", before_path)

        # 4️⃣ Klik tombol Submit
        page.click('input[type="submit"]')

        # 5️⃣ Tunggu redirect & ambil screenshot sesudah
        page.wait_for_timeout(2000)
        after_path = f"{reports_dir}/after_submit_{timestamp}.png"
        page.screenshot(path=after_path, full_page=False)
        record_property("After Submit", after_path)

        # 6️⃣ Validasi visual
        expect(page).to_have_url(re.compile("thankyou.html"))

        print("✅ Form berhasil disubmit dan visual tersimpan.")
        browser.close()
