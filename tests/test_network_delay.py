import pytest
import time
from playwright.sync_api import sync_playwright

@pytest.mark.networkdelay
def test_network_delay():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def handle_route(route, request):
            if "https://jsonplaceholder.typicode.com/users/1" in request.url:
                print("🌐 Simulasi delay 5 detik...")
                time.sleep(5)
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"userId": 1, "name": "Test Delay", "status": "slow"}'
                )
            else:
                route.continue_()

        context.route("**/*", handle_route)

        start_time = time.time()
        page.goto("https://jsonplaceholder.typicode.com/users/1")
        duration = time.time() - start_time

        print(f"⏱️ Durasi respons: {duration:.2f} detik")
        content = page.text_content("body")
        assert "Test Delay" in content, "❌ Data hasil delay tidak muncul!"
        assert duration >= 5, "❌ Delay tidak terjadi!"

        print("✅ Simulasi delay dan timeout berhasil!")
        context.close()
        browser.close()
