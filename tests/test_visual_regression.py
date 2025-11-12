import pytest
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageChops

@pytest.mark.smoke
def test_visual_regression(page):
    """Latihan 14: Visual Regression - Bandingkan screenshot baru dengan baseline"""

    # 1️⃣ Siapkan folder baseline dan hasil baru
    baseline_folder = Path("reports/visual_baseline")
    current_folder = Path("reports/visual_current")
    diff_folder = Path("reports/visual_diff")

    for folder in [baseline_folder, current_folder, diff_folder]:
        folder.mkdir(parents=True, exist_ok=True)

    # 2️⃣ Buat halaman HTML sederhana untuk tes
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visual Regression Test</title>
        <style>
            body { font-family: Arial; background-color: #fafafa; text-align: center; padding: 50px; }
            h1 { color: #333; }
            .box { width: 200px; height: 200px; background-color: #4CAF50; margin: 30px auto; border-radius: 12px; }
        </style>
    </head>
    <body>
        <h1>Halaman Uji Visual</h1>
        <div class="box"></div>
    </body>
    </html>
    """

    page.set_content(html_content)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 3️⃣ Screenshot baru
    current_path = current_folder / f"visual_{timestamp}.png"
    page.screenshot(path=str(current_path), full_page=True)
    print(f"📸 Screenshot baru disimpan di: {current_path}")

    # 4️⃣ Screenshot baseline pertama kali (hanya jika belum ada)
    baseline_path = baseline_folder / "baseline.png"
    if not baseline_path.exists():
        page.screenshot(path=str(baseline_path), full_page=True)
        print(f"✅ Baseline dibuat di: {baseline_path}")
        pytest.skip("Baseline belum ada, dibuat otomatis untuk perbandingan berikutnya.")

    # 5️⃣ Bandingkan screenshot baru dengan baseline
    baseline_img = Image.open(baseline_path)
    current_img = Image.open(current_path)
    diff = ImageChops.difference(baseline_img, current_img)

    diff_path = diff_folder / f"diff_{timestamp}.png"
    diff.save(diff_path)
    print(f"🧐 Hasil perbedaan disimpan di: {diff_path}")

    # 6️⃣ Jika gambar berbeda → fail
    bbox = diff.getbbox()
    if bbox:
        pytest.fail(f"❌ Visual mismatch ditemukan! Lihat hasil diff di {diff_path}")
    else:
        print("✅ Tampilan sama persis dengan baseline!")
