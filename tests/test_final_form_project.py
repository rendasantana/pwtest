import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import expect

@pytest.mark.smoke
def test_final_form_project(page):
    """Latihan 15 (Final): Form lengkap + validasi + screenshot hasil"""

    # 1️⃣ Siapkan folder report & screenshot
    reports_folder = Path("reports/final_project")
    reports_folder.mkdir(parents=True, exist_ok=True)

    # 2️⃣ Buat halaman HTML form lengkap
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Final Project Form</title>
        <style>
            body { font-family: Arial; background: #f6f6f6; padding: 40px; }
            form { background: white; padding: 20px; border-radius: 10px; width: 350px; margin: auto; }
            input, select { display: block; width: 100%; margin-bottom: 12px; padding: 8px; }
            button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
            p.success { color: green; }
            p.error { color: red; }
        </style>
    </head>
    <body>
        <form id="form">
            <h2>Form Pendaftaran QA</h2>
            <input id="name" placeholder="Nama Lengkap">
            <input id="email" placeholder="Email">
            <select id="role">
                <option value="">Pilih Role</option>
                <option value="qa">Quality Assurance</option>
                <option value="dev">Developer</option>
                <option value="pm">Product Manager</option>
            </select>
            <label><input type="checkbox" id="agree"> Saya menyetujui syarat & ketentuan</label>
            <button id="submitBtn">Kirim</button>
            <p id="message"></p>
        </form>

        <script>
            document.getElementById('submitBtn').addEventListener('click', function(e){
                e.preventDefault();
                const name = document.getElementById('name').value.trim();
                const email = document.getElementById('email').value.trim();
                const role = document.getElementById('role').value;
                const agree = document.getElementById('agree').checked;
                const msg = document.getElementById('message');

                if(!name || !email.includes('@') || !role || !agree){
                    msg.textContent = '❌ Data belum lengkap atau tidak valid!';
                    msg.className = 'error';
                } else {
                    msg.textContent = '✅ Form berhasil dikirim!';
                    msg.className = 'success';
                }
            });
        </script>
    </body>
    </html>
    """

    page.set_content(html_content)

    # 3️⃣ Isi form dengan data valid
    page.fill("#name", "Renda Arya Santana")
    page.fill("#email", "renda@example.com")
    page.select_option("#role", "qa")
    page.check("#agree")

    # 4️⃣ Submit form
    page.click("#submitBtn")

    # 5️⃣ Validasi hasil
    expect(page.locator("#message")).to_have_text("✅ Form berhasil dikirim!")

    # 6️⃣ Ambil screenshot hasil akhir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = reports_folder / f"final_form_{timestamp}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"📸 Screenshot hasil tersimpan di: {screenshot_path}")

    print("✅ Test Final Project selesai dan sukses!")

