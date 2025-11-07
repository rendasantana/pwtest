import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.networkintercept
def test_network_intercept():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Intercept request ke API JSON placeholder (API dummy)
        def handle_route(route, request):
            if "https://jsonplaceholder.typicode.com/todos/1" in request.url:
                fake_response = {
                    "userId": 123,
                    "id": 1,
                    "title": "🚀 Data ini hasil intercept, bukan dari API asli!",
                    "completed": False
                }
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=str(fake_response)
                )
            else:
                route.continue_()

        # Aktifkan intercept
        context.route("**/*", handle_route)

        # Buka halaman yang memanggil API (misalnya site dummy)
        page.goto("https://jsonplaceholder.typicode.com/todos/1")

        # Ambil isi halaman (akan tampil respons hasil intercept)
        print("📄 Konten halaman:")
        print(page.text_content("body"))

        # Validasi bahwa teks hasil intercept muncul
        assert "hasil intercept" in page.text_content("body"), "❌ Intercept gagal!"

        print("✅ Intercept dan modifikasi response berhasil!")

        context.close()
        browser.close()
