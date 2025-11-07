import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.mark.networklog
def test_network_logging():
    # Pastikan folder log ada
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "network_log.txt")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        logs = []

        # ✅ Event listener untuk request
        page.on("request", lambda req: logs.append(f"➡️ Request: {req.method} {req.url}"))

        # ✅ Event listener untuk response
        def handle_response(res):
            try:
                logs.append(f"⬅️ Response: {res.status} {res.url}")
            except Exception as e:
                logs.append(f"⚠️ Error parsing response: {e}")

        page.on("response", handle_response)

        # 🧭 Buka halaman web untuk dipantau
        page.goto("https://example.com")

        # Tunggu sebentar agar semua request termuat
        page.wait_for_timeout(3000)

        # 🚀 Simpan log ke file
        with open(log_file, "w", encoding="utf-8") as f:
            for log in logs:
                f.write(log + "\n")

        print(f"\n📁 Log network tersimpan di: {log_file}")
        print(f"Total {len(logs)} event tercatat.")

        browser.close()
