import pytest
from pathlib import Path

@pytest.mark.smoke
def test_file_upload_image_preview(page):
    """Latihan 6b: Upload gambar dan validasi preview muncul"""

    try:
        # 1️⃣ Siapkan file HTML lokal
        html_path = Path("uploads/image_preview.html").absolute().as_uri()
        page.goto(html_path, timeout=60000)
        print(f"🌐 Membuka halaman lokal: {html_path}")

        # 2️⃣ Siapkan file gambar untuk upload
        image_path = Path("uploads/sample_image.png")
        image_path.parent.mkdir(parents=True, exist_ok=True)

        # Buat file gambar dummy (jika belum ada)
        if not image_path.exists():
            from PIL import Image
            img = Image.new("RGB", (200, 200), color=(73, 109, 137))
            img.save(image_path)

        # 3️⃣ Upload gambar
        page.locator("#imageInput").set_input_files(str(image_path))
        print(f"🖼️ Gambar diupload: {image_path.name}")

        # 4️⃣ Validasi preview muncul
        preview = page.locator("#preview")
        preview.wait_for(state="visible", timeout=5000)
        src_value = preview.get_attribute("src")

        assert src_value and "data:image" in src_value, "❌ Preview gambar tidak muncul!"
        print("✅ Preview gambar berhasil ditampilkan di halaman!")

    except Exception as e:
        pytest.fail(f"Terjadi error saat upload gambar: {e}")
