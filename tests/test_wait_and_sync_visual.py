from playwright.sync_api import sync_playwright, expect
import os
from datetime import datetime

def test_wait_and_sync_visual():
    # 🗂️ Buat folder untuk hasil screenshot
    folder = "reports/screenshots_wait"
    os.makedirs(folder, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman dengan delay
        page.goto("https://demo.playwright.dev/todomvc/")
        page.screenshot(path=f"{folder}/1_page_loaded.png")

        # 2️⃣ Tunggu elemen utama (input form) muncul
        page.wait_for_selector(".new-todo")
        page.screenshot(path=f"{folder}/2_input_ready.png")

        # 3️⃣ Isi form setelah input siap
        page.fill(".new-todo", "Belajar Playwright Wait")
        page.screenshot(path=f"{folder}/3_text_filled.png")

        # 4️⃣ Tekan Enter untuk menambahkan item
        page.press(".new-todo", "Enter")
        page.screenshot(path=f"{folder}/4_item_submitted.png")

        # 5️⃣ Tunggu item muncul di daftar
        page.wait_for_selector(".todo-list li")
        page.screenshot(path=f"{folder}/5_item_appeared.png")

        # 6️⃣ Verifikasi teksnya
        text = page.text_content(".todo-list li")
        assert "Belajar Playwright Wait" in text
        page.screenshot(path=f"{folder}/6_verification_done.png")

        browser.close()
