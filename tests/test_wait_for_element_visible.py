import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.wait
def test_wait_for_element_visible():
    """Latihan: menunggu elemen terlihat setelah loading selesai (halaman cepat & stabil)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        print("🔄 Membuka halaman TodoMVC Playwright demo...")
        page.goto("https://demo.playwright.dev/todomvc", wait_until="domcontentloaded", timeout=60000)

        # Tunggu hingga input utama terlihat (indikator loading selesai)
        page.wait_for_selector("input.new-todo", state="visible", timeout=10000)
        print("✅ Halaman sudah siap, input Todo terlihat.")

        # Tambahkan item baru
        page.locator("input.new-todo").fill("Belajar Playwright")
        page.keyboard.press("Enter")

        # Tunggu item muncul di daftar
        page.wait_for_selector("ul.todo-list li", state="visible", timeout=5000)
        expect(page.locator("ul.todo-list li")).to_contain_text("Belajar Playwright")
        print("🎉 Validasi sukses: item Todo muncul di daftar.")

        browser.close()
