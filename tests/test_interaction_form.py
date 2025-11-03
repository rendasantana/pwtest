import os
from playwright.sync_api import Page

def test_form_interaction_block_assets(page: Page):
    page.set_default_navigation_timeout(160000)
    page.set_default_timeout(30000)

    def on_console(msg):
        print(f"CONSOLE: {msg.type} {msg.text}")
    page.on("console", on_console)

    def handle_route(route, request):
        url = request.url.lower()
        rtype = request.resource_type
        if rtype in ["image", "font"]:
            return route.abort()
        if any(ad in url for ad in ["doubleclick", "googlesyndication", "google-analytics", "ads", "gstatic", "adsystem"]):
            return route.abort()
        return route.continue_()

    page.route("**/*", handle_route)

    # Buka halaman
    page.goto("https://www.w3schools.com/html/html_forms.asp", wait_until="domcontentloaded")

    try:
        page.fill("input[name='firstname']", "Renda")
        page.fill("input[name='lastname']", "Santana")
    except Exception as e:
        print("Input langsung tidak ditemukan:", e)
        path = os.path.join(os.getcwd(), "tmp_page_snapshot.png")
        page.screenshot(path=path)
        print("Screenshot disimpan:", path)
        raise

    # 🎯 Perbaikan di sini: ambil submit button pertama saja
    submit_btn = page.locator("input[type='submit']").first
    submit_btn.scroll_into_view_if_needed()
    submit_btn.click()

    # Verifikasi
    print("✅ Form submit button diklik dengan sukses.")
