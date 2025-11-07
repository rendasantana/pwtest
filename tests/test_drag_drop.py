import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.mark.dragdrop
def test_drag_and_drop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Buka halaman lokal
        drag_page = f"file://{os.getcwd()}/pages/drag_drop_demo.html"
        page.goto(drag_page)

        # Pastikan elemen muncul
        drag_source = page.locator("#dragSource")
        drop_target = page.locator("#dropTarget")

        assert drag_source.is_visible()
        assert drop_target.is_visible()

        # Lakukan drag and drop
        drag_source.drag_to(drop_target)

        # Verifikasi hasil drop
        page.wait_for_timeout(500)
        text = drop_target.text_content()
        assert "DROPPED" in text, "❌ Elemen belum berhasil di-drop!"

        print("✅ Drag and drop berhasil!")
        context.close()
        browser.close()
