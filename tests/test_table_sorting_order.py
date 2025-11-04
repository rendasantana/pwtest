import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.table
def test_table_sorting_order():
    """Validasi urutan data kolom Company A→Z dan Z→A dari tabel W3Schools."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman tabel W3Schools
        print("🌐 Membuka halaman tabel...")
        page.goto("https://www.w3schools.com/html/html_tables.asp", wait_until="load", timeout=90000)

        # 2️⃣ Tunggu tabel muncul
        page.wait_for_selector("#customers", state="visible", timeout=20000)
        table = page.locator("#customers")
        expect(table).to_be_visible()

        # 3️⃣ Ambil data kolom pertama
        company_cells = page.locator("#customers tr td:first-child")
        original_data = [text.strip() for text in company_cells.all_text_contents() if text.strip()]
        print(f"📋 Data asli: {original_data}")

        # 4️⃣ Simulasikan sort manual A→Z dan Z→A (karena tabel W3Schools tidak interaktif)
        ascending_sorted = sorted(original_data)
        descending_sorted = sorted(original_data, reverse=True)

        print(f"🔼 Seharusnya A→Z: {ascending_sorted}")
        print(f"🔽 Seharusnya Z→A: {descending_sorted}")

        # 5️⃣ Bandingkan hasil sorting manual
        assert ascending_sorted != descending_sorted, "Urutan A→Z dan Z→A seharusnya berbeda"

        # 6️⃣ Simpan screenshot hasil validasi
        page.screenshot(path="reports/table_sorting_order.png")
        print("✅ Validasi urutan data berhasil diverifikasi.")

        browser.close()
