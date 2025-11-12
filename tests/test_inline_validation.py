import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_inline_validation(page):
    """Latihan 9: Validasi Real-Time Saat User Mengetik"""

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latihan 9: Inline Validation</title>
        <style>
            .error { color: red; font-size: 14px; }
            input { display: block; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Form Validasi Real-Time</h2>

        <label>Nama (min. 3 karakter):</label>
        <input id="name" placeholder="Nama">
        <p id="nameError" class="error"></p>

        <label>Email:</label>
        <input id="email" placeholder="Email">
        <p id="emailError" class="error"></p>

        <script>
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const nameError = document.getElementById('nameError');
            const emailError = document.getElementById('emailError');

            nameInput.addEventListener('input', () => {
                if (nameInput.value.length < 3) {
                    nameError.textContent = 'Nama minimal 3 karakter!';
                } else {
                    nameError.textContent = '';
                }
            });

            emailInput.addEventListener('input', () => {
                if (!emailInput.value.includes('@')) {
                    emailError.textContent = 'Format email tidak valid!';
                } else {
                    emailError.textContent = '';
                }
            });
        </script>
    </body>
    </html>
    """

    # Tampilkan halaman HTML di browser
    page.set_content(html_content)

    # 🔹 Cek validasi nama
    page.fill("#name", "Re")
    expect(page.locator("#nameError")).to_have_text("Nama minimal 3 karakter!")

    page.fill("#name", "Renda")
    expect(page.locator("#nameError")).to_have_text("")

    # 🔹 Cek validasi email
    page.fill("#email", "renda")
    expect(page.locator("#emailError")).to_have_text("Format email tidak valid!")

    page.fill("#email", "renda@example.com")
    expect(page.locator("#emailError")).to_have_text("")

    print("✅ Test berhasil: Inline validation berfungsi sesuai harapan!")
