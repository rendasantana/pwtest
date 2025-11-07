import pytest
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

@pytest.mark.networklogjson
def test_network_logging_json():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        network_logs = []

        # Event listener untuk mencatat setiap request & response
        def log_request(request):
            network_logs.append({
                "type": "request",
                "url": request.url,
                "method": request.method,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        def log_response(response):
            network_logs.append({
                "type": "response",
                "url": response.url,
                "status": response.status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "size": len(response.body()) if response.ok else 0
            })

        page.on("request", log_request)
        page.on("response", log_response)

        # Akses halaman untuk tes
        page.goto("https://reqres.in/api/users?page=2")
        print("🌐 Halaman API ReqRes dibuka.")

        # Tunggu agar semua network selesai
        page.wait_for_timeout(3000)

        # Simpan hasil log ke file
        with open("network_log.json", "w") as f:
            json.dump(network_logs, f, indent=4)

        print(f"✅ Network log disimpan ke file network_log.json, total {len(network_logs)} event.")

        assert len(network_logs) > 0, "Tidak ada network log yang tercatat."

        browser.close()
