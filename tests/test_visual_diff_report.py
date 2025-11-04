import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageDraw

# Folder untuk hasil visual test
REPORT_DIR = "reports/screenshots"
os.makedirs(REPORT_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def browser_context():
    """Fixture browser Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        yield context
        context.close()
        browser.close()


@pytest.fixture(autouse=True)
def visual_diff_on_failure(request):
    """Ambil visual diff kalau test gagal"""
    yield
    outcome = request.node.rep_call
    if outcome.failed:
        page = request.node.funcargs.get("page")
        if not page:
            print("⚠️ Tidak ada page untuk ambil screenshot.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name

        baseline_path = os.path.join(REPORT_DIR, f"baseline_{test_name}.png")
        current_path = os.path.join(REPORT_DIR, f"current_{test_name}_{timestamp}.png")
        diff_path = os.path.join(REPORT_DIR, f"diff_{test_name}_{timestamp}.png")

        # Simpan screenshot saat ini
        page.screenshot(path=current_path, full_page=True)

        if not os.path.exists(baseline_path):
            # Buat baseline pertama kali
            os.rename(current_path, baseline_path)
            print(f"📸 Baseline dibuat pertama kali: {baseline_path}")
        else:
            # Bandingkan dengan baseline
            diff_image(baseline_path, current_path, diff_path)
            print(f"🔍 Diff image dibuat: {diff_path}")

            # Tambahkan ke pytest-html report
            if hasattr(request.config, "_html"):
                extra = getattr(request.config, "_html").extras
                from pytest_html import extras
                extra.append(extras.image(baseline_path, mime_type="image/png", name="Baseline"))
                extra.append(extras.image(current_path, mime_type="image/png", name="Current"))
                extra.append(extras.image(diff_path, mime_type="image/png", name="Diff"))


def pytest_runtest_makereport(item, call):
    """Hook pytest untuk simpan status test"""
    if "visual_diff_on_failure" in item.fixturenames:
        if call.when == "call":
            item.rep_call = call


def diff_image(baseline_path, current_path, diff_path):
    """Bandingkan dua gambar dan simpan diff"""
    img1 = Image.open(baseline_path).convert("RGB")
    img2 = Image.open(current_path).convert("RGB")

    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()

    if bbox:
        # Tandai area berbeda dengan warna merah
        draw = ImageDraw.Draw(diff)
        draw.rectangle(bbox, outline="red", width=5)
        diff.save(diff_path)
    else:
        print("✅ Tidak ada perbedaan visual.")
        diff = Image.new("RGB", img1.size, color=(0, 255, 0))
        diff.save(diff_path)


def test_visual_google(browser_context):
    """Test tampilan Google dan buat diff jika gagal"""
    page = browser_context.new_page()
    page.goto("https://www.google.com/?hl=en", timeout=60000)
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(REPORT_DIR, "temp_google.png"))

    # Buat error visual sengaja (elemen yang tidak ada)
    assert page.is_visible("text=Nonexistent Element")

    page.close()
