import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.mark.consolelogs
def test_console_and_network_logs():
    log_file = os.path.join(os.getcwd(), "reports", "browser_logs.txt")

    # Pastikan folder reports ada
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "w", encoding="utf-8") as logf:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Tangkap log dari console
            def handle_console(msg):
                try:
                    logf.write(f"[Console] {msg.type.upper() if isinstance(msg.type, str) else msg.type()} : {msg.text()}\n")
                except Exception as e:
                    logf.write(f"[Console Error] {e}\n")

            page.on("console", handle_console)

            # Tangkap semua request
            def handle_request(req):
                try:
                    logf.write(f"[Request] {req.method} {req.url}\n")
                except Exception as e:
                    logf.write(f"[Request Error] {e}\n")

            page.on("request", handle_request)

            # Tangkap semua response
            def handle_response(res):
                try:
                    logf.write(f"[Response] {res.status} {res.url}\n")
                except Exception as e:
                    logf.write(f"[Response Error] {e}\n")

            page.on("response", handle_response)

            print("🌐 Membuka halaman...")
            page.goto("https://jsonplaceholder.typicode.com/")
            page.wait_for_timeout(3000)

            # Interaksi tambahan
            page.goto("https://jsonplaceholder.typicode.com/posts")
            page.wait_for_timeout(3000)

            browser.close()

    assert os.path.exists(log_file), "❌ File log tidak ditemukan!"
    print(f"✅ Log berhasil disimpan di: {log_file}")
