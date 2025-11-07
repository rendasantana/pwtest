import os
import sys
import datetime
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.debugcapture
def test_debug_capture_on_fail():
    # 🧹 Bersihkan namespace global dari variabel yang sering bentrok
    for name in ["text", "count", "type"]:
        if name in globals():
            print(f"⚠️ Hapus variabel global bentrok: {name}")
            del globals()[name]

    debug_dir = os.path.join(os.getcwd(), "reports", "debug_logs")
    os.makedirs(debug_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        console_logs = []
        network_logs = []

        # 🔍 Tangkap log console tanpa memanggil method (pakai atribut internal)
        def on_console(msg):
            msg_type = getattr(msg, "_type", None) or "unknown"
            msg_text = getattr(msg, "_text", None) or "no text"
            console_logs.append(f"[{msg_type}] {msg_text}")

        context.on("console", on_console)

        # 🌐 Tangkap log network aman
        def on_request(req):
            method = getattr(req, "method", "UNKNOWN")
            url = getattr(req, "url", "NO_URL")
            network_logs.append(f"REQ → {method} {url}")

        def on_response(res):
            status = getattr(res, "status", "???")
            url = getattr(res, "url", "NO_URL")
            network_logs.append(f"RES ← {status} {url}")

        context.on("request", on_request)
        context.on("response", on_response)

        page = context.new_page()
        try:
            # 🧭 Akses halaman contoh
            page.goto("https://example.com")
            page.wait_for_timeout(1000)

            # 🔎 Ambil semua H1 via JavaScript (hindari method .count() & .all_inner_texts())
            all_texts = page.evaluate("Array.from(document.querySelectorAll('h1')).map(e => e.innerText)")
            h1_count = len(all_texts)
            print(f"🔍 Jumlah elemen H1 ditemukan: {h1_count}")

            heading_text = all_texts[0] if all_texts else "(kosong)"
            print(f"📄 Isi H1: {heading_text}")

            # ❌ Simulasikan kegagalan
            assert "Example" in heading_text, "Judul tidak sesuai yang diharapkan!"

        except AssertionError as e:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # 📸 Screenshot
            screenshot_path = os.path.join(debug_dir, f"screenshot_fail_{timestamp}.png")
            page.screenshot(path=screenshot_path, full_page=True)

            # 🧾 Log console
            console_path = os.path.join(debug_dir, f"console_{timestamp}.log")
            with open(console_path, "w") as f:
                f.write("\n".join(console_logs))

            # 🌐 Log network
            network_path = os.path.join(debug_dir, f"network_{timestamp}.log")
            with open(network_path, "w") as f:
                f.write("\n".join(network_logs))

            print(f"""
❌ Test gagal! Semua data debug disimpan:
📸 Screenshot: {screenshot_path}
🧾 Console log: {console_path}
🌐 Network log: {network_path}
""")
            raise e

        finally:
            context.close()
            browser.close()
