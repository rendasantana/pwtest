import pytest
import re
from playwright.sync_api import expect

@pytest.mark.smoke
def test_multistep_form_validation(page):
    """Latihan 8: Form Multi-Step (Step-by-Step Validation)"""

    try:
        # 1️⃣ Buat halaman HTML multi-step form
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Latihan 8: Multi-Step Form</title>
            <style>
                .step { display: none; margin-top: 20px; }
                .active { display: block; }
                .error { color: red; }
                .success { color: green; }
                button { margin-top: 10px; }
            </style>
        </head>
        <body>
            <h2>Form Pendaftaran Multi-Step</h2>

            <div id="step1" class="step active">
                <h3>Langkah 1: Data Pribadi</h3>
                <input id="name" placeholder="Nama Lengkap">
                <p id="error1" class="error"></p>
                <button id="next1">Next</button>
            </div>

            <div id="step2" class="step">
                <h3>Langkah 2: Kontak</h3>
                <input id="email" placeholder="Email">
                <p id="error2" class="error"></p>
                <button id="prev2">Back</button>
                <button id="next2">Next</button>
            </div>

            <div id="step3" class="step">
                <h3>Langkah 3: Konfirmasi</h3>
                <p id="summary"></p>
                <button id="prev3">Back</button>
                <button id="submitBtn">Submit</button>
                <p id="finalMsg" class="success"></p>
            </div>

            <script>
                const step1 = document.getElementById('step1');
                const step2 = document.getElementById('step2');
                const step3 = document.getElementById('step3');

                document.getElementById('next1').addEventListener('click', () => {
                    const name = document.getElementById('name').value.trim();
                    const error1 = document.getElementById('error1');
                    if (!name) {
                        error1.textContent = 'Nama wajib diisi!';
                    } else {
                        error1.textContent = '';
                        step1.classList.remove('active');
                        step2.classList.add('active');
                    }
                });

                document.getElementById('next2').addEventListener('click', () => {
                    const email = document.getElementById('email').value.trim();
                    const error2 = document.getElementById('error2');
                    if (!email.includes('@')) {
                        error2.textContent = 'Email tidak valid!';
                    } else {
                        error2.textContent = '';
                        step2.classList.remove('active');
                        step3.classList.add('active');
                        document.getElementById('summary').textContent = `Nama: ${document.getElementById('name').value}, Email: ${email}`;
                    }
                });

                document.getElementById('prev2').addEventListener('click', () => {
                    step2.classList.remove('active');
                    step1.classList.add('active');
                });

                document.getElementById('prev3').addEventListener('click', () => {
                    step3.classList.remove('active');
                    step2.classList.add('active');
                });

                document.getElementById('submitBtn').addEventListener('click', () => {
                    document.getElementById('finalMsg').textContent = '✅ Form berhasil dikirim!';
                });
            </script>
        </body>
        </html>
        """

        page.set_content(html_content)

        # 2️⃣ Step 1: Nama kosong → gagal lanjut
        page.click("#next1")
        expect(page.locator("#error1")).to_have_text("Nama wajib diisi!")

        # Isi nama lalu lanjut
        page.fill("#name", "Renda Arya Santana")
        page.click("#next1")
        expect(page.locator("#step2")).to_have_class(re.compile(".*active.*"))

        # 3️⃣ Step 2: Email salah format → gagal lanjut
        page.fill("#email", "renda")
        page.click("#next2")
        expect(page.locator("#error2")).to_have_text("Email tidak valid!")

        # Perbaiki email → lanjut ke step 3
        page.fill("#email", "renda@example.com")
        page.click("#next2")
        expect(page.locator("#step3")).to_have_class(re.compile(".*active.*"))
        expect(page.locator("#summary")).to_contain_text("renda@example.com")

        # 4️⃣ Submit form
        page.click("#submitBtn")
        expect(page.locator("#finalMsg")).to_have_text("✅ Form berhasil dikirim!")

        print("✅ Test berhasil: Multi-step form divalidasi dan berjalan sesuai alur!")

    except Exception as e:
        pytest.fail(f"Terjadi error di Latihan 8: {e}")
