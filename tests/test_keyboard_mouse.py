import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.keyboardmouse
def test_keyboard_mouse_actions():
    file_path = f"file://{os.getcwd()}/pages/keyboard_mouse_demo.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(file_path)

        # 📝 Keyboard type
        input_field = page.locator("#inputField")
        input_field.click()
        input_field.fill("")  # kosongkan dulu
        page.keyboard.type("Renda QA")
        page.keyboard.press("Enter")  # optional

        # 🖱️ Klik tombol Submit
        page.locator("#submitBtn").click()

        # Verifikasi hasil input
        result = page.locator("#result")
        result.wait_for(state="visible")
        assert "Halo, Renda QA!" in result.inner_text()
        print(f"✅ Hasil input: {result.inner_text()}")

        # 🔹 Drag & Drop manual
        source = page.locator("#dragSource")
        target = page.locator("#dropTarget")

        # 🔹 Drag & Drop via JS
        page.evaluate("""
        const source = document.querySelector('#dragSource');
        const target = document.querySelector('#dropTarget');
        const dataTransfer = new DataTransfer();
        source.dispatchEvent(new DragEvent('dragstart', { dataTransfer }));
        target.dispatchEvent(new DragEvent('dragover', { dataTransfer }));
        target.dispatchEvent(new DragEvent('drop', { dataTransfer }));
        source.dispatchEvent(new DragEvent('dragend', { dataTransfer }));
        """)


        # Verifikasi drag & drop berhasil
        drop_text = target.inner_text()
        assert drop_text == "Dropped!"
        print(f"✅ Drag & Drop berhasil: {drop_text}")

        browser.close()
