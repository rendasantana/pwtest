import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_form_fill_and_validation(page):
    """Latihan 2: Mengisi dan validasi form dengan selector spesifik & aman"""

    try:
        # 1️⃣ Buka halaman form
        page.goto("https://www.w3schools.com/html/html_forms.asp", timeout=120000, wait_until="domcontentloaded")

        # 2️⃣ Pastikan halaman benar
        expect(page).to_have_url("https://www.w3schools.com/html/html_forms.asp")

        # 3️⃣ Scroll ke area form pertama
        form = page.locator("#main form[action='/action_page.php']").first
        form.scroll_into_view_if_needed()

        # 4️⃣ Isi input di dalam form itu saja
        form.locator("input[name='firstname']").fill("Renda")
        form.locator("input[name='lastname']").fill("Santana")

        # 5️⃣ Klik tombol Submit di form itu
        form.locator("input[type='submit']").click()

        # 6️⃣ Tunggu halaman hasil
        page.wait_for_url("**/action_page.php", timeout=15000)
        expect(page).to_have_url("https://www.w3schools.com/action_page.php")

        # 7️⃣ Validasi isi hasil
        content = page.content()
        assert "Renda" in content
        assert "Santana" in content

        print("\n✅ Form berhasil diisi dan diverifikasi!")

    except Exception as e:
        pytest.fail(f"Terjadi error saat pengujian form: {e}")
