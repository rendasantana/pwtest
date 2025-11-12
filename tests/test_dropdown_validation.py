import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_dropdown_validation(page):
    """Latihan 11: Dropdown & Select Validation"""

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latihan 11: Dropdown Validation</title>
        <style>
            body { font-family: Arial; margin: 30px; }
            select, button { margin-top: 10px; display: block; }
            .error { color: red; margin-top: 10px; }
            .success { color: green; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Pilih Negara Anda</h2>

        <select id="country">
            <option value="">-- Pilih Negara --</option>
            <option value="indonesia">Indonesia</option>
            <option value="canada">Canada</option>
            <option value="japan">Japan</option>
        </select>

        <button id="submitBtn">Kirim</button>
        <p id="message"></p>

        <script>
            document.getElementById('submitBtn').addEventListener('click', () => {
                const country = document.getElementById('country').value;
                const msg = document.getElementById('message');
                if (!country) {
                    msg.textContent = '⚠️ Anda harus memilih negara!';
                    msg.className = 'error';
                } else {
                    msg.textContent = `✅ Negara ${country} berhasil dipilih!`;
                    msg.className = 'success';
                }
            });
        </script>
    </body>
    </html>
    """

    # 1️⃣ Tampilkan halaman HTML
    page.set_content(html_content)

    # 2️⃣ Klik submit tanpa pilih negara → error
    page.click("#submitBtn")
    expect(page.locator("#message")).to_have_text("⚠️ Anda harus memilih negara!")

    # 3️⃣ Pilih negara "Indonesia" → sukses
    page.select_option("#country", "indonesia")
    page.click("#submitBtn")
    expect(page.locator("#message")).to_have_text("✅ Negara indonesia berhasil dipilih!")

    # 4️⃣ Pilih negara "Japan" → sukses juga
    page.select_option("#country", "japan")
    page.click("#submitBtn")
    expect(page.locator("#message")).to_have_text("✅ Negara japan berhasil dipilih!")

    print("✅ Test berhasil: Validasi dropdown berjalan sesuai harapan!")
