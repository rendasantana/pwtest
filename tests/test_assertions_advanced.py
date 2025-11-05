import pytest
from playwright.sync_api import sync_playwright, expect
import os

@pytest.mark.assertions
def test_assertions_advanced():
    file_path = f"file://{os.getcwd()}/pages/assertions_demo.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(file_path)

        # 🔹 Assertion teks input + tombol
        name_input = page.locator("#nameInput")
        submit_btn = page.locator("#submitBtn")
        expect(name_input).to_be_visible()
        expect(submit_btn).to_be_enabled()

        # 🔹 Isi input dan klik tombol
        name_input.fill("Renda QA")
        submit_btn.click()

        # 🔹 Assertion teks hasil
        greeting = page.locator("#greeting")
        expect(greeting).to_have_text("Halo, Renda QA!")

        # 🔹 Assertion jumlah elemen list
        fruits = page.locator("#fruitsList li.fruit")
        expect(fruits).to_have_count(3)
        print(f"✅ Jumlah buah: {fruits.count()}")

        # 🔹 Assertion teks tiap elemen list
        fruit_texts = [fruits.nth(i).inner_text() for i in range(fruits.count())]
        assert fruit_texts == ["Apple", "Banana", "Cherry"]
        print(f"✅ Daftar buah: {fruit_texts}")

        # 🔹 Screenshot untuk laporan
        page.screenshot(path="reports/assertions_demo.png", full_page=True)
        print("✅ Screenshot tersimpan di reports/assertions_demo.png")

        browser.close()
