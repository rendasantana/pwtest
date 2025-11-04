import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.waitbutton
def test_wait_for_button_enabled():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        # 1️⃣ Buka halaman kosong
        page.goto("about:blank")

        # 2️⃣ Sisipkan HTML demo secara langsung
        html_content = """
        <html>
        <body>
            <h2>Button Enable Test</h2>
            <button id="myBtn" disabled>Click Me</button>
            <script>
                // Tombol akan aktif setelah 3 detik
                setTimeout(() => {
                    document.getElementById('myBtn').disabled = false;
                }, 3000);
            </script>
        </body>
        </html>
        """
        page.set_content(html_content)

        # 3️⃣ Ambil tombol
        button = page.locator("#myBtn")

        # 4️⃣ Pastikan awalnya disabled
        expect(button).to_be_disabled()

        # 5️⃣ Tunggu tombol jadi enabled
        expect(button).to_be_enabled(timeout=5000)

        # 6️⃣ Klik tombol setelah aktif
        button.click()

        browser.close()
