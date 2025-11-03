from playwright.sync_api import sync_playwright, expect
import os, tempfile

def test_form_fill_and_validation(record_property):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buat file HTML form sederhana secara lokal
        html_content = """
        <html>
        <body>
        <h2>Latihan Form</h2>
        <form id="myForm">
            First name:<br>
            <input type="text" id="fname" name="firstname"><br>
            Last name:<br>
            <input type="text" id="lname" name="lastname"><br><br>
            <input type="submit" value="Submit">
        </form>
        <p id="result"></p>
        <script>
        document.getElementById("myForm").addEventListener("submit", function(e) {
            e.preventDefault();
            const fname = document.getElementById("fname").value;
            const lname = document.getElementById("lname").value;
            document.getElementById("result").innerText = "Halo, " + fname + " " + lname + "!";
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

        # 3️⃣ Isi form
        page.fill("#fname", "Renda")
        page.fill("#lname", "Santana")

        # 4️⃣ Klik submit
        page.click("input[type='submit']")

        # 5️⃣ Validasi hasil
        expect(page.locator("#result")).to_have_text("Halo, Renda Santana!")

        # 6️⃣ Screenshot hasilnya
        os.makedirs("tests-output/forms", exist_ok=True)
        screenshot_path = "tests-output/forms/form_local_result.png"
        page.screenshot(path=screenshot_path, full_page=False)
        record_property("screenshot", screenshot_path)

        print("✅ Form lokal berhasil diisi dan divalidasi.")
        browser.close()
