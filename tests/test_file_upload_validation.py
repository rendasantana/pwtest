import pytest
from pathlib import Path

@pytest.mark.smoke
def test_file_upload_validation(page):
    """Latihan 6: Upload file (versi offline, tanpa koneksi internet)"""
    try:
        # 1️⃣ Siapkan file HTML lokal
        html_path = Path("uploads/upload_test.html").absolute().as_uri()
        page.goto(html_path, timeout=60000)
        print(f"🌐 Membuka halaman lokal: {html_path}")

        # 2️⃣ Siapkan file upload
        upload_path = Path("uploads/sample.txt")
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        upload_path.write_text("Ini file contoh untuk latihan upload Playwright.")

        # 3️⃣ Upload file ke input
        file_input = page.locator("#fileInput")
        file_input.set_input_files(str(upload_path))
        print(f"📂 File diupload: {upload_path.name}")

        # 4️⃣ Validasi hasil upload (teks muncul di halaman)
        page.wait_for_selector("#fileName", state="visible")
        uploaded_text = page.inner_text("#fileName")
        assert upload_path.name in uploaded_text, "Nama file tidak muncul setelah upload!"

        print(f"✅ Upload file berhasil: {uploaded_text}")

    except Exception as e:
        pytest.fail(f"Terjadi error saat upload file: {e}")
