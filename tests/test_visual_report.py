import os
from datetime import datetime
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

# Folder laporan
REPORT_DIR = "reports/visual"
BASELINE_DIR = os.path.join(REPORT_DIR, "baseline")
NEW_DIR = os.path.join(REPORT_DIR, "new")
DIFF_DIR = os.path.join(REPORT_DIR, "diff")

for d in [REPORT_DIR, BASELINE_DIR, NEW_DIR, DIFF_DIR]:
    os.makedirs(d, exist_ok=True)

def generate_html_report(baseline, new, diff, result_text):
    """Buat file HTML perbandingan visual"""
    html_path = os.path.join(REPORT_DIR, "visual_report.html")

    html_content = f"""
    <html>
    <head>
        <title>Visual Regression Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f8f9fa;
            }}
            h1 {{ color: #333; }}
            .container {{
                display: flex;
                gap: 20px;
            }}
            .card {{
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 8px rgba(0,0,0,0.1);
                padding: 10px;
            }}
            img {{
                max-width: 350px;
                border-radius: 5px;
            }}
            .result {{
                margin-top: 20px;
                font-weight: bold;
                color: {'green' if 'OK' in result_text else 'red'};
            }}
        </style>
    </head>
    <body>
        <h1>Visual Regression Report</h1>
        <div class="container">
            <div class="card">
                <h3>Baseline</h3>
                <img src="{baseline}" alt="Baseline">
            </div>
            <div class="card">
                <h3>New</h3>
                <img src="{new}" alt="New">
            </div>
            <div class="card">
                <h3>Diff</h3>
                <img src="{diff}" alt="Diff">
            </div>
        </div>
        <p class="result">{result_text}</p>
    </body>
    </html>
    """

    with open(html_path, "w") as f:
        f.write(html_content)

    print(f"📄 Laporan dibuat: {html_path}")


def test_visual_report():
    """Tes visual regression dengan laporan HTML"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://playwright.dev/python/")
        page.wait_for_load_state("domcontentloaded")

        new_path = os.path.join(NEW_DIR, "homepage_new.png")
        page.screenshot(path=new_path, full_page=True)

        baseline_path = os.path.join(BASELINE_DIR, "homepage.png")

        if not os.path.exists(baseline_path):
            page.screenshot(path=baseline_path, full_page=True)
            print("✅ Baseline pertama dibuat:", baseline_path)
            browser.close()
            return

        # Bandingkan dua gambar
        baseline = Image.open(baseline_path).convert("RGB")
        new_image = Image.open(new_path).convert("RGB")
        diff = ImageChops.difference(baseline, new_image)
        diff_path = os.path.join(DIFF_DIR, "diff_homepage.png")

        diff_bbox = diff.getbbox()
        if diff_bbox:
            diff.save(diff_path)
            result_text = "❌ Visual berubah! Cek diff di laporan HTML"
        else:
            result_text = "✅ Visual masih sama (tidak ada perubahan)"
            diff = Image.new("RGB", baseline.size, (255, 255, 255))
            diff.save(diff_path)

        generate_html_report(
            baseline=baseline_path,
            new=new_path,
            diff=diff_path,
            result_text=result_text
        )

        browser.close()
