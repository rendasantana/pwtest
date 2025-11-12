import pytest
from datetime import datetime
from pathlib import Path

@pytest.mark.smoke
def test_screenshot_capture(page):
    """Latihan 13 (offline): Screenshot full page dan elemen tertentu dari halaman lokal"""

    # 1️⃣ Siapkan folder penyimpanan
    folder_path = Path("reports/screenshots")
    folder_path.mkdir(parents=True, exist_ok=True)

    # 2️⃣ Buat halaman HTML lokal untuk uji screenshot
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latihan Screenshot</title>
        <style>
            body { font-family: Arial; background-color: #f5f5f5; padding: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #ddd; }
            button { background-color: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; margin-top: 20px; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>Data Pelanggan</h1>
        <table id="customers">
            <tr><th>Nama</th><th>Kota</th></tr>
            <tr><td>Renda</td><td>Malang</td></tr>
            <tr><td>Arya</td><td>Surabaya</td></tr>
        </table>
        <button class="btn-apply">Apply</button>
    </body>
    </html>
    """

    # 3️⃣ Load konten HTML langsung (tanpa koneksi internet)
    page.set_content(html_content)

    # 4️⃣ Screenshot seluruh halaman
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = folder_path / f"fullpage_{timestamp}.png"
    page.screenshot(path=str(full_path), full_page=True)
    print(f"📸 Screenshot full page disimpan di: {full_path}")

    # 5️⃣ Screenshot tabel
    table = page.locator("#customers")
    table_path = folder_path / f"table_{timestamp}.png"
    table.screenshot(path=str(table_path))
    print(f"📸 Screenshot tabel disimpan di: {table_path}")

    # 6️⃣ Screenshot tombol
    button = page.locator(".btn-apply")
    button_path = folder_path / f"button_{timestamp}.png"
    button.screenshot(path=str(button_path))
    print(f"📸 Screenshot tombol disimpan di: {button_path}")

    # 7️⃣ Validasi file tersimpan
    assert full_path.exists()
    assert table_path.exists()
    assert button_path.exists()
    print("✅ Semua screenshot berhasil diambil dan tersimpan!")
