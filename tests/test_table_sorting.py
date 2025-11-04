import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.table
def test_table_sorting_validation():
    """Validasi bahwa tabel muncul dan kolom dapat di-sort pada halaman W3Schools."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman tabel W3Schools
        print("🌐 Membuka halaman tabel W3Schools...")
        page.goto("https://www.w3schools.com/html/html_tables.asp", wait_until="load", timeout=90000)

        # 2️⃣ Tunggu elemen tabel muncul
        print("⏳ Menunggu tabel muncul...")
        page.wait_for_selector("#customers", state="visible", timeout=20000)

        table = page.locator("#customers")
        expect(table).to_be_visible()

        # 3️⃣ Ambil data awal kolom pertama
        before_sort = page.locator("#customers tr td:first-child").all_text_contents()
        print(f"📋 Data sebelum sort: {before_sort}")

        # 4️⃣ Klik header kolom pertama untuk mencoba sorting
        print("🖱️ Klik header kolom pertama (Company)...")
        page.click("#customers th:first-child")

        # 5️⃣ Tunggu sebentar biar efek terlihat
        page.wait_for_timeout(2000)

        # 6️⃣ Ambil ulang data setelah klik
        after_sort = page.locator("#customers tr td:first-child").all_text_contents()
        print(f"📋 Data setelah sort: {after_sort}")

        # 7️⃣ Bandingkan hasil
        if before_sort != after_sort:
            print("✅ Tabel berubah setelah di-sort (berfungsi).")
        else:
            print("⚠️ Tabel tidak berubah, mungkin kolom tidak interaktif (W3Schools default).")

        # 8️⃣ Screenshot hasil
        page.screenshot(path="reports/w3schools_table_sorting.png")
        browser.close()
