import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.dialog
def test_handle_alert_confirm_prompt():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 🔹 1. Buka halaman demo
        page.goto("https://the-internet.herokuapp.com/javascript_alerts")

        # 🔹 2. Tangani alert biasa
        def handle_alert(dialog):
            print(f"Alert text: {dialog.message}")
            dialog.accept()  # Klik OK

        page.once("dialog", handle_alert)
        page.click("text=Click for JS Alert")
        expect(page.locator("#result")).to_have_text("You successfully clicked an alert")

        # 🔹 3. Tangani confirm (OK / Cancel)
        def handle_confirm(dialog):
            print(f"Confirm text: {dialog.message}")
            dialog.dismiss()  # Klik Cancel

        page.once("dialog", handle_confirm)
        page.click("text=Click for JS Confirm")
        expect(page.locator("#result")).to_have_text("You clicked: Cancel")

        # 🔹 4. Tangani prompt (isi input)
        def handle_prompt(dialog):
            print(f"Prompt text: {dialog.message}")
            dialog.accept("Renda QA")  # Isi teks lalu OK

        page.once("dialog", handle_prompt)
        page.click("text=Click for JS Prompt")
        expect(page.locator("#result")).to_have_text("You entered: Renda QA")

        browser.close()
