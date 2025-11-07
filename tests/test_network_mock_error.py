import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.networkmockerror
def test_network_mock_error():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Intercept request ke endpoint tertentu dan balas dengan error 500
        def handle_route(route, request):
            if "https://jsonplaceholder.typicode.com/posts/1" in request.url:
                route.fulfill(
                    status=500,
                    content_type="application/json",
                    body='{"error": "Internal Server Error"}'
                )
            elif "https://jsonplaceholder.typicode.com/posts/2" in request.url:
                route.fulfill(
                    status=404,
                    content_type="application/json",
                    body='{"error": "Not Found"}'
                )
            else:
                route.continue_()

        context.route("**/*", handle_route)

        # Tes 500 Internal Server Error
        page.goto("https://jsonplaceholder.typicode.com/posts/1")
        content_500 = page.text_content("body")
        print("🧱 Respons 500:")
        print(content_500)
        assert "Internal Server Error" in content_500, "❌ Mock error 500 gagal!"

        # Tes 404 Not Found
        page.goto("https://jsonplaceholder.typicode.com/posts/2")
        content_404 = page.text_content("body")
        print("🚫 Respons 404:")
        print(content_404)
        assert "Not Found" in content_404, "❌ Mock error 404 gagal!"

        print("✅ Mock API error test berhasil!")
        context.close()
        browser.close()
