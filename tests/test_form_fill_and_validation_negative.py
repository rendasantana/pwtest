import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_form_fill_and_validation_negative(page):
    """Latihan 2b: Uji form dengan field kosong (negative test)"""

    try:
        # 1️⃣ Buka halaman form
        page.goto("https://www.w3schools.com/html/html_forms.asp", timeout=120000, wait_until="domcontentloaded")

        # 2️⃣ Arahkan ke form pertama
        form = page.locator("#main form[action='/action_page.php']").first
        form.scroll_into_view_if_needed()

        # 3️⃣ Kosongkan field (pastikan tidak ada isi)
        form.locator("input[name='firstname']").fill("")
        form.locator("input[name='lastname']").fill("")

        # 4️⃣ Klik tombol Submit
        form.locator("input[type='submit']").click()

        # 5️⃣ Tunggu redirect
        page.wait_for_url("**/action_page.php", timeout=15000)

        # 6️⃣ Verifikasi hasil di halaman action_page
        expect(page).to_have_url("https://www.w3schools.com/action_page.php")

        content = page.content()
        # Karena field kosong, hasil halaman harus menampilkan string kosong
        assert "First name:" in content
        assert "Last name:" in content

        print("\n⚠️  Form berhasil dikirim walau kosong — tidak ada validasi client-side.")

    except Exception as e:
        pytest.fail(f"Terjadi error saat pengujian form kosong: {e}")
