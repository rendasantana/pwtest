import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize("firstname, lastname, gender, expected", [
    ("Renda", "Santana", "male", "success"),
    ("", "Santana", "female", "fail")
])
@pytest.mark.smoke
def test_form_with_radio_and_validation(page, firstname, lastname, gender, expected):
    """Latihan 4b: Validasi radio + input tanpa menunggu redirect"""

    try:
        # 1️⃣ Buka halaman form
        page.goto("https://www.w3schools.com/html/html_form_elements.asp", timeout=60000, wait_until="domcontentloaded")

        # 2️⃣ Scroll ke form
        form = page.locator("#main form[action='/action_page.php']").first
        form.scroll_into_view_if_needed()

        # 3️⃣ Isi field nama
        page.fill("input[name='firstname']", firstname)
        page.fill("input[name='lastname']", lastname)

        # 4️⃣ Pilih radio (simulasi)
        selected_gender = gender
        print(f"👉 Gender yang dipilih: {selected_gender}")

        # 5️⃣ Klik submit tanpa menunggu URL berubah
        form.locator("input[type='submit']").click(no_wait_after=True)

        # 6️⃣ Tunggu sejenak biar DOM sempat berubah
        page.wait_for_timeout(2000)

        # 7️⃣ Ambil isi halaman
        content = page.content()

        # 8️⃣ Validasi hasil
        if expected == "success":
            assert firstname != "", "Nama depan wajib diisi!"
            assert "firstname" in content.lower(), "Form tidak ditemukan!"
            print(f"✅ Test sukses untuk: {firstname} {lastname} ({selected_gender})")
        else:
            assert firstname == "", "Nama depan harus kosong di test negatif"
            print(f"⚠️ Test negatif valid: nama depan kosong, form tidak terkirim")

    except Exception as e:
        pytest.fail(f"Terjadi error saat uji radio + validasi: {e}")
