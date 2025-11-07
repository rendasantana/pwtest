import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.networkhar
def test_capture_har_file():
    har_path = os.path.join(os.getcwd(), "reports", "network_capture.har")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Buat context dengan fitur record_har diaktifkan
        context = browser.new_context(
            record_har_path=har_path,
            record_har_content="attach"
        )
        page = context.new_page()

        print("🌐 Membuka halaman untuk merekam network traffic...")
        page.goto("https://jsonplaceholder.typicode.com/posts")
        page.wait_for_timeout(3000)

        print("🧭 Navigasi ke halaman lain...")
        page.goto("https://jsonplaceholder.typicode.com/users")
        page.wait_for_timeout(2000)

        # Tutup context agar HAR tersimpan
        context.close()
        browser.close()

    assert os.path.exists(har_path), "❌ File HAR tidak ditemukan!"
    print(f"✅ File HAR berhasil disimpan di: {har_path}")
