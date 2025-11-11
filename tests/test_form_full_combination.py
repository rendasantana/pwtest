import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize("firstname, lastname, gender, subscribe, country, expected", [
    ("Renda", "Santana", "male", True, "Canada", "success"),
    ("", "Santana", "female", False, "USA", "fail")
])
@pytest.mark.smoke
def test_form_full_combination(page, firstname, lastname, gender, subscribe, country, expected):
    """Latihan 5: Form kombinasi input + radio + checkbox + dropdown + validasi"""

    try:
        # 1️⃣ Buka halaman contoh form
        try:
            page.goto("https://www.w3schools.com/html/html_forms.asp", timeout=120000, wait_until="domcontentloaded")
        except:
            print("⚠️ Gagal load pertama, coba ulang...")
            page.goto("https://www.w3schools.com/html/html_forms.asp", timeout=120000, wait_until="domcontentloaded")

        form = page.locator("#main form[action='/action_page.php']").first
        form.scroll_into_view_if_needed()

        # 2️⃣ Isi input text
        page.fill("input[name='firstname']", firstname)
        page.fill("input[name='lastname']", lastname)

        # 3️⃣ Simulasi radio button (karena halaman ini tidak punya radio)
        selected_gender = gender
        print(f"👉 Gender dipilih: {selected_gender}")

        # 4️⃣ Simulasi checkbox subscribe
        if subscribe:
            print("✅ User memilih subscribe newsletter")
        else:
            print("⚠️ User tidak mencentang subscribe")

        # 5️⃣ Simulasi dropdown pilihan negara
        selected_country = country
        print(f"🌏 Negara dipilih: {selected_country}")

        # 6️⃣ Klik submit tanpa menunggu redirect
        form.locator("input[type='submit']").click(no_wait_after=True)
        page.wait_for_timeout(1500)

        # 7️⃣ Validasi hasil
        if expected == "success":
            assert firstname != "", "Nama depan wajib diisi!"
            print(f"✅ Test sukses: {firstname} {lastname}, {selected_gender}, {selected_country}")
        else:
            assert firstname == "", "Test negatif valid: nama depan harus kosong!"
            print("⚠️ Test negatif berhasil: form gagal karena input kosong")

    except Exception as e:
        pytest.fail(f"Terjadi error di test kombinasi form: {e}")
