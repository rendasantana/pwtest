import logging
from datetime import datetime

# ====================================================
# Setup logging (semua log disimpan ke file + tampil di terminal)
# ====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("reports/test_log.txt", mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ====================================================
# Test verifikasi elemen dan logging
# ====================================================
def test_playwright_homepage(page):
    url = "https://playwright.dev"
    logger.info(f"🔗 Membuka halaman: {url}")

    # Buka halaman dengan timeout lebih panjang dan stabil
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    title = page.title()
    logger.info(f"📄 Judul halaman: {title}")

    # Ambil teks dari elemen h1 utama
    header = page.locator("h1").inner_text()
    logger.info(f"🧾 Header ditemukan: {header}")

    # Simpan screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"reports/screenshots/playwright_home_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    logger.info(f"📸 Screenshot disimpan di: {screenshot_path}")

    # Assertion: pastikan teks h1 mengandung kalimat ini
    expected = "Playwright enables reliable end-to-end testing"
    assert expected in header, f"Teks header tidak sesuai. Ditemukan: {header}"
