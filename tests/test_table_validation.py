import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.table
def test_table_data_validation():
    """Validasi data tabel dari file HTML lokal"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka file HTML lokal
        base_url = "file://" + os.path.abspath("pages/table_example.html")
        page.goto(base_url)
        page.wait_for_load_state("domcontentloaded")

        # 2️⃣ Tunggu tabel muncul
        table = page.locator("#productTable")
        expect(table).to_be_visible()

        # 3️⃣ Ambil header kolom
        headers = page.locator("#productTable thead th").all_text_contents()
        print("🧭 Header kolom:", headers)
        assert headers == ["Nama Produk", "Kategori", "Harga"]

        # 4️⃣ Ambil semua baris data
        rows = page.locator("#productTable tbody tr")
        row_count = rows.count()
        print(f"📊 Jumlah baris data: {row_count}")
        assert row_count == 3

        # 5️⃣ Validasi isi baris pertama
        first_row = rows.nth(0).locator("td").all_text_contents()
        print("🔍 Baris pertama:", first_row)
        assert first_row == ["Kopi Arabica", "Minuman", "50000"]

        # 6️⃣ Screenshot hasil
        os.makedirs("reports/screenshots_table", exist_ok=True)
        screenshot_path = "reports/screenshots_table/local_table_check.png"
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot disimpan di: {screenshot_path}")

        browser.close()
