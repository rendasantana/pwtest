import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_form_with_select_and_checkbox(page):
    """Latihan 3: Mengisi form dengan dropdown dan checkbox"""

    try:
        # 1️⃣ Buka halaman latihan yang punya dropdown dan checkbox
        page.goto("https://www.w3schools.com/html/html_form_elements.asp", timeout=120000, wait_until="domcontentloaded")

        # 2️⃣ Pastikan halaman termuat
        expect(page).to_have_title(lambda title: "HTML" in title)

        # 3️⃣ Scroll agar form terlihat
        form = page.locator("#main form[action='/action_page.php']").first
        form.scroll_into_view_if_needed()

        # 4️⃣ Isi dropdown (select element)
        country_select = form.locator("select[name='cars']")
        country_select.select_option("audi")
        expect(country_select).to_have_value("audi")

        # 5️⃣ Centang checkbox (dua contoh di bawah)
        form.locator("input[type='checkbox'][value='Bike']").check()
        form.locator("input[type='checkbox'][value='Car']").check()

        # 6️⃣ Klik tombol submit
        form.locator("input[type='submit']").click()

        # 7️⃣ Tunggu halaman hasil
        page.wait_for_url("**/action_page.php", timeout=15000)
        expect(page).to_have_url("https://www.w3schools.com/action_page.php")

        # 8️⃣ Validasi hasil
        content = page.content()
        assert "Bike" in content or "Car" in content
        assert "audi" in content or "Audi" in content

        print("\n✅ Dropdown dan checkbox berhasil diisi & diverifikasi!")

    except Exception as e:
        pytest.fail(f"Terjadi error saat pengujian form dropdown & checkbox: {e}")
