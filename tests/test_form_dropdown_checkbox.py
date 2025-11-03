from playwright.sync_api import sync_playwright, expect
import os, tempfile

def test_form_dropdown_and_checkbox(record_property):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buat HTML form dengan dropdown dan checkbox
        html_content = """
        <html>
        <body>
        <h2>Latihan Form - Dropdown & Checkbox</h2>
        <form id="myForm">
            Nama: <input type="text" id="name"><br><br>

            Pilih kota:
            <select id="city">
                <option value="">--Pilih--</option>
                <option value="Malang">Malang</option>
                <option value="Surabaya">Surabaya</option>
                <option value="Jakarta">Jakarta</option>
            </select><br><br>

            <label><input type="checkbox" id="agree"> Saya setuju dengan syarat & ketentuan</label><br><br>

            <input type="submit" value="Kirim">
        </form>

        <p id="result"></p>

        <script>
        document.getElementById("myForm").addEventListener("submit", function(e) {
            e.preventDefault();
            const name = document.getElementById("name").value;
            const city = document.getElementById("city").value;
            const agree = document.getElementById("agree").checked;

            if (!name || !city || !agree) {
                document.getElementById("result").innerText = "⚠️ Semua field wajib diisi!";
            } else {
                document.getElementById("result").innerText = 
                    "Halo " + name + " dari " + city + " 👋";
            }
        });
        </script>
        </body>
        </html>
        """

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmpfile.write(html_content.encode("utf-8"))
        tmpfile.close()

        # 2️⃣ Buka file HTML lokal
        page.goto(f"file://{tmpfile.name}")

        # 3️⃣ Isi form dan pilih kota
        page.fill("#name", "Renda")
        page.select_option("#city", "Malang")
        page.check("#agree")

        # 4️⃣ Klik kirim
        page.click("input[type='submit']")

        # 5️⃣ Validasi hasil
        expect(page.locator("#result")).to_have_text("Halo Renda dari Malang 👋")

        # 6️⃣ Screenshot hasilnya
        os.makedirs("tests-output/forms", exist_ok=True)
        screenshot_path = "tests-output/forms/form_dropdown_checkbox.png"
        page.screenshot(path=screenshot_path, full_page=False)
        record_property("screenshot", screenshot_path)

        print("✅ Dropdown & Checkbox berhasil divalidasi.")
        browser.close()
