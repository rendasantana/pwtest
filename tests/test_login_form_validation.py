import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_login_form_validation(page):
    """Latihan 10: Validasi Form Login + Notifikasi"""

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latihan 10: Login Validation</title>
        <style>
            body { font-family: Arial; margin: 30px; }
            .error { color: red; margin-top: 10px; }
            .success { color: green; margin-top: 10px; }
            input { display: block; margin-top: 5px; }
            button { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Form Login</h2>

        <label>Username:</label>
        <input id="username" placeholder="Masukkan username">

        <label>Password:</label>
        <input id="password" type="password" placeholder="Masukkan password">

        <button id="loginBtn">Login</button>
        <p id="message"></p>

        <script>
            const loginBtn = document.getElementById('loginBtn');
            const message = document.getElementById('message');

            loginBtn.addEventListener('click', () => {
                const user = document.getElementById('username').value.trim();
                const pass = document.getElementById('password').value.trim();

                if (!user || !pass) {
                    message.textContent = '⚠️ Username dan password wajib diisi!';
                    message.className = 'error';
                } else if (user === 'renda' && pass === '12345') {
                    message.textContent = '✅ Login berhasil!';
                    message.className = 'success';
                } else {
                    message.textContent = '❌ Username atau password salah!';
                    message.className = 'error';
                }
            });
        </script>
    </body>
    </html>
    """

    # 1️⃣ Tampilkan halaman HTML di browser
    page.set_content(html_content)

    # 2️⃣ Coba submit tanpa isi form
    page.click("#loginBtn")
    expect(page.locator("#message")).to_have_text("⚠️ Username dan password wajib diisi!")

    # 3️⃣ Isi username saja
    page.fill("#username", "renda")
    page.click("#loginBtn")
    expect(page.locator("#message")).to_have_text("⚠️ Username dan password wajib diisi!")

    # 4️⃣ Isi username dan password salah
    page.fill("#username", "wrong")
    page.fill("#password", "0000")
    page.click("#loginBtn")
    expect(page.locator("#message")).to_have_text("❌ Username atau password salah!")

    # 5️⃣ Isi data benar
    page.fill("#username", "renda")
    page.fill("#password", "12345")
    page.click("#loginBtn")
    expect(page.locator("#message")).to_have_text("✅ Login berhasil!")

    print("✅ Test berhasil: Validasi login berjalan sesuai skenario!")
